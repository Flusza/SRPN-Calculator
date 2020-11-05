import sys
import typing

from c_integer import CInt
from exceptions import (
    StackOverflow,
    StackUnderflow,
    StackEmpty
)


class Stack:
    def __init__(self, values: typing.Iterable[CInt] = None, max_size: int = None) -> None:
        self._max_size = max_size if max_size else sys.maxsize
        self._values = []

        if values:
            self.push_many(values)

    def __len__(self) -> int:
        return len(self._values)

    def __str__(self) -> str:
        return str(self._values)

    @property
    def is_empty(self) -> bool:
        return True if self.count == 0 else False

    @property
    def count(self) -> int:
        return len(self._values)

    @property
    def is_full(self) -> bool:
        return self.count >= self._max_size

    def show(self) -> typing.List[CInt]:
        # Pressing d before anything is pressed to stack, returns the lowest possible number.
        if self.is_empty:
            return [CInt(CInt.min_value),]

        return self._values

    def clear(self) -> None:
        if not self.is_empty:
            self._values = []

    def push(self, value: CInt) -> None:
        if not isinstance(value, CInt):
            raise ValueError('Value is not a CInt')

        if self.count >= self._max_size:
            raise StackOverflow()

        self._values.append(value)

    def pop(self) -> CInt:
        if self.is_empty:
            raise StackUnderflow()

        return self._values.pop(-1)

    def peek(self) -> CInt:
        if self.is_empty:
            raise StackEmpty()

        return self._values[-1]

    def push_many(self, values: typing.Iterable[CInt]) -> None:
        if not isinstance(values, typing.Iterable):
            raise ValueError('Values should be an iterable')

        for value in values:
            self.push(value)

    def pop_many(self, n: int) -> typing.List[CInt]:
        if n > self.count:
            raise StackUnderflow()

        values = []
        for i in range(n):
            values.append(self.pop())
        return list(reversed(values))

    def peek_many(self, n: int) -> typing.List[CInt]:
        if n < 1:
            raise ValueError("Can't peek from back to front.")

        if n > self.count:
            raise StackUnderflow()

        values = []
        for i in range(-1, -n -1, -1):
            values.append(self._values[i])
        return list(reversed(values))
