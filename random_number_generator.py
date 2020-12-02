from __future__ import annotations

from clamped_int import ClampedInt


class RandomNumberGenerator:
    """A generator class. The random numbers here are pre-determined and presumably once upon a time, generated from a
    seed. In this implementation, the generator loops through the set of 22 pre-determined integers.

    Parameters
    ----------
    index: Optional[int]
        The index to start the `RandomNumberGenerator` on. Defaults to 0 (the start).

    Methods
    -------
    next()
        Starts the calculator and enters a blocking loop of waiting for and processing user input via the terminal.
    reset()
        Resets the index of the random number generator.
    """
    _random_values = [
        ClampedInt(1804289383), ClampedInt(846930886),  ClampedInt(1681692777), ClampedInt(1714636915),
        ClampedInt(1957747793), ClampedInt(424238335),  ClampedInt(719885386),  ClampedInt(1649760492),
        ClampedInt(596516649),  ClampedInt(1189641421), ClampedInt(1025202362), ClampedInt(1350490027),
        ClampedInt(783368690),  ClampedInt(1102520059), ClampedInt(2044897763), ClampedInt(1967513926),
        ClampedInt(1365180540), ClampedInt(1540383426), ClampedInt(304089172),  ClampedInt(1303455736),
        ClampedInt(35005211),   ClampedInt(521595368)]

    def __init__(self, index: int = 0) -> None:
        self._index = index

    def __next__(self) -> ClampedInt:
        """Yields the next random value."""
        value = self._random_values[self._index]
        self._index = (self._index + 1) % len(self._random_values)
        return value

    def __iter__(self) -> RandomNumberGenerator:
        """This method is implemented so you can use this class like an Iterator."""
        return self

    def next(self) -> ClampedInt:
        """Requests the generator to yield the next 'random' value."""
        return self.__next__()

    def reset(self) -> None:
        """Resets the index of the random number generator."""
        self._index = 0
