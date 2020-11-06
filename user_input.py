import typing
from stack import StringStack


class UserInput:
    """
    A class used to represent a line of input from the terminal.
    Has functionality to split (parse) the input into individual elements (numbers, operators and letters).

    Parameters
    ----------
    raw_input: str
        The raw string which was entered by the user into the terminal.
    """
    def __init__(self, raw_input: str) -> None:
        self._raw_string = raw_input  # The raw string that was entered by the user into the terminal.
        self._parsed_stack = StringStack()  # Individual elements extracted from the raw input string.
        self.parsed = False  # Bool whether or not the raw_input has been parsed into individual elements already.

    def __repr__(self) -> repr:
        """A """
        if self.parsed:
            return repr(f"Parsed Elements<{self._parsed_stack}>")
        return repr(f"Unparsed String<{self._raw_string}>")

    def get_parsed_input(self) -> StringStack:
        """Returns the list of parsed_elements extracted from the raw_input string."""
        if self.parsed:  # If already parsed, don't do this again unnecessarily.
            return self._parsed_stack

        # At this point, _parse() hasn't been called yet. Parse and then return.
        return self._parse()

    def _parse(self) -> StringStack:
        """Handles all the logic necessary for splitting up the raw string. The string is split up into elements.
        Elements which are stored in the parsed_elements list:
            - A single (<10) or series of digits (>10), forming one integer.
            - A single letter or symbol.
            - All white space represented as ' '.
        Returns the list of parsed elements.
            """
        number_construct = ''
        self._parsed_stack.push(' ')  # Append white space to start and end of input to make processing simpler later.
        for next_char in self._raw_string:
            if next_char.isdigit():
                # A number could be more than one digit, so we can't treat them as a single char.
                number_construct += next_char
                continue

            elif next_char.isspace():
                if number_construct != '':  # Also could denote end of a number
                    self._parsed_stack.push(number_construct)
                    number_construct = ''
                self._parsed_stack.push(' ')
                continue

            else:  # Is any other character.
                if number_construct != '':  # Also could denote end of a number
                    self._parsed_stack.push(number_construct)
                    number_construct = ''
                self._parsed_stack.push(next_char)

        if number_construct != '':
            # Now we have reached the end of the inputted line; add any outstanding number to the _parsed_elements list.
            self._parsed_stack.push(number_construct)
        self._parsed_stack.push(' ')

        self.parsed = True
        return self._parsed_stack
