# -*- encoding: utf-8 -*-

"""
Convenience logging setup
"""

import logging
import os
import re
import signal
import sys
import threading
import time
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

try:
    # faulthandler is only available in python 3.3+
    import faulthandler
    from typing import List, Optional

except ImportError:
    faulthandler = None

from runez.ascii import AsciiAnimation
from runez.convert import to_bytesize, to_int
from runez.date import local_timezone
from runez.file import basename as get_basename, parent_folder
from runez.system import _getframe, _R, cached_property, decode, find_caller_frame, flattened, quoted, short, string_type, stringified
from runez.system import LOG, Slotted, TERMINAL_INFO, ThreadGlobalContext, UNSET, WINDOWS


ORIGINAL_CF = logging.currentframe
RE_FORMAT_MARKERS = re.compile(r"{([a-z][a-z0-9_]*)}", re.IGNORECASE)


def formatted(message, *args, **kwargs):
    """
    Args:
        message (str): Message to format, support either the '%s' old method, or newer format() method

    Returns:
        (str): Formatted message
    """
    if not kwargs:
        if not args:
            return message

        if "%s" in message:
            try:
                return message % args

            except TypeError:
                pass

    try:
        return message.format(*args, **kwargs)

    except (IndexError, KeyError):
        return message


class ProgressHandler(logging.Handler):
    """Used to capture logging chatter and show it as progress"""

    level = logging.DEBUG

    @classmethod
    def handle(cls, record):
        """Intercept all log chatter and show it as progress message"""
        LogManager.progress._show_debug(record.getMessage())

    @classmethod
    def emit(cls, record):
        """Not needed"""

    @classmethod
    def createLock(cls):
        """Not needed"""


class ProgressBar(object):

    def __init__(self, iterable=None, total=None, columns=8, frames=u" ▏▎▍▌▋▊▉"):
        self.columns = columns
        self.frames = frames
        self.per_char = 100.0 / columns
        self.blank_char = frames[0]
        self.full_char = frames[-1]
        self.frame_count = len(frames) - 2
        self.per_frame = self.per_char / self.frame_count if self.frame_count > 0 else None
        self.iterable = iterable
        self.parent = None  # type: Optional[ProgressBar] # Parent progress bar, if any
        if total is None and hasattr(iterable, "__len__"):
            total = len(iterable)

        self.total = total
        self.n = None

    def __repr__(self):
        return "%s/%s" % (self.n, self.total)

    def __iter__(self):
        if self.iterable:
            self.start()
            for x in self.iterable:
                yield x
                self.update()

            self.stop()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *_):
        self.stop()

    def start(self):
        """Start tracking progress with this progressbar"""
        if self.n is None:
            self.n = 0
            LogManager.progress._add_progress_bar(self)

    def stop(self):
        """Stop / cleanup this progressbar"""
        if self.n is not None:
            self.n = None
            LogManager.progress._remove_progress_bar(self)

    def update(self, n=1):
        """Manually update the progress bar, advance progress by 'n'"""
        self.n += n

    def rendered(self):
        """Called in spinner thread (lock already acquired)"""
        if self.n is None:
            return None

        if self.total:
            percent = max(int(round(100.0 * self.n / self.total)), 0)
            blanks = 0
            if percent >= 100:
                percent = 100
                bar = self.full_char * self.columns

            else:
                full_chars = int(percent / self.per_char)
                bar = self.full_char * full_chars
                blanks = self.columns - full_chars
                if self.per_frame:
                    blanks -= 1
                    fi = int((percent - full_chars * self.per_char) / self.per_frame)
                    bar += self.frames[fi]

            return u"%s%s%s%%" % (bar, self.blank_char * blanks, percent)

    def _remove_parent(self, parent):
        if parent is self.parent:
            self.parent = parent.parent

        elif self.parent is not None:
            self.parent._remove_parent(parent)


class _SpinnerComponent(object):

    def __init__(self, fps, source, color, adapter=None):
        self.adapter = adapter
        self.source = source  # type: callable
        self.color = color  # type: Optional[callable]
        self.update_delay = 1.0 / fps
        self.next_update = 0
        self.current_text = None  # type: Optional[str]

    def add_text(self, line, columns):
        """(int): size of text added to 'line' (lock already acquired)"""
        text = self.current_text
        if not text or columns <= 0:
            return 0

        if self.adapter is not None:
            text = self.adapter(text)

        size = len(text)
        if self.adapter is not None or size > columns:
            text = short(text, size=columns)

        if self.color:
            text = self.color(text)

        line.append(text)
        return size

    def update_text(self, ts):
        """(int): 1 if changed, 0 otherwise, called by spinner thread (lock already acquired)"""
        if self.next_update < ts:
            self.next_update = ts + self.update_delay
            text = self.source()
            if text is not self.current_text:
                self.current_text = text
                return 1

        return 0


class _SpinnerState(object):

    def __init__(self, parent, frames, max_columns, message_color, progress_color, spinner_color):
        """
        Args:
            parent (ProgressSpinner): Parent object
            frames (AsciiFrames): Frames to use for spinner
            max_columns (int | None): Optional max number of columns to use
            message_color (callable | None): Optional color to use for the message
            progress_color (callable | None): Optional color to use for the spinner
            spinner_color (callable | None): Optional color to use for the spinner
        """
        self.columns = TERMINAL_INFO.columns - 2
        if max_columns and max_columns > 0:
            self.columns = min(max_columns, self.columns)

        self.frames = _SpinnerComponent(frames.fps, frames.next_frame, spinner_color)
        self.progress_bar = _SpinnerComponent(2, parent._get_progress, progress_color)
        self.message = _SpinnerComponent(2, parent._get_message, message_color, adapter=_R._runez_module().uncolored)
        self.max_fps = max(2, frames.fps)

    def get_line(self, ts):
        """Called by spinner thread (lock already acquired)"""
        n = self.frames.update_text(ts) + self.progress_bar.update_text(ts) + self.message.update_text(ts)
        if n > 0:
            line = []
            columns = self.columns
            columns -= self.frames.add_text(line, columns)
            columns -= self.progress_bar.add_text(line, columns)
            self.message.add_text(line, columns)
            return " %s" % " ".join(line) if line else ""


class ProgressSpinner(object):
    """
    Background progress spinner on stderr tty - with an animation conveying that work is being performed.
    This can be enabled with one call:
        runez.log.progress.start()

    A background thread provides spinner animation, will be automatically closed on program exit or when this is called:
        runez.log.progress.stop()

    Optionally, a ProgressBar can be added
    """

    def __init__(self):
        self.is_running = False
        self._current_line = None
        self._fps = 60.0  # Higher fps for _run(), to reduce flickering as much as possible (float for py2 compat)
        self._has_progress_line = False
        self._msg_show = None  # type: Optional[str] # Message coming from show() calls
        self._msg_debug = None  # type: Optional[str] # Message coming from trace() or debug() calls
        self._progress_bar = None  # type: Optional[ProgressBar]
        self._state = None  # type: Optional[_SpinnerState]
        self._stderr_write = None
        self._stdout_write = None
        self._thread = None  # type: Optional[threading.Thread] # Background daemon thread used to display progress

    def show(self, message):
        """
        Args:
            message (str | None): Show 'message' on progress spinner line (this overrides any debug/trace inferred messages)
        """
        with self._lock:
            self._msg_show = message

    def start(self, frames=UNSET, max_columns=140, message_color=UNSET, progress_color=UNSET, spinner_color=None):
        """Start a background thread to handle spinner, if stderr is a tty

        Args:
            frames (AsciiFrames | callable | str | None): Frames to use for spinner animation
            max_columns (int | None): Maximum number of terminal columns to use for progress line
            message_color (callable | None): Optional color to use for the message part
            progress_color (callable | None): Optional color to use for the progress bar
            spinner_color (callable | None): Optional color to use for the animated spinner
        """
        with self._lock:
            if self._thread is None:
                self._stderr_write = self._original_write(sys.stderr)
                if self._stderr_write is not None:
                    if message_color is UNSET:
                        message_color = _R._runez_module().dim

                    if progress_color is UNSET:
                        progress_color = _R._runez_module().teal

                    frames = AsciiAnimation.get_frames(frames)
                    self._state = _SpinnerState(self, frames, max_columns, message_color, progress_color, spinner_color)
                    try:
                        sys.stderr.write = self._on_stderr  # Will fail in py2
                        self._stdout_write = self._original_write(sys.stdout)
                        if self._stdout_write is not None:
                            sys.stdout.write = self._on_stdout

                    except AttributeError:  # pragma: no cover
                        pass

                    self._thread = threading.Thread(target=self._run, name="Progress")
                    self._thread.daemon = True
                    self._thread.start()
                    self.is_running = True
                    LogManager._auto_enable_progress_handler()

    def stop(self):
        """Stop progress spinner thread, called in any thread"""
        with self._lock:
            if self._thread is None:
                return

            self._thread = None

        attempts = 10
        while attempts > 0:
            with self._lock:
                if not self.is_running:  # Wait for thread to exit before cleaning up write functions it may be still using
                    break

            time.sleep(0.05)
            attempts -= 1

        with self._lock:
            self.is_running = False
            LogManager._auto_enable_progress_handler()
            if self._has_progress_line:  # pragma: no cover (hard to cover in tests)
                self._clear_line()
                self._has_progress_line = False

            if sys.stdout.write == self._on_stdout:
                sys.stdout.write = self._stdout_write

            if sys.stderr.write == self._on_stderr:
                sys.stderr.write = self._stderr_write

            self._stderr_write = None
            self._stdout_write = None

    @cached_property
    def _lock(self):
        return threading.RLock()

    def _show_debug(self, message):
        """Show 'message' on next progress line update, called in main thread"""
        with self._lock:
            self._msg_debug = message

    def _get_message(self):
        """Called in spinner thread (lock already acquired)"""
        if self._msg_show is not None:
            return self._msg_show

        return self._msg_debug

    def _get_progress(self):
        """Called in spinner thread (lock already acquired)"""
        if self._progress_bar:
            return self._progress_bar.rendered()

    def _add_progress_bar(self, bar):
        """Called in main thread"""
        with self._lock:
            if bar is not self._progress_bar:
                bar.parent = self._progress_bar
                self._progress_bar = bar

    def _remove_progress_bar(self, bar):
        """Called in main thread"""
        with self._lock:
            if bar is self._progress_bar:
                self._progress_bar = bar.parent

            elif self._progress_bar:
                self._progress_bar._remove_parent(bar)

    @staticmethod
    def _original_write(stream):
        """Called in main thread (lock already acquired)"""
        if TERMINAL_INFO.isatty(stream):
            return getattr(stream, "write", None)

    def _clean_write(self, write, message):
        """Output 'message' using 'write' function, ensure any pending progress line is cleared first"""
        if message:
            message = decode(message)
            with self._lock:
                if self._has_progress_line:
                    self._clear_line()
                    self._has_progress_line = False

                if self._has_progress_line is False and message.endswith("\n"):
                    self._has_progress_line = None

                write(message)

    def _on_stdout(self, message):
        """Intercepted print() or sys.stdout.write()"""
        self._clean_write(self._stdout_write, message)

    def _on_stderr(self, message):
        """Intercepted sys.stderr.write()"""
        self._clean_write(self._stderr_write, message)

    def _clear_line(self):
        """Called in spinner thread (lock already acquired)"""
        self._write("\r\033[K")

    def _write(self, text):
        """Called in any thread (lock already acquired)"""
        self._stderr_write(text)

    def _run(self):
        """Background thread handling progress reporting and animation"""
        try:
            sleep_delay = 1 / self._fps
            frequency = int(self._fps / self._state.max_fps) - 1
            countdown = 0
            line = None
            while self._thread:
                time.sleep(sleep_delay)
                countdown -= 1
                if countdown < 0 or self._has_progress_line is None:
                    with self._lock:
                        if countdown < 0:
                            countdown = frequency
                            line = self._state.get_line(time.time())

                        if line:
                            self._clear_line()
                            self._write(line)
                            self._write("\r")
                            self._has_progress_line = True

        finally:
            self.is_running = False
            self.stop()


class TraceHandler(object):
    """
    Allows to optionally provide trace logging, typically activated by an env var, like:
        MY_APP_DEBUG=1 my-app ...
    """

    def __init__(self, prefix, stream):
        self.prefix = prefix
        self.stream = stream

    def trace(self, message):
        """
        Args:
            message (str): Message to trace
        """
        self.stream.write("%s%s%s" % (self.prefix or "", message, "\n" if not message.endswith("\n") else ""))
        self.stream.flush()


class LoggingSnapshot(Slotted):
    """
    Take a snapshot of parts we're modifying in the 'logging' module, in order to be able to restore it as it was
    """

    __slots__ = ["_srcfile", "critical", "fatal", "error", "exception", "warning", "info", "debug"]

    def _seed(self):
        """Seed initial fields"""
        for name in self.__slots__:
            setattr(self, name, getattr(logging, name))

    def restore(self):
        for name in self.__slots__:
            setattr(logging, name, getattr(self, name))


class LogSpec(Slotted):
    """
    Settings to use, you can safely customize these (before calling runez.log.setup), for example:
        runez.log.setup(console_stream=sys.stdout)
    or
        runez.log.spec.set(console_stream=sys.stdout)
        runez.log.setup()
    or
        runez.log.spec.console_stream = sys.stdout
        runez.log.setup()
    """

    # See setup()'s docstring for meaning of each field
    __slots__ = [
        "appname",
        "basename",
        "console_format",
        "console_level",
        "console_stream",
        "context_format",
        "default_logger",
        "dev",
        "file_format",
        "file_level",
        "file_location",
        "locations",
        "rotate",
        "rotate_count",
        "timezone",
        "tmp",
    ]

    @property
    def argv(self):
        """str: Command line invocation, represented to show as greeting"""
        return quoted(sys.argv)

    @property
    def pid(self):
        """str: Current process id represented to show as greeting"""
        return os.getpid()

    def usable_location(self):
        """
        Returns:
            str | None: First available usable location
        """
        if not self.should_log_to_file:
            return None

        if self.file_location is not None:
            # Custom location typically provided via --config CLI flag
            return self._auto_complete_filename(self.file_location)

        if self.locations:
            for location in self.locations:
                path = self._auto_complete_filename(location)
                if path:
                    return path

    @property
    def should_log_to_file(self):
        """
        Returns:
            bool: As per the spec, should we be logging to a file?
        """
        if not self.file_format:
            return False

        if self.file_location is not None:
            return bool(self.file_location)

        return bool(self.locations)

    def _props(self, **additional):
        r = dict(argv=self.argv, pid=self.pid)
        r.update(self.to_dict())
        r.update(additional)
        return r

    def _auto_complete_filename(self, location):
        """
        Args:
            location (str | None): Location to auto-complete with {basename}, if it points to a folder

        Returns:
            (str | None): {location}/{basename}
        """
        props = self._props()
        path = _formatted_text(location, props, strict=True)
        if path:
            if os.path.isdir(path):
                filename = _formatted_text(self.basename, props, strict=True)
                if not filename or not is_writable_folder(path):
                    return None

                return os.path.join(path, filename)

            parent = parent_folder(path)
            if not is_writable_folder(parent):
                try:
                    os.mkdir(parent)  # Create only one folder if possible (no mkdir -p)

                except OSError:
                    return None

            if is_writable_folder(parent):
                return path


def is_writable_folder(path):
    return path and os.path.isdir(path) and os.access(path, os.W_OK)


class _ContextFilter(logging.Filter):
    """
    Optional logging filter allowing to inject key/value pairs to every log record.

    In order to activate this:
    - Mention %(context)s in your log format
    - Add key/value pairs via runez.log.context.add_global(), runez.log.context.add_threadlocal()
    """

    def __init__(self, context, name=""):
        """
        Args:
            context (ThreadGlobalContext): Associated context
            name (str): Passed through to parent
        """
        super(_ContextFilter, self).__init__(name=name)
        self.context = context

    def filter(self, record):
        """Determines if the record should be logged and injects context info into the record. Always returns True"""
        fmt = LogManager.spec.context_format
        if fmt:
            data = self.context.to_dict()
            if data:
                record.context = fmt % ",".join("%s=%s" % (key, val) for key, val in sorted(data.items()) if key and val)

            else:
                record.context = ""

        return True


def default_log_locations():
    if WINDOWS:  # pragma: no cover
        return [os.path.join("{dev}", "log", "{basename}")]

    return ["{dev}/log/{basename}", "/logs/{appname}/{basename}", "/var/log/{basename}"]


class LogManager(object):
    """
    Global logging context managed by runez.
    There's only one, as multiple contexts would not be useful (logging setup is a global thing)
    """

    # Defaults used to initialize LogSpec instances
    # Use runez.log.override_spec() to change these defaults (do not change directly)
    _default_spec = LogSpec(
        appname=None,
        basename="{appname}.log",
        console_format="%(asctime)s %(levelname)s %(message)s",
        console_level=logging.WARNING,
        console_stream=sys.stderr,
        context_format="[[%s]] ",
        default_logger=LOG.debug,
        dev=None,
        file_format="%(asctime)s %(timezone)s [%(threadName)s] %(context)s%(levelname)s - %(message)s",
        file_level=logging.DEBUG,
        file_location=None,
        locations=default_log_locations(),
        rotate=None,
        rotate_count=10,
        timezone=local_timezone(),
        tmp=None,
    )

    # Spec defines how logs should be setup()
    # Best way to provide your spec is via: runez.log.setup(), for example:
    #   runez.log.setup(rotate="size:50m")
    spec = LogSpec(_default_spec)

    # Thread-local / global context
    context = ThreadGlobalContext(_ContextFilter)

    # Progress spinner, with animation (on tty only)
    progress = ProgressSpinner()

    # Below fields should be read-only for outside users, do not modify these
    debug = False
    console_handler = None  # type: Optional[logging.StreamHandler]
    file_handler = None  # type: Optional[logging.FileHandler] # File we're currently logging to (if any)
    handlers = None  # type: Optional[List[logging.Handler]]
    tracer = None  # type: Optional[TraceHandler]
    used_formats = None  # type: Optional[str]
    faulthandler_signum = None  # type: Optional[int]
    trace_env_var = "TRACE_DEBUG"

    _lock = threading.RLock()
    _logging_snapshot = LoggingSnapshot()

    @classmethod
    def set_debug(cls, debug):
        """Useful only as simple callback function, use runez.log.setup() for regular usage"""
        if debug is not UNSET:
            cls.debug = bool(debug)

        return cls.debug

    @classmethod
    def set_dryrun(cls, dryrun):
        """Useful only as simple callback function, use runez.log.setup() for regular usage"""
        _R.set_dryrun(dryrun)
        return _R.is_dryrun()

    @classmethod
    def set_file_location(cls, file_location):
        """Useful only as simple callback function, use runez.log.setup() for regular usage"""
        LogManager.spec.set(file_location=file_location)
        return cls.spec.file_location

    @classmethod
    def setup(
        cls,
        debug=UNSET,
        dryrun=UNSET,
        level=UNSET,
        clean_handlers=UNSET,
        greetings=UNSET,
        appname=UNSET,
        basename=UNSET,
        console_format=UNSET,
        console_level=UNSET,
        console_stream=UNSET,
        context_format=UNSET,
        default_logger=UNSET,
        dev=UNSET,
        file_format=UNSET,
        file_level=UNSET,
        file_location=UNSET,
        locations=UNSET,
        rotate=UNSET,
        rotate_count=UNSET,
        timezone=UNSET,
        tmp=UNSET,
        trace=UNSET,
    ):
        """
        Args:
            debug (bool): Enable debug level logging (overrides other specified levels)
            dryrun (bool): Enable dryrun
            level (int | None): Shortcut to set both `console_level` and `file_level` at once
            clean_handlers (bool): Remove any existing logging.root.handlers
            greetings (str | list[str] | None): Optional greetings message(s) to log
            appname (str | None): Program's base name, not used directly, just as reference for default 'basename'
            basename (str | None): Base name of target log file, not used directly, just as reference for default 'locations'
            console_format (str | None): Format to use for console log, use None to deactivate
            console_level (int | None): Level to use for console logging
            console_stream (io.TextIOBase | TextIO | None): Stream to use for console log (eg: sys.stderr), use None to deactivate
            context_format (str | None): Format to use for contextual log, use None to deactivate
            default_logger (callable | None): Default logger to use to trace operations such as runez.run() etc
            dev (str | None): Custom folder to use when running from a development venv (auto-determined if None)
            file_format (str | None): Format to use for file log, use None to deactivate
            file_level (int | None): Level to use for file logging
            file_location (str | None): Desired custom file location (overrides {locations} search, handy as a --log cli flag)
            locations (list[str]|None): List of candidate folders for file logging (None: deactivate file logging)
            rotate (str | None): How to rotate log file (None: no rotation, "time:1d" time-based, "size:50m" size-based)
            rotate_count (int): How many rotations to keep
            timezone (str | None): Time zone, use None to deactivate time zone logging
            tmp (str | None): Optional temp folder to use (auto determined)
            trace (str | bool): Env var to enable tracing, example: "DEBUG+| " to trace when $DEBUG defined (+ [optional] "| " as prefix)
        """
        with cls._lock:
            cls.set_debug(debug)
            cls.set_dryrun(dryrun)
            cls.spec.set(
                appname=appname,
                basename=basename,
                console_format=console_format,
                console_level=console_level or level,
                console_stream=console_stream,
                context_format=context_format,
                default_logger=default_logger,
                dev=dev,
                file_format=file_format,
                file_level=file_level or level,
                file_location=file_location,
                locations=locations,
                rotate=rotate,
                rotate_count=rotate_count,
                timezone=timezone,
                tmp=tmp,
            )

            cls._auto_fill_defaults()
            if cls.debug:
                cls.spec.console_level = logging.DEBUG
                cls.spec.file_level = logging.DEBUG

            elif level:
                cls.spec.console_level = level
                cls.spec.file_level = level

            root_level = min(flattened([cls.spec.console_level, cls.spec.file_level], keep_empty=None))
            if root_level and root_level != logging.root.level:
                logging.root.setLevel(root_level)

            if trace is UNSET:
                if cls.tracer is None:
                    trace = cls.trace_env_var

            elif isinstance(trace, string_type):
                cls.trace_env_var = trace

            if isinstance(trace, string_type) and "+" in trace:
                p = trace.partition("+")
                cls.enable_trace(p[0], prefix=p[2])

            else:
                cls.enable_trace(trace)

            if cls.handlers is None:
                cls.handlers = []

            cls._setup_console_handler()
            cls._setup_file_handler()
            cls._auto_enable_progress_handler()
            cls._update_used_formats()
            cls._fix_logging_shortcuts()
            if clean_handlers:
                cls.clean_handlers()

            cls.greet(greetings)

    @classmethod
    def current_test(cls):
        """
        Returns:
            (str | None): Not empty if we're currently running a test (such as via pytest)
                          Actual value will be path to test_<name>.py file if user followed usual conventions,
                          otherwise path to first found test-framework module
        """
        import re

        regex = re.compile(r"^(.+\.|)(conftest|(test_|_pytest|unittest).+|.+_test)$")

        def is_test_frame(f):
            name = f.f_globals.get("__name__")
            if name and not name.startswith("runez"):
                return regex.match(name.lower()) and f.f_globals.get("__file__")

        return find_caller_frame(validator=is_test_frame)

    @staticmethod
    def dev_folder(*relative_path):
        """
        Args:
            *relative_path: Optional additional relative path to add

        Returns:
            (str | None): Path to development build folder (such as .venv, .tox etc), if we're currently running a dev build
        """
        venv = os.environ.get("VIRTUAL_ENV")
        if venv:
            return venv

        folder = _find_parent_folder(sys.prefix, {"venv", ".venv", ".tox", "build"})
        if folder and relative_path:
            folder = os.path.join(folder, *relative_path)

        return folder

    @staticmethod
    def project_path(*relative_path):
        """
        Args:
            *relative_path: Optional additional relative path to add

        Returns:
            (str | None): Computed path, if we're currently running a dev build
        """
        path = _validated_project_path(LogManager.tests_path, LogManager.dev_folder)
        if path and relative_path:
            path = os.path.join(path, *relative_path)

        return path

    @staticmethod
    def tests_path(*relative_path):
        """
        Args:
            *relative_path: Optional additional relative path to add

        Returns:
            (str | None): Computed path, if we're currently running a test
        """
        path = _find_parent_folder(LogManager.current_test(), {"tests", "test"})
        if relative_path:
            path = os.path.join(path, *relative_path)

        return path

    @classmethod
    def greet(cls, greetings, logger=LOG.debug):
        """
        Args:
            greetings (str | list[str] | None): Greetings message(s) to log
            logger (callable | None): Logger to use
        """
        if greetings and logger:
            for msg in flattened(greetings, keep_empty=False):
                message = cls.formatted_greeting(msg)
                if message:
                    logger(message)

    @classmethod
    def clean_handlers(cls):
        """Remove all non-runez logging handlers"""
        for h in list(logging.root.handlers):
            if h is not cls.console_handler and h is not cls.file_handler and h is not ProgressHandler:
                logging.root.removeHandler(h)

    @classmethod
    def program_path(cls, path=None):
        """
        Args:
            path (str | None): Optional, path or name to consider (default: `sys.argv[0]`)

        Returns:
            (str): Path of currently running program
        """
        return path or sys.argv[0]

    @classmethod
    def reset(cls):
        """Reset logging as it was before setup(), no need to call this outside of testing, or some very special cases"""
        cls._disable_faulthandler()
        if cls.handlers is not None:
            for handler in cls.handlers:
                logging.root.removeHandler(handler)

            cls.handlers = None

        cls._logging_snapshot.restore()
        cls.context.reset()
        cls.spec = LogSpec(cls._default_spec)
        cls.debug = None
        cls.console_handler = None
        cls.file_handler = None
        cls.progress.stop()
        cls.tracer = None
        cls.used_formats = None

    @classmethod
    def formatted_greeting(cls, greeting):
        if greeting:
            if cls.file_handler and cls.file_handler.baseFilename:
                location = cls.file_handler.baseFilename

            elif not cls.spec.should_log_to_file:
                location = "file log disabled"

            elif cls.spec.file_location:
                location = "given location '{file_location}' is not usable"

            else:
                location = "no usable locations from {locations}"

            return _formatted_text(greeting, cls.spec._props(location=location))

    @classmethod
    def silence(cls, *modules, **kwargs):
        """
        Args:
            *modules: Modules, or names of modules to silence (by setting their log level to WARNING or above)
            **kwargs: Pass as kwargs due to python 2.7, would be level=logging.WARNING otherwise
        """
        level = kwargs.pop("level", logging.WARNING)
        for mod in modules:
            name = mod.__name__ if hasattr(mod, "__name__") else mod
            logging.getLogger(name).setLevel(level)

    @classmethod
    def is_using_format(cls, markers, used_formats=None):
        """
        Args:
            markers (str): Space separated list of markers to look for
            used_formats (str): Formats to consider (default: cls.used_formats)

        Returns:
            (bool): True if any one of the 'markers' is seen in 'used_formats'
        """
        if used_formats is None:
            used_formats = cls.used_formats

        if not markers or not used_formats:
            return False

        return any(marker in used_formats for marker in flattened(markers, split=" "))

    @classmethod
    def enable_faulthandler(cls, signum=getattr(signal, "SIGUSR1", None)):
        """Enable dumping thread stack traces when specified signals are received, similar to java's handling of SIGQUIT

        Note: this must be called from the surviving process in case of daemonization.

        Args:
            signum (int | None): Signal number to register for full thread stack dump (use None to disable)
        """
        with cls._lock:
            if not signum:
                cls._disable_faulthandler()
                return

            if not cls.file_handler or faulthandler is None:
                return

            cls.faulthandler_signum = signum
            dump_file = cls.file_handler.stream
            faulthandler.enable(file=dump_file, all_threads=True)
            faulthandler.register(signum, file=dump_file, all_threads=True, chain=False)

    @classmethod
    def override_spec(cls, **kwargs):
        """OVerride 'spec' and '_default_spec' with given values"""
        cls._default_spec.set(**kwargs)
        cls.spec.set(**kwargs)

    @classmethod
    def enable_trace(cls, spec, prefix=":: ", stream=UNSET):
        """
        Args:
            spec (str | bool | None): If string given, enable tracing when corresponding env var is set to a non-empty value
            prefix (str | None): Prefix to use for trace messages (default: ":: ")
            stream: Where to trace (by default: current 'console_stream' if configured, otherwise sys.stderr)
        """
        if spec is not UNSET:
            if spec and (not isinstance(spec, string_type) or spec in os.environ):
                cls.tracer = TraceHandler(prefix, stream or cls.spec.console_stream or sys.stderr)

            else:
                cls.tracer = None

    @classmethod
    def trace(cls, message, *args, **kwargs):
        """
        Args:
            message (str): Message to trace
        """
        if cls.tracer or cls.progress.is_running:
            message = formatted(message, *args, **kwargs)
            cls.progress._show_debug(message)
            if cls.tracer:
                cls.tracer.trace(message)

    @classmethod
    def _auto_enable_progress_handler(cls):
        if cls.progress.is_running:
            if ProgressHandler not in logging.root.handlers:
                logging.root.handlers.append(ProgressHandler)

        elif ProgressHandler in logging.root.handlers:
            logging.root.handlers.remove(ProgressHandler)

    @classmethod
    def _update_used_formats(cls):
        cls.used_formats = None
        for handler in (cls.console_handler, cls.file_handler):
            fmt = _get_fmt(handler)
            if fmt:
                cls.used_formats = "%s %s" % (cls.used_formats or "", fmt)
                cls.used_formats = cls.used_formats.strip()

    @classmethod
    def _setup_console_handler(cls):
        fmt = _canonical_format(cls.spec.console_format)
        level = cls.spec.console_level
        target = cls.spec.console_stream
        existing = cls.console_handler
        if existing is None or _get_fmt(existing) != fmt or existing.level != level or existing.stream != target:
            if existing is not None:
                cls.handlers.remove(existing)
                logging.root.removeHandler(existing)

            if target:
                cls.console_handler = cls._add_handler(logging.StreamHandler(target), fmt, level)

    @classmethod
    def _setup_file_handler(cls):
        fmt = _canonical_format(cls.spec.file_format)
        level = cls.spec.file_level
        target = cls.spec.usable_location()
        existing = cls.file_handler
        if existing is None or _get_fmt(existing) != fmt or existing.level != level or existing.baseFilename != target:
            if existing is not None:
                cls.handlers.remove(existing)
                logging.root.removeHandler(existing)

            if target:
                cls.file_handler = cls._add_handler(_get_file_handler(target, cls.spec.rotate, cls.spec.rotate_count), fmt, level)

    @classmethod
    def _add_handler(cls, new_handler, fmt, level):
        if fmt:
            new_handler.setFormatter(logging.Formatter(fmt))

        if level:
            new_handler.setLevel(level)

        logging.root.addHandler(new_handler)
        cls.handlers.append(new_handler)
        return new_handler

    @classmethod
    def _auto_fill_defaults(cls):
        """Late auto-filled missing defaults (caller's value kept if provided)"""
        if not cls.spec.appname:
            cls.spec.appname = get_basename(cls.program_path())

        if not cls.spec.dev:
            cls.spec.dev = cls.dev_folder()

    @classmethod
    def _disable_faulthandler(cls):
        if faulthandler and cls.faulthandler_signum:
            faulthandler.unregister(cls.faulthandler_signum)
            faulthandler.disable()
            cls.faulthandler_signum = None

    @classmethod
    def _fix_logging_shortcuts(cls):
        """
        Fix standard logging shortcuts to correctly report logging module.

        This is only useful if you:
        - actually use %(name) and care about it being correct
        - you would still like to use the logging.info() etc shortcuts

        So basically you'd like to write this:
            import logging
            logging.info("hello")

        Instead of this:
            import logging
            LOG = logging.getLogger(__name__)
            LOG.info("hello")
        """
        if cls.is_using_format("%(context)"):
            cls.context.enable(True)
            for handler in cls.handlers:
                handler.addFilter(cls.context.filter)

        else:
            for handler in cls.handlers:
                handler.removeFilter(cls.context.filter)

            cls.context.enable(False)

        if cls.is_using_format("%(pathname) %(filename) %(funcName) %(module)"):
            logging._srcfile = cls._logging_snapshot._srcfile

        else:
            logging._srcfile = None

        logging.logProcesses = cls.is_using_format("%(process)")
        logging.logThreads = cls.is_using_format("%(thread) %(threadName)")

        if not isinstance(logging.info, _LogWrap) and _getframe is not None:
            logging.critical = _LogWrap(logging.CRITICAL)
            logging.fatal = logging.critical
            logging.error = _LogWrap(logging.ERROR)
            logging.exception = _LogWrap(logging.ERROR, exc_info=True)
            logging.warning = _LogWrap(logging.WARNING)
            logging.info = _LogWrap(logging.INFO)
            logging.debug = _LogWrap(logging.DEBUG)
            logging.log = _LogWrap.log


class _LogWrap(object):
    """Allows to correctly report caller file/function/line from convenience calls such as logging.info()"""

    def __init__(self, level, exc_info=None):
        self.level = level
        self.exc_info = exc_info
        self.__doc__ = getattr(logging, logging.getLevelName(level).lower()).__doc__

    @staticmethod
    def log(level, msg, *args, **kwargs):
        offset = kwargs.pop("_stack_offset", 1)
        name = _getframe(offset).f_globals.get("__name__")
        logger = logging.getLogger(name)
        try:
            logging.currentframe = lambda: _getframe(3 + offset)
            logger.log(level, msg, *args, **kwargs)

        finally:
            logging.currentframe = ORIGINAL_CF

    def __call__(self, msg, *args, **kwargs):
        kwargs.setdefault("exc_info", self.exc_info)
        kwargs.setdefault("_stack_offset", 2)
        self.log(self.level, msg, *args, **kwargs)


def _replace_and_pad(fmt, marker, replacement):
    """
    Args:
        fmt (str): Format to tweak
        marker (str): Marker to replace
        replacement (str): What to replace marker with

    Returns:
        (str): Resulting format, with marker replaced
    """
    if marker not in fmt:
        return fmt

    if replacement:
        return fmt.replace(marker, replacement)

    # Remove mention of 'marker' in 'fmt', including leading space (if present)
    fmt = fmt.replace("%s " % marker, marker)
    return fmt.replace(marker, "")


def _canonical_format(fmt):
    """
    Args:
        fmt (str | None): Format specification

    Returns:
        (str | None): Canonical version of format
    """
    if not fmt:
        return fmt

    return _replace_and_pad(fmt, "%(timezone)s", LogManager.spec.timezone)


def _find_parent_folder(path, basenames):
    if not path or len(path) <= 3:
        return None

    dirpath, basename = os.path.split(path)
    if dirpath and basename:
        if basename and basename.lower() in basenames:
            return path

        return _find_parent_folder(dirpath, basenames)


def _format_recursive(key, value, definitions, max_depth):
    m = RE_FORMAT_MARKERS.search(value)
    if not m:
        return value

    if max_depth > 1 and value and "{" in value:
        try:
            value = value.format(**definitions)
            return _format_recursive(key, value, definitions, max_depth=max_depth - 1)

        except KeyError:
            pass

    return value


def _formatted_text(text, props, strict=False, max_depth=3):
    """
    Args:
        text (str): Text with '{...}' placeholders to be resolved
        props (dict): Available values

    Returns:
        (str): '{...}' placeholders resolved from given `props`
    """
    if not text:
        return text

    if text.startswith("~"):
        text = os.path.expanduser(text)

    if "{" not in text:
        return text

    definitions = {}
    markers = RE_FORMAT_MARKERS.findall(text)
    while markers:
        key = markers.pop()
        if key in definitions:
            continue

        val = props.get(key)
        if strict and val is None:
            return None

        val = stringified(val) if val is not None else "{%s}" % key
        markers.extend(m for m in RE_FORMAT_MARKERS.findall(val) if m not in definitions)
        definitions[key] = val

    if not max_depth or not isinstance(max_depth, int) or max_depth <= 0:
        return text

    result = dict((k, _format_recursive(k, v, definitions, max_depth)) for k, v in definitions.items())
    return text.format(**result)


def _get_fmt(handler):
    return handler and handler.formatter and handler.formatter._fmt


def _get_file_handler(location, rotate, rotate_count):
    """
    Args:
        location (str | None): Log file path
        rotate (str | None): How to rotate, examples:
            time:midnight - Rotate at midnight
            time:15s - Rotate every 15 seconds
            time:2h - Rotate every 2 hours
            time:7d - Rotate every 7 days
            size:20m - Rotate every 20MB
            size:1g - Rotate every 1MB
        rotate_count (int): How many backups to keep

    Returns:
        (logging.FileHandler): Associated handler
    """
    if not rotate:
        return logging.FileHandler(location)

    kind, _, mode = rotate.partition(":")

    if not mode:
        raise ValueError("Invalid 'rotate' (missing kind): %s" % rotate)

    if kind == "time":
        if mode == "midnight":
            return TimedRotatingFileHandler(location, when="midnight", backupCount=rotate_count)

        timed = "shd"
        if mode[-1].lower() not in timed:
            raise ValueError("Invalid 'rotate' (unknown time spec): %s" % rotate)

        interval = to_int(mode[:-1])
        if interval is None:
            raise ValueError("Invalid 'rotate' (time range not an int): %s" % rotate)

        return TimedRotatingFileHandler(location, when=mode[-1], interval=interval, backupCount=rotate_count)

    if kind == "size":
        size = to_bytesize(mode)
        if size is None:
            raise ValueError("Invalid 'rotate' (size not a bytesize): %s" % rotate)

        return RotatingFileHandler(location, maxBytes=size, backupCount=rotate_count)

    raise ValueError("Invalid 'rotate' (unknown type): %s" % rotate)


def _validated_project_path(*funcs):
    for func in funcs:
        path = func()
        if path:
            path = os.path.dirname(path)
            if os.path.exists(os.path.join(path, "setup.py")) or os.path.exists(os.path.join(path, "project.toml")):
                return path
