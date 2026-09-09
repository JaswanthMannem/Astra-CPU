from astra.logic.gates import and_gate, not_gate

def dmux(input: int, select: int) -> tuple[int, int]:
    """
    Demultiplexer function that routes a single input to one of two outputs based on a select signal.
    """
    output_a = and_gate(input, not_gate(select))
    output_b = and_gate(input, select)
    return output_a, output_b

def dmux4(input: int, select: tuple[int,int]) -> tuple[int, int, int, int]:
    """
    4-way Demultiplexer function that routes a single input to one of four outputs based on a 2-bit select signal.
    """
    output_a, output_b = dmux(input, select[0])

    output_0, output_1 = dmux(output_a, select[1])
    output_2, output_3 = dmux(output_b, select[1])

    return output_0, output_1, output_2, output_3

def dmux8(input: int, select: tuple[int, int, int]) -> tuple[int, int, int, int, int, int, int, int]:
    """
    8-way Demultiplexer function that routes a single input to one of eight outputs based on a 3-bit select signal.
    """
    output_a, output_b = dmux(input, select[0])

    output_0, output_1, output_2, output_3 = dmux4(output_a, (select[1], select[2]))
    output_4, output_5, output_6, output_7 = dmux4(output_b, (select[1], select[2]))

    return output_0, output_1, output_2, output_3, output_4, output_5, output_6, output_7