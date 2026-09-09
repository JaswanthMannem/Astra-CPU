from astra.logic.gates import not_gate, and_gate, or_gate, xor_gate

def not_4bit(bits: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    """
    4-bit NOT gate.

    Args:
        bits: 4-bit input tuple
    """
    result_bits = []

    for i in range(4):
        result_bits.append(not_gate(bits[i]))

    return tuple(result_bits)

def and_4bit(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    """
    4-bit AND gate.

    Args:
        a: 4-bit input tuple
        b: 4-bit input tuple
    """
    result_bits = []

    for i in range(4):
        result_bits.append(and_gate(a[i], b[i]))

    return tuple(result_bits)

def or_4bit(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    """
    4-bit OR gate.

    Args:
        a: 4-bit input tuple
        b: 4-bit input tuple
    """
    result_bits = []

    for i in range(4):
        result_bits.append(or_gate(a[i], b[i]))

    return tuple(result_bits)

def xor_4bit(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    """
    4-bit XOR gate.

    Args:
        a: 4-bit input tuple
        b: 4-bit input tuple
    """
    result_bits = []

    for i in range(4):
        result_bits.append(xor_gate(a[i], b[i]))

    return tuple(result_bits)

def zero_flag(bits: tuple[int, int, int, int]) -> int:
    """
    Returns 1 if all four bits are 0.
    Returns 0 if any bit is 1.
    """
    result = or_gate(bits[0], bits[1])
    result = or_gate(result, bits[2])
    result = or_gate(result, bits[3])

    return not_gate(result)

def negative_flag(bits: tuple[int, int, int, int]) -> int:
    """
    Returns 1 if the most significant bit is 1 (negative).
    Returns 0 if the most significant bit is 0 (non-negative).
    """
    return bits[0]

def overflow_flag(a: tuple[int, int, int, int], b: tuple[int, int, int, int], result: tuple[int, int, int, int], subtract: int) -> int:
    """
    Returns 1 if a signed 4-bit arithmetic operation overflowed.

    subtract:
        0 -> addition
        1 -> subtraction
    """
    # Overflow occurs if the sign of the result is different from the sign of the inputs
    a_sign = a[0]
    b_sign = b[0]
    result_sign = result[0]

    same_sign = xor_gate(a_sign, b_sign)
    sign_change = xor_gate(a_sign, result_sign)

    addition_overflow = and_gate(
        not_gate(same_sign),
        sign_change
    )

    subtraction_overflow = and_gate(
        same_sign,
        sign_change
    )

    return or_gate(
        and_gate(not_gate(subtract), addition_overflow),
        and_gate(subtract, subtraction_overflow)
    )