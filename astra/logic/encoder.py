from astra.logic.gates import or_gate, validate_bit

def encoder(i0: int, i1: int, i2: int, i3: int) -> tuple[int, int]:
    """
    4-to-2 encoder that encodes four input bits into two output bits.
    """

    i0 = validate_bit(i0)
    i1 = validate_bit(i1)
    i2 = validate_bit(i2)
    i3 = validate_bit(i3)

    if i0 + i1 + i2 + i3 != 1:
        raise ValueError("Exactly one input must be active")

    output_1 = or_gate(i2, i3)
    output_0 = or_gate(i1, i3)

    return output_1, output_0