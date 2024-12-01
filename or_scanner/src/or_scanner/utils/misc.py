def to_base(number, base):
    if base > 16:
        raise ValueError(f"base must be smaler than 17 (was {base})")
    if number == 0:
        return "0"
    res = ""
    symbols = "0123456789abcdef"
    while number:
        res = symbols[number % base] + res
        number = number // base
    return res
