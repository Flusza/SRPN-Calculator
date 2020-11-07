from __future__ import annotations

import sys

from c_integer import CInt
from random_number_generator import RandomNumberGenerator
from stack import CIntStack, OperatorStack, StringStack
from user_input import UserInput
from utility import is_digit, operator_map
from exceptions import (
    SRPNException,
    InvalidInput,
    ModulusByZero,
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
    """
    def __init__(self, max_stack_size: int = None, rng_index: int = 0) -> None:
        self._stack = CIntStack(max_size=max_stack_size)
        self._operator_stack = OperatorStack()
        self._rng = RandomNumberGenerator(index=rng_index)
        self._is_commenting = False  # Bool as to whether or not the user is currently writing comments using a '#'.
        print('You can now start interacting with the SRPN calculator')

    def __call__(self, string_input: str) -> None:
        """Called and handles the raw string input from command line."""
        try:
            user_input = UserInput(string_input)
            # We need to split the raw string up into elements. Group numbers >9 together and clean up white space.
            parsed_input = user_input.get_parsed_input()
            # Process the input now it is nicely split up.
            self._process_parsed_string(parsed_input)
        except SRPNException as e:  # Something unexpected has happened if the program reaches here.
            raise e

    def reset(self) -> None:
        """Resets any instance variables."""
        self._rng.reset()
        self._stack.clear()
        self._operator_stack.clear()
        self._is_commenting = False
        return

    def _process_parsed_string(self, parsed_string: StringStack) -> None:
        """Process an individual element that the user inputted."""
        # IMPORTANT NOTE! ----------------------------------------------------------------------------------------------
        # There is strange functionality when mathematical operators are chained together with no white space.
        # In any 'chain' of operators exists, the SRPN calculator executes them upon the next white space (or letter d).
        # It also doesn't execute them in the same order. It does them in reverse
        # (likely achieved through popping off the top of the stack, which will naturally do this).
        # Furthermore, if an equals is in the chain, they are processed immediately, and the operations follow after.
        # Therefore we need to store what operators we have encountered to execute them afterwards.
        # --------------------------------------------------------------------------------------------------------------
        previous_string = ' '
        current_string = ' '
        for next_string in parsed_string:
            try:
                if current_string == '#':
                    if previous_string == ' ' and next_string == ' ':
                        # A hashtag surrounded by white space or at start/end of a line will toggle commenting mode.
                        self._is_commenting = not self._is_commenting
                        continue
                    else:
                        raise InvalidInput(current_string)

                if self._is_commenting:
                    pass  # If we are commenting, we can ignore the input.

                elif current_string == ' ':
                    pass  # Do nothing and don't raise an error.

                elif is_digit(current_string):
                    self._stack.push(CInt(int(current_string)))

                elif current_string == '=':
                    print(self._stack.peek())

                elif current_string == 'r':  # User wants a 'random' number. Generate one and push it onto the stack.
                    if self._stack.is_full:  # We will only generate a random number if the stack isn't full.
                        raise StackOverflow()
                    self._stack.push(self._rng.next())

                elif current_string == 'd':  # Display all the elements on the stack line by line.
                    for item in self._stack.show():
                        print(item)

                elif operator := operator_map.get(current_string):  # User inputted a mathematical symbol.
                    self._operator_stack.push(operator)

                else:  # If input reaches here, we can ignore it and make the user aware with this error.
                    raise InvalidInput(current_string)

            except (StackException, InvalidInput) as e:
                # Any user caused errors should not cause the program to crash.
                # We will simply print the error to the terminal to make the user aware.
                print(e)
            finally:
                # End of each element, check if conditions are right to run the operator chain.
                if len(self._operator_stack) > 0 and next_string in (' ', 'd'):
                    self._execute_operator_stack()

                # Update variables for the next iteration.
                previous_string = current_string
                current_string = next_string

    def _execute_operator_stack(self) -> None:
        """Check if conditions are right to execute a chain of operators.
        Chains are created through a chain of operators and equal signs.
        """
        try:
            for operator in self._operator_stack:
                self._process_operator(operator)
        except StackException as e:
            print(e)

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
            if isinstance(e, ModulusByZero):  # The SRPN calculator we're replicating crashes when doing modulus 0.
                sys.exit(0)
