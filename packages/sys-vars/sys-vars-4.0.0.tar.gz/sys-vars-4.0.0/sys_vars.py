from datetime import datetime
import json
from os import environ
from pathlib import Path
from typing import Any, Optional, Union

__version__ = "3.0.0"
__all__ = [
    "get",
    "get_bool",
    "get_datetime",
    "get_float",
    "get_int",
    "get_json",
    "get_path",
    "SysVarNotFoundError",
]


# Allow a developer-defined Docker secrets path,
# defaulting to the Docker secrets Linux path
__SECRETS_PATH = Path(environ.get("SYS_VARS_PATH", "/run/secrets")).resolve()


class SysVarNotFoundError(Exception):
    """Custom-defined exception for unlocated system variables.

    Any time a system variable cannot be found in Docker secrets
    or os.environ, this Exception is raised."""

    pass


def get(key: str, *, default: Optional[Any] = None) -> str:
    """Get a system variable value as a str type.

    Check Docker secrets and os.environ for the key,
    preferring values from Docker secrets. If the key
    is not found and a default value is specified,
    the default value will be returned. Otherwise,
    SysVarNotFoundError will be raised.

    @param key - The system variable key.
    @param default - A default value is the key is not found.
    @return - The system variable value.
    """
    try:
        # Try to get a Docker secret value
        path = __SECRETS_PATH / key
        sys_var_value = path.read_text().strip() or None

    # The secret does not exist
    except FileNotFoundError:
        # Try to get it from the environment
        sys_var_value = environ.get(key)

    # The sys variable could not be loaded at all
    if sys_var_value is None:
        # A default value was specified, return it
        if default is not None:
            return default

        # No default value was given, raise an exception
        raise SysVarNotFoundError(f'Could not get value for system variable "{key}"')

    # A value for the key was found!
    return sys_var_value


def get_bool(key: str, **kwargs: dict) -> bool:
    """Get a system variable as a bool object.

    See signature of get() for parameter details."""
    # Start by getting the system value
    sys_val = get(key, **kwargs)

    # We have an actual boolean data type
    # (most likely a specified default value).
    # There's nothing we need to do for it
    if isinstance(sys_val, bool):
        return sys_val

    # We got a "word" string back, check if is an boolean word
    elif sys_val.isalpha():
        bool_strings = ("y", "yes", "t", "true")
        return sys_val.lower() in bool_strings

    # The sys val is mostly likely number, cast it
    # and check the truthy-ness of the resulting number
    else:
        sys_val = float(sys_val)
        return bool(sys_val)


def get_datetime(key: str, **kwargs: dict) -> datetime:
    """Get a system variable as a datetime.datetime object.

    The datestring is parsed using datetime.datetime.fromisoformat(),
    and as such, expects ISO 8601 strings written using
    date.isoformat() or datetime.isoformat().

    Raises ValueError if the data cannot be cast.

    See signature of get() for parameter details."""
    sys_val = get(key, **kwargs)

    # We have an actual datetime obj (most likely a default val)
    # There's nothing more to do
    if isinstance(sys_val, datetime):
        return sys_val
    return datetime.fromisoformat(sys_val)


def get_float(key: str, **kwargs: dict) -> float:
    """Get a system variable as a float value.

    Raises ValueError if the data cannot be cast.

    See signature of get() for parameter details."""
    return float(get(key, **kwargs))


def get_int(key: str, **kwargs: dict) -> int:
    """Get a system variable as an int value.

    Raises ValueError if the data cannot be cast.

    See signature of get() for parameter details."""
    return int(get(key, **kwargs))


def get_json(key: str, **kwargs: dict) -> Union[dict, list]:
    """Get a JSON string system variable as a dictionary object.

    Unlike the other methods whose names suggest the return data type
    of the system variable, this method refers to the type of data
    that is being retrieved. Because a raw JSON string is probably
    not too useful, the JSON string is automatically decoded into
    a Python dictionary or list for immediate consumption by the caller.
    This operates in a similar vein Flask's Request/Response get_json method.

    Raises json.JSONDecodeError if the JSON data cannot be decoded.

    See signature of get() for parameter details."""
    sys_val = get(key, **kwargs)

    # We have a dictionary or list (most likely a default val)
    # There's nothing more to do
    if isinstance(sys_val, dict) or isinstance(sys_val, list):
        return sys_val

    return json.loads(sys_val)


def get_path(key: str, **kwargs: dict) -> Path:
    """Get a file path string system variable as a pathlib.Path instance.

    See signature of get() for parameter details."""
    return Path(get(key, **kwargs))
