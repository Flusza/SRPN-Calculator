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
    """
    A class used to represent the command line saturated reverse polish notation (SRPN) calculator.
    When running, the class will wait for user input via the command line and process it accordingly.

    Parameters
    ----------
    max_stack_size: Optional[int]
        The maximum number of elements the `Stack` can hold.
    rng_index: Optional[int]
        The index to start the `RandomNumberGenerator` on. Defaults to 0 (the start).

    Methods
    -------
    start()
        Starts the calculator and enters a blocking loop of waiting for and processing user input via the terminal.
    stop()
        Silently stops the calculator on the next iteration of the loop.
    """
    def __init__(self, max_stack_size: int = None, rng_index: int = 0) -> None:
        self._stack = Stack(max_size=max_stack_size)
        self._rng = RandomNumberGenerator(index=rng_index)
        self._is_commenting = False  # Bool as to whether or not the user is currently writing comments using a '#'.
        self._running = False  # Bool as to whether or not the calculator is currently running.

    def start(self) -> None:
        if self._running:  # Checks if this instance is already running. Raise if so.
            raise RuntimeError('Calculator is already running!')

        print('You can now start interacting with the SRPN calculator')
        self._running = True
        self._loop()  # Enter blocking running loop.

    def stop(self) -> None:
        """When called, silently stops the calculator and resets any instance variables in case it is started again."""
        self._running = False
        self._rng.reset()
        self._stack.clear()
        self._is_commenting = False
        return

    def _loop(self) -> None:
        """A loop which continues to wait for and process user input."""
        try:
            while self._running:
                user_input = self._get_input()  # Wait for input from user.
                # Parse input, splitting up different commands or numbers into individual elements in a list.
                parsed_input = user_input.get_parsed_input()

                # Multiline comments are allowed in the calculator.
                # We must store between inputs whether the last line was in the process of commenting or not.
                self._is_commenting = user_input.is_commenting

                for element in parsed_input:
                    self._process_element(element)

        except KeyboardInterrupt:
            self.stop()

        except SRPNException as e:  # Something unexpected has happened if the program reaches here.
            self.stop()
            raise e

    def _get_input(self) -> UserInput:
        """Waits here for input via the terminal and encapsulates it in the the UserInput class."""
        return UserInput(input(), is_commenting=self._is_commenting)

    def _process_element(self, element: str) -> None:
        """Process an individual element that the user inputted."""
        try:
            if element.isdigit():  # User inputted a number. Push it onto the stack.
                self._stack.push(CInt(int(element)))

            elif operator := operator_map.get(element):  # User inputted a mathematical symbol.
                self._process_operator(operator)

            elif element == 'r':  # User wants a 'random' number. Generate one and push it onto the stack.
                if self._stack.is_full:  # We will only generate a random number if the stack isn't full.
                    raise StackOverflow()
                self._stack.push(self._rng.next())

            elif element == '=':  # User wants to see the top item in the stack.
                print(self._stack.peek())

            elif element == 'd':  # Display all the elements on the stack line by line.
                for item in self._stack.show():
                    print(item)

            else:  # If input reaches here, we can ignore it and make the user aware with this error.
                raise InvalidInput(element)

        except (StackException, InvalidInput) as e:
            # Any user caused errors should not cause the program to crash.
            # We will simply print the error to the terminal to make the user aware.
            print(e)
            return

    def _process_operator(self, operator: callable) -> None:
        """More specifically over processing an individual element, this processes a specific mathematical operator."""
        n1, n2 = self._stack.pop_many(2)  # Take the top two elements off the stack and apply the operator to them.
        try:
            self._stack.push(operator(n1, n2))
        except OperatorException as e:
            # Any mathematical error should not crash the program.
            # However, we will print what went wrong to terminal to make user aware.
            print(e)
            self._stack.push_many((n1, n2))

