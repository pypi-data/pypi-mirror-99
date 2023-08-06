from __future__ import print_function
try:
    import logging
except ModuleNotFoundError:
    raise RuntimeError(
        "Must install logging before using Zaraciccio's input module."
    )
import re
import sys

from os.path import abspath, join
try:
    from termcolor import colored
except ModuleNotFoundError:
    raise RuntimeError(
        "Must install termcolor before using Zaraciccio's input module."
    )
from traceback import format_exception


logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)

try:
    logging.root.handlers[0].formatter.formatException = lambda exc_info: _formatException(
        *exc_info
    )
except IndexError:
    pass

_logger = logging.getLogger("Zaraciccio")
_logger.setLevel(logging.DEBUG)

_logger.propagate = False

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s: %(message)s")
formatter.formatException = lambda exc_info: _formatException(*exc_info)
handler.setFormatter(formatter)
_logger.addHandler(handler)


class _flushfile():
    """
    Disable buffering for standard output and standard error.
    """

    def __init__(self, f):
        self.f = f

    def __getattr__(self, name):
        return object.__getattribute__(self.f, name)

    def write(self, x):
        self.f.write(x)
        self.f.flush()


sys.stderr = _flushfile(sys.stderr)
sys.stdout = _flushfile(sys.stdout)


def _formatException(type, value, tb):
    """
    Format traceback, darkening entries from global site-packages directories
    and user-specific site-packages directory.
    """

    packages = tuple(join(abspath(p), "") for p in sys.path[1:])
    lines = []
    for line in format_exception(type, value, tb):
        matches = re.search(r"^  File \"([^\"]+)\", line \d+, in .+", line)
        if matches and matches.group(1).startswith(packages):
            lines += line
        else:
            matches = re.search(r"^(\s*)(.*?)(\s*)$", line, re.DOTALL)
            lines.append(matches.group(
                1) + colored(matches.group(2), "yellow") + matches.group(3))
    return "".join(lines).rstrip()


sys.excepthook = lambda type, value, tb: print(
    _formatException(type, value, tb), file=sys.stderr)


def input_float(prompt):
    """
    Read a line of text from standard input and return the equivalent float
    as precisely as possible; if text does not represent a double, user is
    prompted to retry. If line can't be read, return None.
    """
    while True:
        s = input_string(prompt)
        if s is None:
            return None
        if len(s) > 0 and re.search(r"^[+-]?\d*(?:\.\d*)?$", s):
            try:
                return float(s)
            except (OverflowError, ValueError):
                pass


def input_int(prompt):
    """
    Read a line of text from standard input and return the equivalent int;
    if text does not represent an int, user is prompted to retry. If line
    can't be read, return None.
    """
    while True:
        s = input_string(prompt)
        if s is None:
            return None
        if re.search(r"^[+-]?\d+$", s):
            try:
                return int(s, 10)
            except ValueError:
                pass


def input_string(prompt):
    """
    Read a line of text from standard input and return it as a string,
    sans trailing line ending. Supports CR (\r), LF (\n), and CRLF (\r\n)
    as line endings. If user inputs only a line ending, returns "", not None.
    Returns None upon error or no input whatsoever (i.e., just EOF).
    """
    if type(prompt) is not str:
        raise TypeError("prompt must be of type str")
    try:
        return input(prompt)
    except EOFError:
        return None
