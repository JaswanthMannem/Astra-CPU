from astra.logic.gates import or_gate, and_gate, not_gate

def mux(a: int, b: int, select: int) -> int:
    """
    Multiplexer function that selects between two inputs based on a select signal.
    """

    return or_gate(and_gate(a, not_gate(select)), and_gate(b, select))

def mux4(i0: int, i1: int, i2: int, i3: int, s1: int, s0: int) -> int:
    """
    4-to-1 multiplexer function that selects between four inputs based on two select signals.
    """
    x = mux(i0, i1, s0)
    y = mux(i2, i3, s0)
    return mux(x, y, s1)

def mux8(i0: int, i1: int, i2: int, i3: int, i4: int, i5: int, i6: int, i7: int, s2: int, s1: int, s0: int) -> int:
    """
    8-to-1 multiplexer function that selects between eight inputs based on three select signals.
    """
    x = mux4(i0, i1, i2, i3, s1, s0)
    y = mux4(i4, i5, i6, i7, s1, s0)
    return mux(x, y, s2)

def mux_4bit(a: tuple[int, int, int, int], b: tuple[int, int, int, int], select: int) -> tuple[int, int, int, int]:
    """Select one of two 4-bit inputs based on the select signal."""
    select_bits = []
    for i in range(4):
        select_bit = mux(a[i], b[i], select)
        select_bits.append(select_bit)
    return tuple(select_bits)