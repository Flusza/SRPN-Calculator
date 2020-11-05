from __future__ import annotations
import typing

from exceptions import DivideByZero, NegativePower


class CInt:
    """
    Base 10 implementation of a C type Integer.
    Clamps value between max and min.
    """
    __slots__ = '_value'

    max_value = 2147483647
    min_value = -2147483648

    def __init__(self, value: typing.Union[int, CInt, float]) -> None:
        """
        Will convert any input into an integer. Floats will be rounded.
        """
        self.value = value

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, v: int) -> None:
        self._value = int(max(CInt.min_value, min(CInt.max_value, v)))

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> repr:
        return repr(self.value)

    def __add__(self, other: CInt) -> CInt:
        new_value = self.value + other.value
        return CInt(new_value)

    def __sub__(self, other: CInt) -> CInt:
        new_value = self.value - other.value
        return CInt(new_value)

    def __mul__(self, other: CInt) -> CInt:
        new_value = self.value * other.value
        return CInt(new_value)

    def __truediv__(self, other: CInt) -> CInt:
        return self.__floordiv__(other)

    def __floordiv__(self, other: CInt) -> CInt:
        if other.value == 0:
            raise DivideByZero()

        new_value = self.value // other.value
        return CInt(new_value)

    def __mod__(self, other: CInt) -> CInt:
        if other.value == 0:
            raise DivideByZero()

        new_value = self.value % other.value
        return CInt(new_value)

    def __pow__(self, other: CInt) -> CInt:
        if other.value < 0:
            raise NegativePower()

        new_value = self.value ^ other.value
        return CInt(new_value)

    # Additional functionality
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