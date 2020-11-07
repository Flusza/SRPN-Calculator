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
            - A single (<10) or series of digits (>10), forming one integer. Can also include a negative
              (which could also mean subtraction).
            - A single letter or mathematical symbol.
            - All white space represented as ' '.
        Returns the list of parsed elements.
            """
        number_construct = ''
        # We will use this variable to determine if a number is negative or if it is just a subtraction sign
        negative_val = False
        self._parsed_stack.push(' ')  # Append white space to start and end of input to make processing simpler later.
        for next_char in self._raw_string:
            if next_char == '-':  # Could be a negative number or a minus.
                if number_construct == '':  # No number in the making
                    if negative_val:
                        self._parsed_stack.push('-')
                    else:
                        negative_val = True
                else:  # is a number in the making
                    number_construct, negative_val = self._number_termination(number_construct, negative_val)
                    negative_val = True

            elif next_char.isdigit():
                # A number could be more than one digit, so we can't treat them as a single char.
                number_construct += next_char

            elif next_char.isspace():
                if number_construct == '':  # No number in the making
                    if negative_val:
                        self._parsed_stack.push('-')
                    negative_val = False
                else:  # Number in the making
                    number_construct, negative_val = self._number_termination(number_construct, negative_val)
                self._parsed_stack.push(' ')

            else:  # Is any other character.
                if number_construct == '':  # Also could denote end of a number
                    if negative_val:
                        self._parsed_stack.push('-')
                    negative_val = False
                else:
                    number_construct, negative_val = self._number_termination(number_construct, negative_val)
                self._parsed_stack.push(next_char)

        # Now we have reached the end of the inputted line; add any outstanding number to the _parsed_elements list.
        if number_construct == '':
            if negative_val:
                self._parsed_stack.push('-')
            negative_val = False
        else:
            number_construct, negative_val = self._number_termination(number_construct, negative_val)
        self._parsed_stack.push(' ')

        self.parsed = True
        return self._parsed_stack

    def _number_termination(self, number_construct: str, negative_val: bool) -> tuple:
        if negative_val:
            number_construct = '-' + number_construct
        self._parsed_stack.push(number_construct)
        negative_val = False
        number_construct = ''
        return number_construct, negative_val
