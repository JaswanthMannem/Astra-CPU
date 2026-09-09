from astra.logic.gates import and_gate, not_gate

def decoder(a: int, b: int) -> tuple[int, int, int, int]:
    """
    2-to-4 decoder that activates exactly one output corresponding to the two input bits.
    """
    output_0 = and_gate(not_gate(a), not_gate(b))
    output_1 = and_gate(not_gate(a), b)
    output_2 = and_gate(a, not_gate(b))
    output_3 = and_gate(a, b)
    
    return output_0, output_1, output_2, output_3