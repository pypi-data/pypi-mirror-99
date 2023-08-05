"""Class implementation for line style related interface.

See Also
--------
- graphics_clear_interface
"""

from typing import Union

from apyscript.color import color_util
from apyscript.converter import cast
from apyscript.type import Int
from apyscript.type import Number
from apyscript.type import String
from apyscript.type import value_util
from apyscript.type.number_value_interface import NumberValueInterface
from apyscript.validation import color_validation
from apyscript.validation import number_validation


class LineStyleInterface:

    _line_color: String
    _line_thickness: Int
    _line_alpha: Number

    def line_style(
            self, color: Union[str, String],
            thickness: Union[int, Int] = 1,
            alpha: Union[float, Number] = 1.0) -> None:
        """
        Set line style values.

        Parameters
        ----------
        color : str or String
            Hexadecimal color string. e.g., '#00aaff'
        thickness : int or Int, default 1
            Line thickness (minimum value is 1).
        alpha : float or Number, default 1.0
            Line color opacity (0.0 to 1.0).
        """
        if isinstance(color, String):
            color.value = color_util.complement_hex_color(
                hex_color_code=color.value)
        else:
            color = color_util.complement_hex_color(
                hex_color_code=color)
        self._line_color.value = color
        number_validation.validate_integer(integer=thickness)
        number_validation.validate_num_is_gt_zero(num=thickness)
        self._line_thickness = Int(thickness)
        number_validation.validate_num(num=alpha)
        if not isinstance(alpha, NumberValueInterface):
            alpha = cast.to_float_from_int(int_or_float=alpha)
            alpha = Number(alpha)
        color_validation.validate_alpha_range(alpha=alpha)
        self._line_alpha = alpha

    @property
    def line_color(self) -> String:
        """
        Get current line color.

        Returns
        -------
        line_color : String
            Current line color (hexadecimal string, e.g., '#00aaff').
            If not be set, blank string will be returned.
        """
        return self._line_color

    @property
    def line_thickness(self) -> Int:
        """
        Get current line thickness.

        Returns
        -------
        line_thickness : Int
            Current line thickness.
        """
        return self._line_thickness

    @property
    def line_alpha(self) -> Number:
        """
        Get current line color opacity.

        Returns
        -------
        line_alpha : Number
            Current line opacity (0.0 to 1.0).
            If not be set, None will be returned.
        """
        return value_util.get_copy(value=self._line_alpha)
