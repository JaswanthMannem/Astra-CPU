from astra.logic.gates import or_gate, and_gate, xor_gate, validate_bit

def half_adder(a: int, b: int) -> tuple[int, int]:
    """
    Half adder function that adds two bits and returns the sum and carry.
    """
    sum_bit = xor_gate(a, b)
    carry_bit = and_gate(a, b)

    return sum_bit, carry_bit

def full_adder(a: int, b: int, carry_in: int) -> tuple[int, int]:
    """
    Full adder function that adds two bits and a carry-in bit, returning the sum and carry-out.
    """
    sum_bit, carry_out = half_adder(a, b)
    sum_bit, carry_out2 = half_adder(sum_bit, carry_in)
    carry_out = or_gate(carry_out, carry_out2)

    return sum_bit, carry_out

def ripple_carry_adder(a: tuple[int,int, int, int], b: tuple[int,int, int, int], carry_in: int = 0) -> tuple[tuple[int,int, int, int], int]:
    """
    4-bit ripple carry adder that adds two 4-bit numbers and returns the sum and carry-out.
    """

    if len(a) != 4 or len(b) != 4:
        raise ValueError("Both inputs must be 4 bits long")
    
    a = tuple(validate_bit(bit) for bit in a)
    b = tuple(validate_bit(bit) for bit in b)
    carry_in = validate_bit(carry_in)
    
    sum_bits = []
    carry = carry_in

    for i in range(3, -1, -1):
        sum_bit, carry = full_adder(a[i], b[i], carry)
        sum_bits.append(sum_bit)

    sum_bits.reverse()  # Reverse to maintain the correct order of bits

    return tuple(sum_bits), carry