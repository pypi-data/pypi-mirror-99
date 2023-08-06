"""Module for miscellaneous helper methods."""

import random
import string
import warnings

from ..exceptions import AmbiguousError


def random_string(length=4):
    """Generate a random string based on the length given.

    Keyword Arguments:
        length {int} -- The amount of the characters to generate (default: {4})

    Returns:
        string
    """
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(length)
    )


def dot(data, compile_to=None):
    notation_list = data.split(".")

    compiling = ""
    compiling += notation_list[0]
    beginning_string = compile_to.split("{1}")[0]
    compiling = beginning_string + compiling
    dot_split = compile_to.replace(beginning_string + "{1}", "").split("{.}")
    if any(len(x) > 1 for x in dot_split):
        raise ValueError("Cannot have multiple values between {1} and {.}")

    for notation in notation_list[1:]:
        compiling += dot_split[0]
        compiling += notation
        compiling += dot_split[1]
    return compiling


def clean_request_input(value, clean=True, quote=True):
    if not clean:
        return value

    import html

    try:
        if isinstance(value, str):
            return html.escape(value, quote=quote)
        elif isinstance(value, list):
            return [html.escape(x, quote=quote) for x in value]
        elif isinstance(value, int):
            return value
        elif isinstance(value, dict):
            return {key: html.escape(val, quote=quote) for (key, val) in value.items()}
    except (AttributeError, TypeError):
        pass

    return value


class HasColoredCommands:
    def success(self, message):
        print("\033[92m {0} \033[0m".format(message))

    def warning(self, message):
        print("\033[93m {0} \033[0m".format(message))

    def danger(self, message):
        print("\033[91m {0} \033[0m".format(message))

    def info(self, message):
        return self.success(message)


class Compact:
    def __new__(cls, *args):
        import inspect

        frame = inspect.currentframe()

        cls.dictionary = {}
        for arg in args:

            if isinstance(arg, dict):
                cls.dictionary.update(arg)
                continue

            found = []
            for key, value in frame.f_back.f_locals.items():
                if value == arg:
                    for f in found:
                        if value is f and f is not None:
                            raise AmbiguousError(
                                "Cannot contain variables with multiple of the same object in scope. "
                                "Getting {}".format(value)
                            )
                    cls.dictionary.update({key: value})
                    found.append(value)

        if len(args) != len(cls.dictionary):
            raise ValueError("Could not find all variables in this")
        return cls.dictionary


def deprecated(message):
    warnings.simplefilter("default", DeprecationWarning)

    def deprecated_decorator(func):
        def deprecated_func(*args, **kwargs):
            warnings.warn(
                "{} is a deprecated function. {}".format(func.__name__, message),
                category=DeprecationWarning,
                stacklevel=2,
            )
            return func(*args, **kwargs)

        return deprecated_func

    return deprecated_decorator
