"""Each types common value utilities.

Mainly following interfaces are defined:

- get_value_str_for_expression
    Get a value string for expression.
- get_copy
    Get a copy of specified instance if it is instance of CopyInterface.
"""

from typing import Any
from typing import List
from typing import TypeVar
from typing import Union

from apysc.type import Array


def get_value_str_for_expression(value: Any) -> str:
    """
    Get a value string for expression.

    Parameters
    ----------
    value : *
        Any value to convert to string.

    Returns
    -------
    value_str : str
        String for expression. If value is instance of
        VariableNameInterface, then variable's name will be returned,
        otherwise string casted value will be returned.
        Bool value will be lowercase (true or false) and str value
        will be quoted by double quotation.
        List or tuple value will be converted to js Array expression,
        e.g., '[10, "Hello!", true, any_variable]'.
    """
    from apysc.type.variable_name_interface import VariableNameInterface
    if isinstance(value, VariableNameInterface):
        return value.variable_name
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, str):
        return f'"{value}"'
    if isinstance(value, (list, tuple)):
        value_str: str = _get_value_str_from_iterable(value=value)
        return value_str
    return str(value)


def _get_value_str_from_iterable(value: Union[list, tuple, Array]) -> str:
    """
    Get value string from iterable object.

    Parameters
    ----------
    value : list or tuple or Array
        Target iterable object.

    Returns
    -------
    value_str : str
        Converted string, e.g., '[10, "Hello!", true, any_variable]'.
    """
    from apysc.type import Array
    from apysc.type.variable_name_interface import VariableNameInterface
    if isinstance(value, Array):
        value_: List[Any] = value.value  # type: ignore
    elif isinstance(value, tuple):
        value_ = list(value)
    else:
        value_ = value
    value_str: str = '['
    for unit_value in value_:
        if value_str != '[':
            value_str += ', '
        if isinstance(unit_value, VariableNameInterface):
            value_str += f'{unit_value.variable_name}'
            continue
        value_str += get_value_str_for_expression(value=unit_value)
    value_str += ']'
    return value_str


T = TypeVar('T')


def get_copy(value: T) -> T:
    """
    Get a copy of specified instance if it is instance of CopyInterface.

    Parameters
    ----------
    value : *
        Any value to copy.

    Returns
    -------
    copied : *
        Copied value. If value is not instance of CopyInterface,
        then argument value will be returned directly.
    """
    from apysc.type.copy_interface import CopyInterface
    if not isinstance(value, CopyInterface):
        return value
    return value._copy()
