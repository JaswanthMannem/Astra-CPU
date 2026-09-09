def validate_bit(value: int) -> int:
    if value not in (0, 1) or isinstance(value, bool):
        raise ValueError(f"Invalid bit: {value}")
    return value

def and_gate(a: int, b: int) -> int:
    a = validate_bit(a)
    b = validate_bit(b)
    return a & b

def or_gate(a: int, b: int) -> int:
    a = validate_bit(a)
    b = validate_bit(b)
    return a | b

def not_gate(a: int) -> int:
    a = validate_bit(a)
    return 1-a

def nand_gate(a: int, b: int) -> int:
    return not_gate(and_gate(a, b))

def nor_gate(a: int, b: int) -> int:
    return not_gate(or_gate(a, b))

def xor_gate(a: int, b: int) -> int:
    return or_gate(and_gate(a, not_gate(b)), and_gate(not_gate(a), b))

def xnor_gate(a: int, b: int) -> int:
    return not_gate(xor_gate(a, b))

