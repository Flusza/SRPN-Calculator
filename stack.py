from __future__ import annotations

import abc
import sys
import types
import typing

from clamped_int import ClampedInt
from exceptions import (
    StackOverflow,
    StackUnderflow,
    StackEmpty
)


class ABCStack(abc.ABC):
    """Represents the abstract data type: stack.
    Items can only be added (pushed) or removed (popped) to this stack from the top.

    Parameters
    ----------
    values: Optional[Iterable[stack_value_type]]
        A list of values to pre-populate the stack with.
    max_size: Optional[Int]
        The maximum number of items the stack can hold. Defaults to the value returned by sys.maxsize.
        This value should not be changed after instantiation, because this class does not have functionality to
        truncate the list of values to be under this limit should it change.
    """
    def __init__(self, values: typing.Iterable[stack_value_type] = None, max_size: int = None) -> None:
        self.max_size = max_size if max_size else sys.maxsize
        self._values = []
        if values:
            self.push_many(values)

    @property
    @abc.abstractmethod
    def stack_value_type(self):
        """This must be overridden as a class attribute in any subclass. Else `TypeError` will be raised."""
        pass

    def __next__(self) -> stack_value_type:
        """Keeps popping values from the top of the stack until no more values exist.
        `StopIteration` can be caught for when the stack empties."""
        try:
            return self.pop()
        except StackUnderflow:
            raise StopIteration()

    def __iter__(self) -> ABCStack:
        """This method is implemented so you can use this class like an Iterator."""
        return self

    def next(self) -> stack_value_type:
        """Requests the generator to yield the next value from the top of the stack.."""
        return self.__next__()

    def __len__(self) -> int:
        """Returns the number of items currently in the stack"""
        return len(self._values)

    def __str__(self) -> str:
        """Returns a string-like representation of the list of items in the stack"""
        return str(self._values)

    def __eq__(self, other: ABCStack) -> bool:
        """Returns True if the values and max_size in both stacks are the same. Otherwise False."""
        return self._values == other._values and self.max_size == other.max_size

    def __ne__(self, other: ABCStack) -> bool:
        """Returns True if the values or max_size in both stacks are different. Otherwise False."""
        return not self.__eq__(other)

    @property
    def is_empty(self) -> bool:
        """Returns True is the stack is currently empty. Otherwise False."""
        return True if self.count == 0 else False

    @property
    def is_full(self) -> bool:
        """Returns True if the stack is currently full"""
        return self.count >= self.max_size

    @property
    def count(self) -> int:
        """Returns as an integer, the number of values currently in the stack"""
        return len(self._values)

    def show(self) -> typing.List[stack_value_type]:
        """Returns a list of values contained in the Stack."""
        if self.is_empty:  # Pressing d before pushing anything to the stack, returns the lowest possible number.
            raise StackEmpty()

        return self._values

    def clear(self) -> None:
        """Remove all items from the stack."""
        if not self.is_empty:
            self._values = []

    def push(self, value: stack_value_type) -> None:
        """Push a single value to the top of the stack.
        Raises `ValueError` should the type not match that set in stack_value_type.
        Raises `StackOverflow` if the stack is already full.
        """
        if not isinstance(value, self.stack_value_type):
            raise ValueError(f'Value is not of type {self.stack_value_type}.')

        if self.count >= self.max_size:
            raise StackOverflow()

        self._values.append(value)

    def pop(self, index: int = -1) -> stack_value_type:
        """Removes and returns a single value from the top the stack.
        Index can be used to pop from a different place of the stack, however this isn't recommended.
        Raises `StackUnderflow` if the stack is empty.
        """
        if self.is_empty:
            raise StackUnderflow()

        return self._values.pop(index)

    def peek(self) -> stack_value_type:
        """Returns the top value from the stack
        Raises `StackEmpty` if the stack is empty.
        """
        if self.is_empty:
            raise StackEmpty()

        return self._values[-1]

    def push_many(self, values: typing.Iterable[stack_value_type]) -> None:
        """Same functionality as `push`, but for multiple values. Adds then sequentially."""
        if not isinstance(values, typing.Iterable):
            raise ValueError('Values should be an iterable')

        for value in values:
            self.push(value)

    def pop_many(self, n: int) -> typing.List[stack_value_type]:
        """Same functionality as `pop`, but for multiple values. Maintains their order."""
        if n > self.count:
            raise StackUnderflow()

        values = []
        for i in range(n):
            values.append(self.pop())
        return list(reversed(values))

    def peek_many(self, n: int) -> typing.List[stack_value_type]:
        """Same functionality as `peek`, but for multiple values. Maintains their order."""
        if n < 1:  # An integer less than 1 would return a value from the back of the stack. This shouldn't be possible.
            raise ValueError("Can't peek from back to front.")

        if n > self.count:  # Requesting to peek more items than exist.
            raise StackUnderflow()

        values = []
        for i in range(-1, -n - 1, -1):  # range(start, stop, step).
            values.insert(0, self._values[i])
        return values


class ClampedIntStack(ABCStack):
    """Represents a stack of CInts."""
    stack_value_type = ClampedInt

    def show(self) -> typing.List[stack_value_type]:
        """Returns a list of values contained in the Stack."""
        if self.is_empty:  # Override normal functionality to return the minimum value instead of raising `StackEmpty`.
            return [ClampedInt(ClampedInt.min_value), ]

        return self._values


class StringStack(ABCStack):
    """Used to represent a stack of strings."""
    stack_value_type = str

    def __next__(self) -> stack_value_type:
        """Unlike other stacks, we will allow iteration in this in reverse order through passing index=0 to pop().
        This is to allow parsing input the correct way around."""
        try:
            return self.pop(index=0)
        except StackUnderflow:
            raise StopIteration()


class OperatorStack(ABCStack):
    """Used to represent a stack of mathematical operators to execute"""
    stack_value_type = types.FunctionType
