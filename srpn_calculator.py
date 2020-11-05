from __future__ import annotations

from c_integer import CInt
from random_number_generator import RandomNumberGenerator
from stack import Stack
from user_input import UserInput
from utility import operator_map
from exceptions import (
    SRPNException,
    InvalidInput,
    StackException,
    OperatorException,
    StackOverflow
)


class SRPNCalculator:
    def __init__(self, max_stack_size: int = None, rng_head: int = 0) -> None:
        self.stack = Stack(max_size=max_stack_size)
        self.rng = RandomNumberGenerator(head=rng_head)

        self._running = False
        self._is_commenting = False

    def start(self) -> None:
        if self._running:
            raise RuntimeError('Calculator is already running!')

        print('You can now start interacting with the SRPN calculator')
        self._running = True
        self._loop()

    def stop(self) -> None:
        self.rng.reset()
        self.stack.clear()
        self._running = False

    def _loop(self) -> None:
        try:
            while self._running:
                user_input = self._get_input()
                parsed_input = user_input.get_parsed_input()

                # Multiline comments are allowed in the calculator.
                # We must store between inputs whether the last line was in the process of commenting or not.
                self._is_commenting = user_input.is_commenting

                for element in parsed_input:
                    self._process_element(element)

        except KeyboardInterrupt:
            self.stop()

        except SRPNException as e:
            self.stop()
            raise e

    def _get_input(self) -> UserInput:
        return UserInput(input(), is_commenting=self._is_commenting)

    def _process_element(self, element: str) -> None:
        try:
            if element.isdigit():
                self.stack.push(CInt(int(element)))

            elif operator := operator_map.get(element):
                self._process_operator(operator)

            elif element == 'r':
                if self.stack.is_full:
                    raise StackOverflow()

                self.stack.push(self.rng.next())

            elif element == '=':
                print(self.stack.peek())

            elif element == 'd':
                for item in self.stack.show():
                    print(item)

            else:
                raise InvalidInput(element)

        except (StackException, InvalidInput) as e:
            print(e)

    def _process_operator(self, operator: callable) -> None:
        n1, n2 = self.stack.pop_many(2)

        try:
            self.stack.push(operator(n1, n2))

        except OperatorException as e:
            print(e)

            # If an error occurs during the operation, push the two CInts popped off the stack back on it.
            self.stack.push_many((n1, n2))
