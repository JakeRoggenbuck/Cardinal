"""Provides a decorator which logs all requests to a log file."""

from datetime import datetime
from os import path

_FILE_PATH = "request_log.txt"

"""THE MAIN DECORATOR
Please look up how decorators work, but in essence:
@decorator
def function():
  # code
is equivalent to:
def function():
  # code
function = decorator(function)
This decorator is applied to every get operation so that each one has
logging code inserted.
"""


def request_logged(fn):
    def new_fn(cself, request, *args, **kwargs):
        logger(cself, request, fn, *args, **kwargs)
        return fn(cself, request, *args, **kwargs)

    return new_fn


# THE LOGGER
# Takes in the arguments and the function and spits out some logging info
def logger(cself, request, fn, *args, **kwargs):
    log_file = open(_FILE_PATH, "a")
    # So (classname).get
    name = fn.__qualname__
    # (classname).get -> ['classname', 'get'] -> 'classname'
    calling_class = name.split(".")[0]
    args_string = (
        "\n".join(("\t" + str(arg)) for arg in args) + "\n" if len(args) != 0 else "[no arguments]"
    )
    kwargs_string = (
        "\n".join(("\t" + f"{arg} : '{str(kwargs[arg])}'") for arg in kwargs.keys()) + "\n"
        if len(kwargs.keys()) != 0
        else "[no arguments]"
    )
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    log_file.write(
        f"""Date: {timestamp}
Request type: {calling_class}
Arguments: {args_string}
Keyword arguments: {kwargs_string}
Query params:
    {request.query_params}

"""
    )
    log_file.close()
