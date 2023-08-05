"""Class implementation for height interface.
"""

from apyscript.converter import cast
from apyscript.expression import expression_file_util
from apyscript.html import html_util
from apyscript.type import Int
from apyscript.type import value_util
from apyscript.type.variable_name_interface import VariableNameInterface
from apyscript.validation import size_validation


class HeightInterface(VariableNameInterface):

    _height: Int

    @property
    def height(self) -> Int:
        """
        Get this instance's height.

        Returns
        -------
        height : Int
            This instance's height.
        """
        return value_util.get_copy(value=self._height)

    @height.setter
    def height(self, value: Int) -> None:
        """
        Update this instance's height.

        Parameters
        ----------
        value : int
            Height value to set.
        """
        self.update_height_and_skip_appending_exp(value=value)
        self._append_height_update_expression()

    def _append_height_update_expression(self) -> None:
        """
        Append height updating expression.
        """
        expression: str = (
            f'{self.variable_name}.height({self.height});'
        )
        expression = html_util.wrap_expression_by_script_tag(
            expression=expression)
        expression_file_util.append_expression(
            expression=expression)

    def update_height_and_skip_appending_exp(self, value: Int) -> None:
        """
        Update height value and skip appending expression to file.

        Parameters
        ----------
        value : Int
            Height value to set.
        """
        value = cast.to_int_from_float(int_or_float=value)
        size_validation.validate_size_is_int(size=value)
        size_validation.validate_size_is_gte_zero(size=value)
        self._height = value
