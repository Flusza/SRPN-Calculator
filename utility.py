operator_map = {  # A dictionary mapping string-like mathematical operators to their corresponding function.
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a // b,
    '%': lambda a, b: a % b,
    '^': lambda a, b: pow(a, b),
}
