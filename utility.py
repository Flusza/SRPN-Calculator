operator_map = {  # A dictionary mapping string-like mathematical operators to their corresponding function.
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a // b,
    '%': lambda a, b: a % b,
    '^': lambda a, b: pow(a, b),
}


def is_digit(n: str) -> bool:
    try:
        int(n)
        return True
    except ValueError:
        return False
