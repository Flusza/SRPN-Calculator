__all__ = (
    "SRPNException", "InvalidInput", "StackException", "StackOverflow",
    "StackUnderflow", "StackEmpty", "OperatorException", "NegativePower",
    "DivideByZero"
)


class SRPNException(Exception):
    """Base exception class for this calculator.

    Ideally, this could be caught to handle any exceptions thrown by this library.
    """
    pass


class InvalidInput(SRPNException):
    """Exception raised when a character is not recognised"""
    def __init__(self, char: str = '') -> None:
        message = f'Unrecognised operator or operand "{char}".'
        super().__init__(message)


class StackException(SRPNException):
    """A base class for exceptions which occur within the `Stack` class."""
    pass


class StackOverflow(StackException):
    def __init__(self) -> None:
        message = 'Stack overflow.'
        super().__init__(message)


class StackUnderflow(StackException):
    def __init__(self) -> None:
        message = 'Stack underflow.'
        super().__init__(message)


class StackEmpty(StackException):
    def __init__(self) -> None:
        message = 'Stack empty.'
        super().__init__(message)


class OperatorException(SRPNException):
    pass


class NegativePower(OperatorException):
    def __init__(self, message: str = 'Negative power.') -> None:
        super().__init__(message)


class DivideByZero(OperatorException):
    def __init__(self, message: str = 'Divide by 0.') -> None:
        super().__init__(message)