__all__ = (
    "SRPNException", "InvalidInput", "StackException", "StackOverflow",
    "StackUnderflow", "StackEmpty", "OperatorException", "NegativePower",
    "DivideByZero"
)


class SRPNException(Exception):
    """Base exception class for this calculator.
    Ideally speaking, this could be caught to handle any exception thrown by this library.
    """
    pass


class InvalidInput(SRPNException):
    """Exception raised when a character is not recognised."""
    def __init__(self, char: str = '') -> None:
        message = f'Unrecognised operator or operand "{char}".'
        super().__init__(message)


class StackException(SRPNException):
    """A base class for exceptions which occur within the `Stack` class."""
    pass


class StackOverflow(StackException):
    """Exception raised when the stack is full and an additional value is attempted to be pushed onto it."""
    def __init__(self) -> None:
        message = 'Stack overflow.'
        super().__init__(message)


class StackUnderflow(StackException):
    """Exception raised when the stack is empty and an item is attempted to be popped off of it."""
    def __init__(self) -> None:
        message = 'Stack underflow.'
        super().__init__(message)


class StackEmpty(StackException):
    """Exception raised when the top value in the stack is peeked and the stack is empty."""
    def __init__(self) -> None:
        message = 'Stack empty.'
        super().__init__(message)


class OperatorException(SRPNException):
    """Base exception class for exceptions which occur when using operators on the `CInt` class."""
    pass


class NegativePower(OperatorException):
    """Exception raised when a `CInt` is raised to a negative power."""
    def __init__(self, message: str = 'Negative power.') -> None:
        super().__init__(message)


class DivideByZero(OperatorException):
    """Exception raised when a `CInt` is divided by 0."""
    def __init__(self, message: str = 'Divide by 0.') -> None:
        super().__init__(message)
