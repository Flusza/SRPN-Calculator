import typing


class UserInput:
    """
    A class used to represent a line of input from the terminal.
    Has functionality to split (parse) the input into individual elements (numbers, operators and letters).

    Parameters
    ----------
    raw_input: str
        The raw string which was entered by the user into the terminal.
    is_commenting: Optional[bool]
        A bool to determine whether or not the user is currently writing a comment. As comments can be multiline,
        we must keep the state consistent between lines. Defaults to False.
    """
    def __init__(self, raw_input: str, is_commenting: bool = False) -> None:
        self._raw_string = raw_input  # The raw string that was entered by the user into the terminal.
        self._parsed_elements = []  # Individual elements extracted from the string. Populated in the _parse function.
        self.is_commenting = is_commenting  # Whether or not comment mode is currently on/off.
        self.parsed = False  # Bool whether or not the raw_input has been parsed into individual elements already.

    def __repr__(self) -> repr:
        """A """
        if self.parsed:
            return repr(f"Parsed Elements<{self._parsed_elements}>")
        return repr(f"Unparsed String<{self._raw_string}>")

    def get_parsed_input(self) -> typing.List[str]:
        """Returns the list of parsed_elements extracted from the raw_input string."""
        if self.parsed:  # If already parsed, don't do this again unnecessarily.
            return self._parsed_elements

        # At this point, _parse() hasn't been called yet. Parse and then return.
        return self._parse()

    def _parse(self) -> typing.List[str]:
        """Handles all the logic necessary for parsing the raw string. The string is split up into elements.
        Elements which are stored in the parsed_elements list:
            - A single (<10) or series of digits (>10), forming one integer.
            - A single letter or symbol.
        Elements which aren't stored in the list:
            - White space (space, tab enter, etc).
            - A hashtag '#'. This does however, toggle the bool `is_commenting`.

        Returns the list of parsed elements. Note: This could be empty.
            """
        number_construct = ''
        parsed_elements = []
        for next_char in self._get_next_char():
            if next_char == '#':
                # This char toggles between writing comments or not.
                self.is_commenting = not self.is_commenting
                continue

            if self.is_commenting:
                # Comment mode is on. We can ignore any characters until this is disabled.
                continue

            if next_char.isdigit():
                # A number could be more than one digit, so we can't treat them as a single char.
                number_construct += next_char
                continue

            if number_construct != '':
                # After handling the above cases, any char which reaches here means we have reached
                # the end of a number (if there has been one inputted. If so, append it to the _parsed_elements list
                # & reset the number_construct should there be more numbers on this line.
                parsed_elements.append(number_construct)
                number_construct = ''

            if not next_char.isspace():
                # Any other char will be appended individually. We can handle these later.
                parsed_elements.append(next_char)

        if number_construct != '':
            # Now we have reached the end of the inputted line; add any outstanding number to the _parsed_elements list.
            parsed_elements.append(number_construct)

        self.parsed = True
        self._parsed_elements = parsed_elements
        return self._parsed_elements

    def _get_next_char(self) -> typing.Iterator[str]:
        """A generator function which yields each char from the raw_input string."""
        for char in self._raw_string:
            yield char
