"""Type related common implementations.

Mainly following interface is defined:

- is_number
    Get a boolean value whether specified value is Number value.
- is_float_or_number
    Get a boolean value whether specified value is float or Nuber
    value.
- is_bool
    Get a boolean value whether specified value is bool or Boolean
    value.
- is_same_class_instance
    Get a boolean value whether specified class and instance's class
    are same or not.
"""

from typing import Any
from typing import Type


def is_number(value: Any) -> bool:
    """
    Get a boolean value whether specified value is Number value.

    Parameters
    ----------
    value : *
        Any value to check.

    Returns
    -------
    result : bool
        If Number value is specified, True will be returned.
    """
    from apysc.type import Number
    if isinstance(value, Number):
        return True
    return False


def is_float_or_number(value: Any) -> bool:
    """
    Get a boolean value whether specified value is float or Nuber
    value.

    Parameters
    ----------
    value : *
        Any value to check.

    Returns
    -------
    result : bool
        If float or Number value is specified, True will be returned.
    """
    if isinstance(value, float):
        return True
    if is_number(value=value):
        return True
    return False


def is_bool(value: Any) -> bool:
    """
    Get a boolean value whether specified value is bool or Boolean
    value.

    Parameters
    ----------
    value : *
        Any value to check.

    Returns
    -------
    result : bool
        If bool or Boolean value is specified, True will be returned.
    """
    if is_same_class_instance(class_=bool, instance=value):
        return True
    from apysc.type import Boolean
    if isinstance(value, Boolean):
        return True
    return False


def is_same_class_instance(class_: Type, instance: Any) -> bool:
    """
    Get a boolean value whether specified class and instance's class
    are same or not.

    Notes
    -----
    If instance is subclass of `cls` argument, differ from `isinstace`,
    then False will be returned.

    Parameters
    ----------
    class_ : Type
        Expected class.
    instance : *
        Intance to check it's class.

    Returns
    -------
    result : bool
        If a specified class and instance's class are same, then True
        will be set.
    """
    instance_type: Type = type(instance)  # type: ignore
    if instance_type == class_:
        return True
    return False
