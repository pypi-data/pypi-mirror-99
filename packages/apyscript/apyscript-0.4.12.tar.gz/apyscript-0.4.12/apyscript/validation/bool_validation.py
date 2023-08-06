"""Boolean value's validation implementations.
"""

from typing import Any
from typing import Union


def validate_bool(value: Union[bool, Any]) -> None:
    """
    Validate specified value is bool or Boolean type.

    Parameters
    ----------
    value : bool or Boolean
        Boolean value to check.

    Raises
    ------
    ValueError
        If specified value isn't bool or Boolean type.
    """
    from apyscript.type import type_util
    is_bool: bool = type_util.is_bool(value=value)
    if is_bool:
        return
    raise ValueError(
        f'Specified value is not bool or Boolean type: {type(value)}')
