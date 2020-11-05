from __future__ import annotations

from c_integer import CInt


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
        CInt(1804289383), CInt(846930886),  CInt(1681692777), CInt(1714636915),
        CInt(1957747793), CInt(424238335),  CInt(719885386),  CInt(1649760492),
        CInt(596516649),  CInt(1189641421), CInt(1025202362), CInt(1350490027),
        CInt(783368690),  CInt(1102520059), CInt(2044897763), CInt(1967513926),
        CInt(1365180540), CInt(1540383426), CInt(304089172),  CInt(1303455736),
        CInt(35005211),   CInt(521595368)]

    def __init__(self, index: int = 0) -> None:
        self._index = index

    def __next__(self) -> CInt:
        """Yields the next random value."""
        value = self._random_values[self._index]
        self._index = (self._index + 1) % len(self._random_values)
        return value

    def __iter__(self) -> RandomNumberGenerator:
        """This method is implemented so you can use this class like an Iterator."""
        return self

    def next(self) -> CInt:
        """Requests the generator to yield the next 'random' value."""
        return self.__next__()

    def reset(self) -> None:
        """Resets the index of the random number generator."""
        self._index = 0
