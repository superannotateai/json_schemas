# -*- test-case-name: twisted.test.test_reflect -*-
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
Standardized versions of various cool and/or strange things that you can do
with Python's reflection capabilities.
"""

import sys


class _NoModuleFound(Exception):
    """
    No module was found because none exists.
    """


class InvalidName(ValueError):
    """
    The given name is not a dot-separated list of Python objects.
    """


class ModuleNotFound(InvalidName):
    """
    The module associated with the given name doesn't exist and it can't be
    imported.
    """


class ObjectNotFound(InvalidName):
    """
    The object associated with the given name doesn't exist and it can't be
    imported.
    """


def reraise(exception, traceback):
    raise exception.with_traceback(traceback)


reraise.__doc__ = """
Re-raise an exception, with an optional traceback, in a way that is compatible
with both Python 2 and Python 3.

Note that on Python 3, re-raised exceptions will be mutated, with their
C{__traceback__} attribute being set.

@param exception: The exception instance.
@param traceback: The traceback to use, or C{None} indicating a new traceback.
"""


def _importAndCheckStack(importName):
    """
    Import the given name as a module, then walk the stack to determine whether
    the failure was the module not existing, or some code in the module (for
    example a dependent import) failing.  This can be helpful to determine
    whether any actual application code was run.  For example, to distiguish
    administrative error (entering the wrong module name), from programmer
    error (writing buggy code in a module that fails to import).

    @param importName: The name of the module to import.
    @type importName: C{str}
    @raise Exception: if something bad happens.  This can be any type of
        exception, since nobody knows what loading some arbitrary code might
        do.
    @raise _NoModuleFound: if no module was found.
    """
    try:
        return __import__(importName)
    except ImportError:
        excType, excValue, excTraceback = sys.exc_info()
        while excTraceback:
            execName = excTraceback.tb_frame.f_globals["__name__"]
            # in Python 2 execName is None when an ImportError is encountered,
            # where in Python 3 execName is equal to the importName.
            if execName is None or execName == importName:
                reraise(excValue, excTraceback)
            excTraceback = excTraceback.tb_next
        raise _NoModuleFound()


