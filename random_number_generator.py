from __future__ import annotations

from c_integer import CInt


class RandomNumberGenerator:
    _random_values = [
        CInt(1804289383), CInt(846930886),  CInt(1681692777), CInt(1714636915),
        CInt(1957747793), CInt(424238335),  CInt(719885386),  CInt(1649760492),
        CInt(596516649),  CInt(1189641421), CInt(1025202362), CInt(1350490027),
        CInt(783368690),  CInt(1102520059), CInt(2044897763), CInt(1967513926),
        CInt(1365180540), CInt(1540383426), CInt(304089172),  CInt(1303455736),
        CInt(35005211),   CInt(521595368)]

    def __init__(self, head: int = 0) -> None:
        self._head = head

    def __next__(self) -> CInt:
        value = self._random_values[self._head]
        self._head = (self._head + 1) % len(self._random_values)
        return value

    def __iter__(self) -> RandomNumberGenerator:
        return self

    def next(self) -> CInt:
        return self.__next__()

    def reset(self) -> None:
        self._head = 0
