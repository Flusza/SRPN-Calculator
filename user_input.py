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

    Attributes
    ----------
    parsed: bool
        A bool as to whether or not the raw_input has been parsed into individual elements already.
    is_commenting: bool
        Whether or not comment mode is currently on/off

    Methods
    -------
    get_parsed_input()
    """
    def __init__(self, raw_input: str, is_commenting: bool = False) -> None:
        self._raw_string = raw_input  # The raw string that was entered by the user into the terminal.

        self.is_commenting = is_commenting
        self.parsed = False
        self._parsed_elements = []

    def __repr__(self) -> repr:
        if self.parsed:
            return repr(self._parsed_elements)
        return self._raw_string

    def get_parsed_input(self) -> typing.List[str]:
        if self.parsed:  # If already parsed, don't do this again unnecessarily.
            return self._parsed_elements

        # At this point, _parse() hasn't been called yet. Parse and then return.
        return self._parse()

    def _parse(self) -> typing.List[str]:
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
        for char in self._raw_string:
            yield char
