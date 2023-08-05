"""
Base functionality used by other parts of `runez`.

This class should not import any other `runez` class, to avoid circular deps.
"""

import inspect
import logging
import os
import re
import shutil
import sys
import threading


try:
    string_type = basestring  # noqa
    PY2 = True

    from StringIO import StringIO

except NameError:
    from io import StringIO

    string_type = str
    PY2 = False


LOG = logging.getLogger("runez")
SYMBOLIC_TMP = "<tmp>"
WINDOWS = sys.platform.startswith("win")
RE_SPACES = re.compile(r"[\s\n]+", re.MULTILINE)
_getframe = getattr(sys, "_getframe", None)


class Undefined(object):
    """Provides base type for `UNSET` below (representing an undefined value)

    Allows to distinguish between a caller not providing a value, vs providing `None`.
    This is needed in order to track whether a user actually provided a value (including `None`) as named argument.

    Example application is `runez.log.setup()`
    """

    def __repr__(self):
        return "UNSET"

    def __len__(self):
        # Ensures that Undefined instances evaluate as falsy
        return 0


# Internal marker for values that are NOT set
UNSET = Undefined()  # type: Undefined


def abort(message, code=1, exc_info=None, return_value=None, fatal=True, logger=UNSET):
    """General wrapper for optionally fatal calls

    >>> from runez import abort
    >>> abort("foo")  # Raises AbortException
    foo
    runez.system.AbortException: 1
    >>> abort("foo", fatal=True) # Raises AbortException
    foo
    runez.system.AbortException: 1
    >>> # Not fatal, but will log/print message:
    >>> abort("foo", return_value=False, fatal=False)  # Returns False
    foo
    False
    >>> abort("foo", fatal=False)  # Returns None
    foo
    >>> abort("foo", return_value=-1, fatal=False)  # Returns -1
    foo
    -1
    >>> # Not fatal, will not log/print any message:
    >>> abort("foo", fatal=None)  # Returns None
    >>> abort("foo", return_value=-1, fatal=None)  # Returns -1
    -1

    Args:
        message (str): Message explaining why we're aborting
        code (int): Exit code used when runez.system.AbortException is set to SystemExit
        exc_info (Exception): Exception info to pass on to logger
        return_value (Any): Value to return when `fatal` is not True
        fatal (type | bool | None): True: abort execution, False: don't abort but log, None: don't abort, don't log
        logger (callable | None): Logger to use, or None to disable log chatter

    Returns:
        Given `return_value`
    """
    if exc_info is not None:
        message = "%s: %s" % (message, exc_info)

    if logger is UNSET or logger is False:
        logger = LOG.error

    if fatal:
        exception = _R.abort_exception(override=fatal)
        if exception is SystemExit:  # Ensure message shown if we raise SystemExit
            _show_abort_message(message, exc_info, LOG.error)
            raise SystemExit(code)

        if isinstance(exception, type) and issubclass(exception, BaseException):
            _show_abort_message(message, exc_info, logger)
            raise exception(message)

    elif fatal is not None:
        _show_abort_message(message, exc_info, logger)

    return return_value


class cached_property(object):
    """
    A property that is only computed once per instance and then replaces itself with an ordinary attribute.
    Same as https://pypi.org/project/cached-property/ (without having to add another dependency).
    Deleting the attribute resets the property.

    Threads/async is not supported on purpose (to keep things simple)
    See docs/async-cached-property.md for how that can be added if/when needed.
    """

    def __init__(self, func):
        self.func = func
        self.__annotations__ = getattr(func, "__annotations__", None)
        self.__doc__ = func.__doc__
        self.__module__ = func.__module__
        self.__name__ = func.__name__

    def __get__(self, instance, owner):
        if instance is None:
            return self

        value = instance.__dict__[self.__name__] = self.func(instance)
        return value


class chill_property(cached_property):
    """
    Same as @cached_property, except the first 'not None' value yielded by the decorated function is used.

    This is useful to avoid repetitive code patterns such as this:

    @property
    def foo(self):
        value = f(...)
        if value is not None:
            return value

        value = g(...)
        if value is not None:
            return value
        ...

    The above becomes:

    @chill_property
    def foo(self):
        yield f(...) or None
        yield g(...)  # Tried only if preceding f() call returned a False-ish value
        ...
    """

    def __get__(self, instance, owner):
        if instance is None:
            return self

        for value in self.func(instance):
            if value is not None:
                instance.__dict__[self.func.__name__] = value
                return value


def decode(value, strip=None):
    """Python 2/3 friendly decoding of output.

    Args:
        value (str | bytes | None): The value to decode.
        strip (str | bool | None): If provided, `strip()` the returned string.

    Returns:
        str: Decoded value, if applicable.
    """
    if value is None:
        return None

    if isinstance(value, bytes):
        value = value.decode("utf-8")

    if strip:
        if strip is True:
            value = value.strip()

        else:
            value = value.strip(strip)

    return value


def find_caller_frame(validator=None, depth=2, maximum=1000):
    """
    Args:
        validator (callable): Function that will decide whether a frame is suitable, and return value of interest from it
        depth (int): Depth from top of stack where to start
        maximum (int | None): Maximum depth to scan

    Returns:
        (frame): First frame found
    """
    if _getframe is not None:
        if validator is None:
            validator = _is_actual_caller_frame

        while not maximum or depth <= maximum:
            try:
                f = _getframe(depth)
                value = validator(f)
                if value is not None:
                    return value

                depth = depth + 1

            except ValueError:
                return None


def first_line(text, keep_empty=False, default=None):
    """First line in 'data', if any

    Args:
        text (str | list | None): Text to examine
        keep_empty (bool): When False skip empty lines (+ strip spaces/newlines), when True don't filter (strip newlines only)
        default (str | None): Default to return if there was no first line

    Returns:
        (str | None): First line, if any
    """
    if text is None:
        return default

    if hasattr(text, "splitlines"):
        text = text.splitlines()

    for line in text:
        if keep_empty:
            return line.strip("\n")

        line = line.strip()
        if line:
            return line

    return default


def flattened(*value, **kwargs):
    """
    Args:
        value: Possibly nested arguments (sequence of lists, nested lists, ...)
        keep_empty (str | bool): States how to filter 'None' and/or False-ish values
                               - string: Replace `None` with given string, keep False-ish values as-is
                               - None: Filter out all False-ish values (including `None`)
                               - False: Filter out `None` values only (keep False-ish values as-is)
                               - True (default): No filtering, keep all values as-is
        split (str | None): If provided, split strings by given character
        shellify (bool): If True, filter out sequences of the form ["-f", None] (handy for simplified cmd line specification)
        unique (bool): If True, ensure every value appears only once

    Returns:
        (list): Flattened list from 'value'
    """
    keep_empty = kwargs.pop("keep_empty", True)
    split = kwargs.pop("split", None)
    shellify = kwargs.pop("shellify", False)
    unique = kwargs.pop("unique", False)
    if kwargs:
        raise TypeError("flattened() got unexpected keyword arguments %s" % kwargs)

    result = []
    _flatten(result, value, keep_empty, split, shellify, unique)
    return result


def get_version(mod, default="0.0.0", logger=LOG.warning):
    """
    Args:
        mod (module | str): Module, or module name to find version for (pass either calling module, or its .__name__)
        default (str): Value to return if version determination fails
        logger (callable | None): Logger to use to report inability to determine version

    Returns:
        (str): Determined version
    """
    name = mod
    if hasattr(mod, "__name__"):
        name = mod.__name__

    if not name:
        return default

    top_module_name = name
    last_exception = None
    try:
        import pkg_resources

        top_module_name = name.partition(".")[0]
        d = pkg_resources.get_distribution(top_module_name)
        if d and d.version:
            return d.version

    except Exception as e:
        last_exception = e

    try:
        m = sys.modules.get(name)
        if m is not None:
            v = getattr(m, "__version__", None)
            if not v:
                v = getattr(m, "VERSION", None)

            if v:
                return v

    except Exception as e:
        last_exception = e

    if logger and top_module_name != "tests":
        logger("Can't determine version for %s: %s", name, last_exception, exc_info=last_exception)

    return default


def is_basetype(value):
    """
    Returns:
        (bool): True if value is a base type
    """
    return isinstance(value, (int, float, string_type))


def is_iterable(value):
    """
    Returns:
        (bool): True if value is iterable (but NOT a string)
    """
    return isinstance(value, (list, tuple, set)) or inspect.isgenerator(value)


def python_version(components=2):
    """
    Returns:
        (str): Major.minor version of currently running python
    """
    return ".".join(str(v) for v in sys.version_info[:components])


def joined(*args, **kwargs):
    """
    >>> joined(1, None, 2)
    '1 None 2'
    >>> joined(1, None, 2, keep_empty=False)
    '1 2'

    Args:
        *args: Things to join
        delimiter (str): Delimiter to use (default: space character)
        keep_empty (str | bool): States how to filter 'None' and/or False-ish values
                               - string: Replace `None` with given string, keep False-ish values as-is
                               - None: Filter out all False-ish values (including `None`)
                               - False: Filter out `None` values only (keep False-ish values as-is)
                               - True (default): No filtering, keep all values as-is
        stringify (str): Function to use to stringify args (default: `stringified`)

    Returns:
        (str): Joined string
    """
    delimiter = kwargs.pop("delimiter", " ")
    keep_empty = kwargs.pop("keep_empty", True)
    stringify = kwargs.pop("stringify", stringified)
    if kwargs:
        raise TypeError("joined() got unexpected keyword arguments %s" % kwargs)

    args = flattened(args, keep_empty=keep_empty)
    return delimiter.join((stringify(x) for x in args))


def quoted(*items, **kwargs):
    """Quoted `items`, for those that contain whitespaces

    >>> quoted("foo")
    'foo'
    >>> quoted("foo bar")
    '"foo bar"'
    >>> quoted(["foo", "foo bar"])
    'foo "foo bar"'

    Args:
        items (str | list | tuple | None): Text, or list of text to optionally quote
        delimiter (str): Delimiter to use to join args back
        adapter (callable | None): Called for every item if provided, it should return a string
        keep_empty (str | bool): States how to filter 'None' and/or False-ish values
                               - string: Replace `None` with given string, keep False-ish values as-is
                               - None: Filter out all False-ish values (including `None`)
                               - False: Filter out `None` values only (keep False-ish values as-is)
                               - True (default): No filtering, keep all values as-is

    Returns:
        (str): Quoted if 'text' contains spaces
    """
    delimiter = kwargs.pop("delimiter", " ")
    adapter = kwargs.pop("adapter", UNSET)
    keep_empty = kwargs.pop("delimiter", True)
    if kwargs:
        raise TypeError("quoted() got unexpected keyword arguments %s" % kwargs)

    items = flattened(items, keep_empty=keep_empty)
    result = []
    for text in items:
        if adapter is UNSET:
            text = Anchored.short(stringified(text))

        elif callable(adapter):
            text = adapter(text)

        if text and " " in text:
            sep = "'" if '"' in text else '"'
            text = "%s%s%s" % (sep, text, sep)

        result.append(text)

    return delimiter.join(result)


def resolved_path(path, base=None):
    """
    Args:
        path (str | None): Path to resolve
        base (str | None): Base path to use to resolve relative paths (default: current working dir)

    Returns:
        (str): Absolute path
    """
    if not path or str(path).startswith(SYMBOLIC_TMP):
        return path

    path = os.path.expanduser(path)
    if base and not os.path.isabs(path):
        return os.path.join(resolved_path(base), path)

    return os.path.abspath(path)


def short(value, size=UNSET, none="None"):
    """
    Args:
        value: Value to textually represent in a shortened form
        size (int | Undefined | None): Max chars (default: terminal width if available, otherwise 180)
        none (str): String to use to represent `None`

    Returns:
        (str): Leading part of text, with at most 'size' chars (when specified)
    """
    text = stringified(value, converter=_prettified, none=none).strip()
    text = RE_SPACES.sub(" ", text)
    text = Anchored.short(text)
    if size is UNSET or isinstance(size, int) and size < 0:
        size = TERMINAL_INFO.columns

    if isinstance(size, int) and len(text) > size > 0:
        return "%s..." % text[:size - 3]

    return text


def stringified(value, converter=None, none="None"):
    """
    Args:
        value: Any object to turn into a string
        converter (callable | None): Optional converter to use for non-string objects
        none (str | bool | None): String to use to represent `None`

    Returns:
        (str): Ensure `text` is a string if necessary (this is to avoid transforming string types in py2 as much as possible)
    """
    if isinstance(value, string_type):
        return value

    if isinstance(value, bytes):
        return value.decode("utf-8")

    if converter is not None:
        converted = converter(value)
        if isinstance(converted, string_type):
            return converted

        if converted is not None:
            value = converted

    if value is None:
        if isinstance(none, string_type):
            return none

        if not none:
            return ""  # Represent `None` as empty string if `none` is False-ish

    return "{}".format(value)


class AbortException(Exception):
    """Raised when calls fail, in runez functions with argument `fatal=True`.

    You can replace this with your preferred exception, for example:

    >>> import runez
    >>> runez.system.AbortException = SystemExit
    """


class AdaptedProperty(object):
    """
    This decorator allows to define properties with regular get/set behavior,
    but the body of the decorated function can act as a validator, and can auto-convert given values

    Example usage:
        >>> from runez import AdaptedProperty
        >>> class MyObject:
        ...     age = AdaptedProperty(default=5)  # Anonymous property
        ...
        ...     @AdaptedProperty           # Simple adapted property
        ...     def width(self, value):
        ...         if value is not None:  # Implementation of this function acts as validator and adapter
        ...             return int(value)  # Here we turn value into an int (will raise exception if not possible)
        ...
        >>> my_object = MyObject()
        >>> assert my_object.age == 5  # Default value
        >>> my_object.width = "10"     # Implementation of decorated function turns this into an int
        >>> assert my_object.width == 10
    """

    __counter = [0]  # Simple counter for anonymous properties

    def __init__(self, validator=None, default=None, doc=None, caster=None, type=None):
        """
        Args:
            validator (callable | str | None): Function to use to validate/adapt passed values, or name of property
            default: Default value
            doc (str): Docstring (applies to anonymous properties only)
            caster (callable): Optional caster called for non-None values only (applies to anonymous properties only)
            type (type): Optional type, must have initializer with one argument if provided
        """
        self.default = default
        self.caster = caster
        self.type = type
        assert caster is None or type is None, "Can't accept both 'caster' and 'type' for AdaptedProperty, pick one"
        if callable(validator):
            # 'validator' is available when used as decorator of the form: @AdaptedProperty
            assert caster is None and type is None, "'caster' and 'type' are not applicable to AdaptedProperty decorator"
            self.validator = validator
            self.__doc__ = validator.__doc__
            self.key = "__%s" % validator.__name__

        else:
            # 'validator' is NOT available when decorator of this form is used: @AdaptedProperty(default=...)
            # or as an anonymous property form: my_prop = AdaptedProperty()
            self.validator = None
            self.__doc__ = doc
            if validator is None:
                i = self.__counter[0] = self.__counter[0] + 1
                validator = "anon_prop_%s" % i

            self.key = "__%s" % validator

    def __call__(self, validator):
        """Called when used as decorator of the form: @AdaptedProperty(default=...)"""
        assert self.caster is None and self.type is None, "'caster' and 'type' are not applicable to decorated properties"
        self.validator = validator
        self.__doc__ = validator.__doc__
        self.key = "__%s" % validator.__name__
        return self

    def __get__(self, instance, owner):
        if instance is None:
            return self  # We're being called by class

        return getattr(instance, self.key, self.default)

    def __set__(self, obj, value):
        if self.validator is not None:
            value = self.validator(obj, value)

        elif self.type is not None:
            if not isinstance(value, self.type):
                value = self.type(value)

        elif value is not None and self.caster is not None:
            value = self.caster(value)

        setattr(obj, self.key, value)


class Anchored(object):
    """
    An "anchor" is a known path that we don't wish to show in full when printing/logging
    This allows to conveniently shorten paths, and show more readable relative paths
    """

    _home = None
    _paths = []  # Currently stacked anchored folders that can be simplified away, via short()

    def __init__(self, *folders):
        self.folders = folders

    def __enter__(self):
        Anchored.add(self.folders)

    def __exit__(self, *_):
        Anchored.pop(self.folders)

    @classmethod
    def set(cls, *anchors):
        """
        Args:
            *anchors (str | list | tuple): Optional paths to use as anchors for short()
        """
        cls._paths = sorted((resolved_path(p) for p in flattened(anchors, keep_empty=False, unique=True)), reverse=True)

    @classmethod
    def add(cls, anchors):
        """
        Args:
            anchors (str | list | tuple): Optional paths to use as anchors for short()
        """
        cls.set(cls._paths, anchors)

    @classmethod
    def pop(cls, anchors):
        """
        Args:
            anchors (str | list | tuple): Optional paths to use as anchors for short()
        """
        for anchor in flattened(anchors, keep_empty=False, unique=True):
            anchor = resolved_path(anchor)
            if anchor in cls._paths:
                cls._paths.remove(anchor)

    @classmethod
    def short(cls, text):
        """
        Args:
            text (str): Text where to shorten paths

        Returns:
            (str): Short form, using '~' if applicable
        """
        if cls._home is None:
            cls._home = os.path.expanduser("~")

        if cls._paths:
            for p in cls._paths:
                if p:
                    text = text.replace(p + os.path.sep, "")

        return text.replace(cls._home, "~")


class CapturedStream(object):
    """Capture output to a stream by hijacking temporarily its write() function"""

    def __init__(self, name, target):
        self.name = name
        self.target = target
        self.buffer = StringIO()
        target_class = stringified(self.target.__class__).lower()
        self.capture_write = "_pytest" in target_class or "wrapper" in target_class
        if self.capture_write and self.target.write.__name__ == self.captured_write.__name__:
            self.capture_write = False

    def __repr__(self):
        return self.contents()

    def __contains__(self, item):
        return item is not None and item in self.contents()

    def __len__(self):
        return len(self.contents())

    def captured_write(self, message):
        self.buffer.write(message)

    def contents(self):
        """str: Contents of this capture"""
        return self.buffer.getvalue()

    def _start_capture(self):
        if self.capture_write:
            # setting sys.stdout doesn't survive with cross module fixtures, so we hijack its write the 1st time we see it
            self.original = self.target.write
            self.target.write = self.captured_write

        else:
            self.original = getattr(sys, self.name)
            setattr(sys, self.name, self.buffer)

    def _stop_capture(self):
        if self.capture_write:
            self.target.write = self.original

        else:
            setattr(sys, self.name, self.original)

    def assert_printed(self, expected):
        """Assert that 'expected' matches current output exactly (modulo trailing spaces/newlines), and clear current capture"""
        content = self.pop()
        assert content == expected

    def pop(self):
        """Current content popped, useful for testing"""
        r = self.contents()
        self.clear()
        return r.strip()

    def clear(self):
        """Clear captured content"""
        self.buffer.seek(0)
        self.buffer.truncate(0)


class CaptureOutput(object):
    """Output is captured and made available only for the duration of the context.

    Sample usage:

    >>> with CaptureOutput() as logged:
    >>>     print("foo bar")
    >>>     # output has been captured in `logged`, see `logged.stdout` etc
    >>>     assert "foo" in logged
    >>>     assert "bar" in logged.stdout
    """

    _capture_stack = []  # Shared across all objects, tracks possibly nested CaptureOutput buffers

    def __init__(self, stdout=True, stderr=True, anchors=None, dryrun=UNSET, seed_logging=False):
        """Context manager allowing to temporarily grab stdout/stderr/log output.

        Args:
            stdout (bool): Capture stdout?
            stderr (bool): Capture stderr?
            anchors (str | list | None): Optional paths to use as anchors for `runez.short()`
            dryrun (bool): Optionally override current dryrun setting
            seed_logging (bool): If True, ensure there is at least one logging handler configured
        """
        self.stdout = stdout
        self.stderr = stderr
        self.anchors = anchors
        self.dryrun = dryrun
        self.seed_logging = seed_logging
        self.handler = None

    @classmethod
    def current_capture_buffer(cls):
        if cls._capture_stack:
            return cls._capture_stack[-1].buffer

    def __enter__(self):
        """
        Returns:
            (TrackedOutput): Object holding captured stdout/stderr/log output
        """
        self.dryrun = _R.set_dryrun(self.dryrun)
        self.tracked = TrackedOutput(
            CapturedStream("stdout", sys.stdout) if self.stdout else None,
            CapturedStream("stderr", sys.stderr) if self.stderr else None,
        )

        for c in self.tracked.captured:
            c._start_capture()

        if self.tracked.captured:
            self._capture_stack.append(self.tracked.captured[-1])

        if self.anchors:
            Anchored.add(self.anchors)

        if self.seed_logging and not _has_stream_handler():
            # Define a logging handler, IsolatedLogSetup cleared them all
            self.handler = logging.StreamHandler(stream=self.tracked.captured[-1].buffer)
            self.handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
            self.handler.setLevel(logging.DEBUG)
            logging.root.addHandler(self.handler)

        return self.tracked

    def __exit__(self, *_):
        _R.set_dryrun(self.dryrun)
        if self.tracked.captured:
            self._capture_stack.pop()

        for c in self.tracked.captured:
            c._stop_capture()

        if self.handler:
            logging.root.handlers.remove(self.handler)

        if self.anchors:
            Anchored.pop(self.anchors)


class CurrentFolder(object):
    """Context manager for changing the current working directory"""

    def __init__(self, destination, anchor=False):
        self.anchor = anchor
        self.destination = resolved_path(destination)

    def __enter__(self):
        self.current_folder = os.getcwd()
        os.chdir(self.destination)
        if self.anchor:
            Anchored.add(self.destination)

    def __exit__(self, *_):
        os.chdir(self.current_folder)
        if self.anchor:
            Anchored.pop(self.destination)


class FallbackOp(object):
    def __init__(self, func, name=None, prepare=None):
        self.func = func
        self.name = name or "FallbackOp(%s)" % self.func
        self._prepare = prepare

    def __repr__(self):
        return self.name

    def run(self, *args, **kwargs):
        if self._prepare is not None:
            self._prepare()
            self._prepare = None

        return self.func(*args, **kwargs)


class FallbackChain(object):
    """Allows to have multiple ways of performing a given operation"""

    def __init__(self, *args, **kwargs):
        """
        Args:
            *args: Optional operations passed in positionally (will be used first)
            **kwargs: Optional additional named implementations (added in alphabetic order by key)
        """
        self.description = kwargs.pop("description", "fallback chain")
        self.logger = kwargs.pop("logger", None)
        self.current = None
        self.implementations = []
        self.available = []
        self.failed = []
        for arg in args:
            self.add_implementation(arg)

        for k in sorted(kwargs):
            self.add_implementation(kwargs[k], name=k)

    def __repr__(self):
        r = "[%s] %s (+%s)" % (self.description, self.current, len(self.available))
        if self.failed:
            r += ", failed: %s" % ", ".join(str(x) for x in self.failed)

        return r

    def __call__(self, *args, **kwargs):
        while self.available or self.current is not None:
            if self.current is None:
                self.current = self.available.pop(0)

            try:
                return self.current.run(*args, **kwargs)

            except Exception as e:
                self.failed.append(self.current)
                if self.logger:
                    self.logger("%s failed: %s" % (self.current, e))

                self.current = None

        raise Exception("Fallback chain exhausted for %s" % self.description)

    def add_implementation(self, run, name=None, prepare=None):
        if not isinstance(run, FallbackOp):
            if isinstance(run, dict):
                name = run.get("name", name)
                prepare = run.get("prepare", prepare)
                run = run.get("run")

            elif hasattr(run, "prepare"):
                name = getattr(run, "name", name)
                prepare = getattr(run, "prepare")
                run = getattr(run, "run", run)

            if name is None:
                name = getattr(run, "__name__", "FallbackOp(%s)" % run)

            run = FallbackOp(run, name=name, prepare=prepare)

        self.implementations.append(run)
        if self.current is None:
            self.current = run

        else:
            self.available.append(run)


class TrackedOutput(object):
    """Track captured output"""

    def __init__(self, stdout, stderr):
        """
        Args:
            stdout (CapturedStream | None): Captured stdout
            stderr (CapturedStream | None): Captured stderr
        """
        self.stdout = stdout
        self.stderr = stderr
        self.captured = [c for c in (self.stdout, self.stderr) if c is not None]

    def __repr__(self):
        return "\n".join("%s: %s" % (s.name, s) for s in self.captured)

    def __contains__(self, item):
        return any(item in s for s in self.captured)

    def __len__(self):
        return sum(len(s) for s in self.captured)

    def contents(self):
        return "".join(s.contents() for s in self.captured)

    def assert_printed(self, expected):
        """Assert that 'expected' matches current stdout exactly (modulo trailing spaces/newlines), and clear current capture"""
        self.stdout.assert_printed(expected)
        if self.stderr is not None:
            self.stderr.clear()

    def pop(self):
        """Current content popped, useful for testing"""
        r = self.contents()
        self.clear()
        return r.strip()

    def clear(self):
        """Clear captured content"""
        for s in self.captured:
            s.clear()


class Slotted(object):
    """This class allows to easily initialize/set a descendant using named arguments"""

    def __init__(self, *positionals, **kwargs):
        """
        Args:
            *positionals: Optionally provide positional objects to extract values from, when possible
            **kwargs: Override one or more of this classes' fields (keys must refer to valid slots)
        """
        self._seed()
        self.set(*positionals, **kwargs)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.represented_values())

    @classmethod
    def cast(cls, instance):
        """Cast `instance` to an instance of this type, via positional setter"""
        if isinstance(instance, cls):
            return instance

        return cls(instance)

    def represented_values(self, delimiter=", ", operator="=", none=False, name_formatter=None):
        """
        Args:
            delimiter (str): Delimiter used to separate field representation
            operator (str): Operator to represent assignment (equal sign '=' by default)
            none (bool): Include `None` values?
            name_formatter (callable | None): If provided, called to transform 'field' for each field=value pair

        Returns:
            (str): Textual representation of the form field=value
        """
        result = []
        for name in self.__slots__:
            value = getattr(self, name, UNSET)
            if value is not UNSET and (none or value is not None):
                if name_formatter is not None:
                    name = name_formatter(name)

                result.append("%s%s%s" % (name, operator, stringified(value, none=none)))

        return delimiter.join(result)

    def get(self, key, default=None):
        """This makes Slotted objects able to mimic dict get() function

        Args:
            key (str | None): Field name (on defined in __slots__)
            default: Default value to return if field is currently undefined (or UNSET)

        Returns:
            Value of field with 'key'
        """
        if key is not None:
            value = getattr(self, key, default)
            if value is not UNSET:
                return value

        return default

    def set(self, *positionals, **kwargs):
        """Conveniently set one or more fields at a time.

        Args:
            *positionals: Optionally set from other objects, available fields from the passed object are used in order
            **kwargs: Set from given key/value pairs (only names defined in __slots__ are used)
        """
        for positional in positionals:
            if positional is not UNSET:
                values = self._values_from_positional(positional)
                if values:
                    for k, v in values.items():
                        if v is not UNSET and kwargs.get(k) in (None, UNSET):
                            # Positionals take precedence over None and UNSET only
                            kwargs[k] = v

        for name in kwargs:
            self._set(name, kwargs.get(name, UNSET))

    def pop(self, settings):
        """
        Args:
            settings (dict): Dict to pop applicable fields from
        """
        if settings:
            for name in self.__slots__:
                self._set(name, settings.pop(name, UNSET))

    def to_dict(self):
        """dict: Key/value pairs of defined fields"""
        result = {}
        for name in self.__slots__:
            val = getattr(self, name, UNSET)
            if val is not UNSET:
                result[name] = val

        return result

    def __iter__(self):
        """Iterate over all defined values in this object"""
        for name in self.__slots__:
            val = getattr(self, name, UNSET)
            if val is not UNSET:
                yield val

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            for name in self.__slots__:
                if getattr(self, name, None) != getattr(other, name, None):
                    return False

            return True

    if PY2:

        def __cmp__(self, other):  # Applicable only for py2
            if isinstance(other, self.__class__):
                for name in self.__slots__:
                    i = cmp(getattr(self, name, None), getattr(other, name, None))  # noqa
                    if i != 0:
                        return i

                return 0

    def _seed(self):
        """Seed initial fields"""
        defaults = self._get_defaults()
        if not isinstance(defaults, dict):
            defaults = dict((k, defaults) for k in self.__slots__)

        for name in self.__slots__:
            value = getattr(self, name, defaults.get(name))
            setattr(self, name, value)

    def _set_field(self, name, value):
        setattr(self, name, value)

    def _get_defaults(self):
        """dict|Undefined|None: Optional defaults"""

    def _set(self, name, value):
        """
        Args:
            name (str): Name of slot to set.
            value: Associated value
        """
        if value is not UNSET:
            if isinstance(value, Slotted):
                current = getattr(self, name, UNSET)
                if current is None or current is UNSET:
                    current = value.__class__()
                    current.set(value)
                    setattr(self, name, current)
                    return

                if isinstance(current, Slotted):
                    current.set(value)
                    return

            setter = getattr(self, "set_%s" % name, None)
            if setter is not None:
                setter(value)

            else:
                self._set_field(name, value)

    def _values_from_positional(self, positional):
        """dict: Key/value pairs from a given position to set()"""
        if isinstance(positional, string_type):
            return self._values_from_string(positional)

        if isinstance(positional, dict):
            return positional

        if isinstance(positional, Slotted):
            return positional.to_dict()

        return self._values_from_object(positional)

    def _values_from_string(self, text):
        """dict: Optional hook to allow descendants to extract key/value pairs from a string"""

    def _values_from_object(self, obj):
        """dict: Optional hook to allow descendants to extract key/value pairs from an object"""
        if obj is not None:
            return dict((k, getattr(obj, k, UNSET)) for k in self.__slots__)


class TempArgv(object):
    """Context manager for changing the current sys.argv"""

    def __init__(self, args, exe=None):
        if exe is None:
            exe = sys.argv[0] if sys.argv and sys.argv[0] else sys.executable

        self.args = args
        self.exe = exe
        self.old_argv = sys.argv

    def __enter__(self):
        sys.argv = [self.exe] + self.args

    def __exit__(self, *_):
        sys.argv = self.old_argv


class TerminalInfo(object):
    """Info about current terminal"""

    @cached_property
    def columns(self):
        return self.size[0]

    @cached_property
    def lines(self):
        return self.size[1]

    @cached_property
    def size(self):
        """(int, int): Cached number of rows and columns of current terminal, if available"""
        return self.get_size()

    @cached_property
    def is_stdout_tty(self):
        """(bool): Is sys.stdout a tty?"""
        return self.isatty(sys.stdout)

    @cached_property
    def is_stderr_tty(self):
        """(bool): Is sys.stdout a tty?"""
        return self.isatty(sys.stderr)

    @staticmethod
    def isatty(channel):
        """True if we have a tty (or known equivalent), and are not running a test"""
        if channel.isatty() or "PYCHARM_HOSTED" in os.environ:
            return not _R.current_test()

    def padded_columns(self, padding=0, minimum=0):
        """
        Args:
            padding (int): Optional padding to add
            minimum (int): Minimum number of columns

        Returns:
            (int): Determined terminal width
        """
        return max(self.columns - padding, minimum)

    @staticmethod
    def get_columns():
        """
        Returns:
            (int | None): Current number of columns, determined dynamically
        """
        return _R.to_int(_R.program_output("tput", "cols", fatal=False, logger=None))

    @staticmethod
    def get_lines():
        """
        Returns:
            (int | None): Current number of lines, determined dynamically
        """
        return _R.to_int(_R.program_output("tput", "lines", fatal=False, logger=None))

    @staticmethod
    def get_size(default_columns=160, default_lines=25):
        """
        Returns:
            (int, int): Current number of rows and columns of current terminal, if available
        """
        cols = _R.to_int(os.environ.get("COLUMNS"))
        lines = _R.to_int(os.environ.get("LINES"))
        if not cols or not lines:
            try:
                size = shutil.get_terminal_size(fallback=(0, 0))
                cols = size.columns
                lines = size.lines

            except AttributeError:
                pass

        return cols or default_columns, lines or default_lines


TERMINAL_INFO = TerminalInfo()


class ThreadGlobalContext(object):
    """Thread-local + global context, composed of key/value pairs.

    Thread-local context is a dict per thread (stored in a threading.local()).
    Global context is a simple dict (applies to all threads).
    """

    def __init__(self, filter_type):
        """
        Args:
            filter_type (type): Class to instantiate as filter
        """
        self._filter_type = filter_type
        self._lock = threading.RLock()
        self._tpayload = None
        self._gpayload = None
        self.filter = None

    def reset(self):
        with self._lock:
            self.filter = None
            self._tpayload = None
            self._gpayload = None

    def enable(self, on):
        """Enable contextual logging"""
        with self._lock:
            if on:
                if self.filter is None:
                    self.filter = self._filter_type(self)
            else:
                self.filter = None

    def has_threadlocal(self):
        with self._lock:
            return bool(self._tpayload)

    def has_global(self):
        with self._lock:
            return bool(self._gpayload)

    def set_threadlocal(self, **values):
        """Set current thread's logging context to specified `values`"""
        with self._lock:
            self._ensure_threadlocal()
            self._tpayload.context = values

    def add_threadlocal(self, **values):
        """Add `values` to current thread's logging context"""
        with self._lock:
            self._ensure_threadlocal()
            self._tpayload.context.update(**values)

    def remove_threadlocal(self, name):
        """
        Args:
            name (str): Remove entry with `name` from current thread's context
        """
        with self._lock:
            if self._tpayload is not None:
                if name in self._tpayload.context:
                    del self._tpayload.context[name]
                if not self._tpayload.context:
                    self._tpayload = None

    def clear_threadlocal(self):
        """Clear current thread's context"""
        with self._lock:
            self._tpayload = None

    def set_global(self, **values):
        """Set global logging context to provided `values`"""
        with self._lock:
            self._ensure_global(values)

    def add_global(self, **values):
        """Add `values` to global logging context"""
        with self._lock:
            self._ensure_global()
            self._gpayload.update(**values)

    def remove_global(self, name):
        """
        Args:
            name (str): Remove entry with `name` from global context
        """
        with self._lock:
            if self._gpayload is not None:
                if name in self._gpayload:
                    del self._gpayload[name]
                if not self._gpayload:
                    self._gpayload = None

    def clear_global(self):
        """Clear global context"""
        with self._lock:
            if self._gpayload is not None:
                self._gpayload = None

    def to_dict(self):
        """dict: Combined global and thread-specific logging context"""
        with self._lock:
            result = {}
            if self._gpayload:
                result.update(self._gpayload)
            if self._tpayload:
                result.update(getattr(self._tpayload, "context", {}))
            return result

    def _ensure_threadlocal(self):
        if self._tpayload is None:
            self._tpayload = threading.local()
            self._tpayload.context = {}

    def _ensure_global(self, values=None):
        """
        Args:
            values (dict): Ensure internal global tracking dict is created, seed it with `values` when provided (Default value = None)
        """
        if self._gpayload is None:
            self._gpayload = values or {}


class _R:
    """
    Internal class to provide a late import of runez (after __init__ imported everything), and also holds some common stuff.
    The name is intentionally short to avoid verbose/long lines calling it.
    _R stands for "runez, internal class"

    This internal class allows to make global settings such as runez.DRYRUN usable internally:
    - without having to `import runez` internally (can't do that due to circular import)
    - respecting any external modifications clients may have done (like: runez.DRYRUN = foo)
    """

    _runez = None
    _schema = None

    @classmethod
    def _runez_module(cls):
        """Late-imported runez module"""
        if cls._runez is None:
            import runez

            cls._runez = runez

        return cls._runez

    @classmethod
    def program_output(cls, program, *args, **kwargs):
        r = cls._runez_module().run(program, *args, **kwargs)
        if r.succeeded:
            return r.output

    @classmethod
    def to_int(cls, text):
        return cls._runez_module().to_int(text)

    @staticmethod
    def _schema_type_name(target):
        meta = getattr(target, "meta", None)
        if meta is not None:
            return meta.name

        return target.__class__.__name__

    @classmethod
    def abort_exception(cls, override=None):
        """AbortException can be modified from client"""
        if isinstance(override, type) and issubclass(override, BaseException):
            return override

        return cls._runez_module().system.AbortException

    @classmethod
    def current_test(cls):
        return cls._runez_module().log.current_test()

    @classmethod
    def hdef(cls, default, logger, message, e=None):
        """Handle IO default

        Args:
            default (Any): The default value to return, if it is not UNSET
            logger (callable | None): Logger to use, False to log errors only, None to disable log chatter
            message (str): Message explaining failure
            e (Exception): Exception, if this comes from a try/except block

        Returns:
            'default', if it is not UNSET
        """
        if default is UNSET:
            abort(_actual_message(message), exc_info=e, logger=logger)

        if callable(default):
            default = default()

        cls.hlog(logger, message)
        return default

    @classmethod
    def hdry(cls, dryrun, logger, message):
        """Handle dryrun

        Args:
            logger (callable | None): Logger to use, or None to disable log chatter
            dryrun (bool): Optionally override current dryrun setting
            message (str | callable): Message to log

        Returns:
            (bool): True if we were indeed in dryrun mode, and we logged the message
        """
        if dryrun is UNSET:
            dryrun = cls.is_dryrun()

        if dryrun:
            if logger is not None:
                message = "Would %s" % _actual_message(message)
                if logger is False:
                    cls.trace(message)

                elif callable(logger):
                    logger(message)

                else:
                    print(message)

            return True

    @classmethod
    def hlog(cls, logger, message):
        """Handle optional logging calls via 'logger=' for IO-related non-returning-content functions, making them consistent.
        This allows to have less repeated code out there, find all places where we do this,
        and ensure they all respect the same convention.

        Args:
            logger (callable | None): Logger to use, or None to disable log chatter
            message (str | callable): Message to log
        """
        if logger is None:
            return

        if logger is False:
            return cls.trace(_actual_message(message))

        if logger is UNSET:
            logger = cls._runez_module().log.spec.default_logger

        if callable(logger):
            logger(_actual_message(message))

    @classmethod
    def is_dryrun(cls):
        """
        Returns:
            (bool): Same as runez.DRYRUN, but as a function (and with late import)
        """
        return cls._runez_module().DRYRUN

    @classmethod
    def schema(cls):
        """Late-imported schema"""
        if cls._schema is None:
            import runez.schema

            cls._schema = runez.schema

        return cls._schema

    @classmethod
    def serializable(cls):
        """Late-imported Serializable class"""
        return cls._runez_module().Serializable

    @classmethod
    def meta_description(cls, struct):
        """
        Args:
            struct (runez.schema.Struct): Associated Struct

        Returns:
            (runez.serialize.ClassMetaDescription): Meta object describing given 'struct'
        """
        return cls._runez_module().serialize.ClassMetaDescription(struct.__class__)

    @classmethod
    def set_dryrun(cls, dryrun):
        """Set runez.DRYRUN, and return its previous value (useful for context managers)

        Args:
            dryrun (bool | UNSET): New value for runez.DRYRUN

        Returns:
            (bool): Old values for dryrun
        """
        r = cls._runez_module()
        old_dryrun = r.DRYRUN
        if dryrun is not UNSET:
            r.DRYRUN = bool(dryrun)

        return old_dryrun

    @classmethod
    def trace(cls, message, *args, **kwargs):
        """
        Args:
            message (str): Message to trace
        """
        cls._runez_module().log.trace(message, *args, **kwargs)


def _actual_message(message):
    if callable(message):
        message = message()  # Allow message to be late-called function

    return message


def _flatten(result, value, keep_empty, split, shellify, unique):
    """
    keep_empty: string: replace None, None: filter out all False-ish, False: filter out `None` only, True (default): no filtering
    """
    if value is None or value is UNSET or (keep_empty is None and not value):
        if shellify:
            # Convenience: allow to filter out ["--switch", None] easily
            if result and result[-1].startswith("-"):
                result.pop(-1)

            return

        if keep_empty is None or (keep_empty is False and (value is None or value is UNSET)):
            return

        if isinstance(keep_empty, string_type):
            value = keep_empty

        if not unique or value not in result:
            result.append(value)

        return

    if is_iterable(value):
        for item in value:
            _flatten(result, item, keep_empty, split, shellify, unique)

        return

    if split and isinstance(value, string_type) and split in value:
        _flatten(result, value.split(split), keep_empty, split, shellify, unique)
        return

    if shellify:
        value = "%s" % value  # coerce to str() for py2

    if not unique or value not in result:
        result.append(value)


def _is_actual_caller_frame(f):
    """Return `f` if it's a frame that looks like coming from actual caller (not runez itself, or an internal library package)"""
    name = f.f_globals.get("__name__")
    if name and "__main__" in name:
        return f

    package = f.f_globals.get("__package__")
    if package and not package.startswith("_") and package.partition(".")[0] not in ("importlib", "pluggy", "runez"):
        return f


def _prettified(value):
    if isinstance(value, list):
        return "[%s]" % ", ".join(stringified(s, converter=_prettified) for s in value)

    if isinstance(value, tuple):
        return "(%s)" % ", ".join(stringified(s, converter=_prettified) for s in value)

    if isinstance(value, dict):
        keys = sorted(value, key=lambda x: "%s" % x)
        pairs = ("%s: %s" % (stringified(k, converter=_prettified), stringified(value[k], converter=_prettified)) for k in keys)
        return "{%s}" % ", ".join(pairs)

    if isinstance(value, set):
        return "{%s}" % ", ".join(stringified(s, converter=_prettified) for s in sorted(value, key=lambda x: "%s" % x))

    if isinstance(value, type):
        return "class %s.%s" % (value.__module__, value.__name__)

    if callable(value):
        return "function '%s'" % value.__name__


def _show_abort_message(message, exc_info, logger):
    if logging.root.handlers:
        if callable(logger):
            logger(message, exc_info=exc_info)

        else:
            _R.hlog(logger, message)

    else:
        sys.stderr.write("%s\n" % message)


def _has_stream_handler():
    for h in logging.root.handlers:
        if isinstance(h, logging.StreamHandler) or getattr(h, "isolation", None) == 0:
            return True
