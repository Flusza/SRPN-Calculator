from __future__ import annotations
import typing

from exceptions import DivideByZero, ModulusByZero, NegativePower


class CInt:
    """
    Base 10 implementation of a C type Integer.
    Clamps value between max and min values, denoted by `cls.max_value` & `cls.min_value`.
    """
    __slots__ = '_value'

    max_value = 2147483647
    min_value = -2147483648

    def __init__(self, value: typing.Union[int, CInt, float]) -> None:
        self.value = value

    @property
    def value(self) -> int:
        """returns the actual value as an integer held by this class."""
        return self._value

    @value.setter
    def value(self, v: int) -> None:
        """This setter ensures the value does not exceed the integer range specified by `max_value` & `min_value`.
        Raises `ValueError should type not be an int, CInt or float."""
        if not isinstance(v, (int, CInt, float)):
            raise ValueError('Inputted type is not an int.')
        self._value = int(max(CInt.min_value, min(CInt.max_value, v)))

    def __str__(self) -> str:
        """Returns a printable representation of the value."""
        return str(self.value)

    def __repr__(self) -> repr:
        """Similar to str function, but returns a more technical description of the class."""
        return repr(self.value)

    def __add__(self, other: CInt) -> CInt:
        """Returns the result from adding this CInt's value to the other CInt's value.
        this + other
        """
        new_value = self.value + other.value
        return CInt(new_value)

    def __sub__(self, other: CInt) -> CInt:
        """Returns the result from subtracting this CInt's value by the other CInt's value.
        this - other.
        """
        new_value = self.value - other.value
        return CInt(new_value)

    def __mul__(self, other: CInt) -> CInt:
        """Returns the multiplication product from this CInt's value and the other CInt's value.
        this * other.
        """
        new_value = self.value * other.value
        return CInt(new_value)

    def __truediv__(self, other: CInt) -> CInt:
        """CInt can't handle true division (with a remainder value).
        If called, process as a floor division instead (no remainder).
        """
        return self.__floordiv__(other)

    def __floordiv__(self, other: CInt) -> CInt:
        """Returns the whole number value when dividing this CInt's value by the other CInt's value.
        Remainder is ignored.
        this // other.
        """
        if other.value == 0:
            raise DivideByZero()

        new_value = self.value // other.value
        return CInt(new_value)

    def __mod__(self, other: CInt) -> CInt:
        """Returns the remainder from dividing this CInt's value by the other CInt's value.
        this % other.
        Raises `DivideByZero` should the denominator be == 0.
        """
        if other.value == 0:
            raise ModulusByZero()

        new_value = self.value % other.value
        return CInt(new_value)

    def __pow__(self, other: CInt) -> CInt:
        """Returns the resulting value after raising this CInt's value to the power denoted by the other CInt's value.
        this ^ other.
        Raises `NegativePower` should the other power be less than 0.
        """
        if other.value < 0:
            raise NegativePower()

        new_value = self.value ** other.value
        return CInt(new_value)

    # Equality functions. https://docs.python.org/3/reference/datamodel.html#object.__lt__
    def __eq__(self, other: CInt) -> bool:
        return self.value == other.value

    def __ne__(self, other: CInt) -> bool:
        return self.value != other.value

    def __lt__(self, other: CInt) -> bool:
        return self.value < other.value

    def __le__(self, other: CInt) -> bool:
        return self.value <= other.value

    def __gt__(self, other: CInt) -> bool:
        return self.value > other.value

    def __ge__(self, other: CInt) -> bool:
        return self.value >= other.value
