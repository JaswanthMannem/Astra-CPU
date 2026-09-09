from astra.logic.bitwise import and_4bit, not_4bit, or_4bit, xor_4bit, zero_flag, negative_flag, overflow_flag
from astra.logic.mux import mux8
from astra.logic.adder import ripple_carry_adder


def alu(a: tuple[int, int, int, int], b: tuple[int, int, int, int], select: tuple[int, int, int]) -> tuple[tuple[int, int, int, int], int, int, int, int]:
    """
    4-bit ALU.

    Select signal:
        000: Bitwise AND
        001: Bitwise OR
        010: Bitwise XOR
        011: Bitwise NOT A
        100: Addition
        101: Subtraction

    Returns:
        result: 4-bit result
        carry: carry-out from addition/subtraction
        zero: 1 if result is zero, otherwise 0
    """

    result_bits = []
    carry = 0
    
    and_result = and_4bit(a, b)
    or_result = or_4bit(a, b)
    xor_result = xor_4bit(a, b)
    not_result = not_4bit(a)
    add_result, add_carry = ripple_carry_adder(a, b)

    not_b = not_4bit(b)
    sub_result, sub_carry = ripple_carry_adder(a, not_b, 1)

    for i in range(4):
        result_bit = mux8(
            and_result[i],
            or_result[i],
            xor_result[i],
            not_result[i],
            add_result[i],
            sub_result[i],
            0,
            0,
            select[0],
            select[1],
            select[2]
        )

        result_bits.append(result_bit)

    if select == (1, 0, 0):
        carry = add_carry
    elif select == (1, 0, 1):
        carry = sub_carry

    result = tuple(result_bits)
    zero = zero_flag(result)
    negative = negative_flag(result)

    overflow = overflow_flag(
        a,
        b,
        result,
        1 if select == (1, 0, 1) else 0
    )

    return result, carry, zero, negative, overflow
