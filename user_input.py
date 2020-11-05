import typing


class UserInput:
    def __init__(self, raw_input: str, is_commenting: bool = False) -> None:
        self._raw_string = raw_input

        self.is_commenting = is_commenting
        self._parsed = False
        self._parsed_elements = []

    def __repr__(self) -> repr:
        if self._parsed:
            return repr(self._parsed_elements)
        return self._raw_string

    def get_parsed_input(self) -> typing.List[str]:
        if self._parsed:
            return self._parsed_elements

        # At this point, _parse() hasn't been called yet. Parse and then return.
        return self._parse()

    def _parse(self) -> typing.List[str]:
        number_construct = ''
        for next_char in self._get_next_char():
            if next_char == '#':
                self.is_commenting = not self.is_commenting
                continue

            if self.is_commenting:
                continue

            if next_char.isdigit():
                number_construct += next_char
                continue

            if number_construct != '':
                self._parsed_elements.append(number_construct)
                number_construct = ''

            if not next_char.isspace():
                self._parsed_elements.append(next_char)

        if number_construct != '':
            self._parsed_elements.append(number_construct)

        self._parsed = True
        return self._parsed_elements

    def _get_next_char(self) -> typing.Iterator[str]:
        for char in self._raw_string:
            yield char
