import pytest

from astra.cpu.fetch_decode import FetchDecode
from astra.cpu.fetch_unit import FetchUnit
from astra.cpu.instruction_memory import InstructionMemory
from astra.isa.decoder import InstructionDecoder
from astra.isa.instructions import (
    Instruction,
    Opcode,
    Register,
)


def create_fetch_decode():
    instruction_memory = InstructionMemory()

    fetch_unit = FetchUnit(
        instruction_memory
    )

    decoder = InstructionDecoder()

    fetch_decode = FetchDecode(
        fetch_unit,
        decoder,
    )

    return instruction_memory, fetch_decode


def write_instruction(
    memory,
    address,
    instruction,
):
    memory.write(
        address=address,
        instruction=instruction,
        write_enable=1,
        clock=0,
    )

    memory.write(
        address=address,
        instruction=instruction,
        write_enable=1,
        clock=1,
    )


def test_fetch_decode_initializes():
    instruction_memory = InstructionMemory()

    fetch_unit = FetchUnit(
        instruction_memory
    )

    decoder = InstructionDecoder()

    fetch_decode = FetchDecode(
        fetch_unit,
        decoder,
    )

    assert fetch_decode.fetch_unit is fetch_unit
    assert fetch_decode.decoder is decoder


def test_fetch_decode_add():
    memory, fetch_decode = create_fetch_decode()

    word = Instruction(
        Opcode.ADD,
        destination=Register.R1,
        source=Register.R2,
    ).encode()[0]

    address = (0, 0, 0, 0)

    write_instruction(
        memory,
        address,
        word,
    )

    result = fetch_decode.fetch_and_decode(
        address
    )

    assert result["opcode"] == Opcode.ADD
    assert result["destination"] == Register.R1
    assert result["source"] == Register.R2
    assert result["address"] is None


def test_fetch_decode_sub():
    memory, fetch_decode = create_fetch_decode()

    word = Instruction(
        Opcode.SUB,
        destination=Register.R2,
        source=Register.R3,
    ).encode()[0]

    address = (0, 0, 0, 1)

    write_instruction(
        memory,
        address,
        word,
    )

    result = fetch_decode.fetch_and_decode(
        address
    )

    assert result["opcode"] == Opcode.SUB
    assert result["destination"] == Register.R2
    assert result["source"] == Register.R3
    assert result["address"] is None


def test_fetch_decode_not():
    memory, fetch_decode = create_fetch_decode()

    word = Instruction(
        Opcode.NOT,
        destination=Register.R1,
    ).encode()[0]

    address = (0, 0, 1, 0)

    write_instruction(
        memory,
        address,
        word,
    )

    result = fetch_decode.fetch_and_decode(
        address
    )

    assert result["opcode"] == Opcode.NOT
    assert result["destination"] == Register.R1
    assert result["source"] is None
    assert result["address"] is None


def test_fetch_decode_load():
    memory, fetch_decode = create_fetch_decode()

    words = Instruction(
        Opcode.LOAD,
        destination=Register.R2,
        address=10,
    ).encode()

    first_word = words[0]

    address = (0, 0, 1, 1)

    write_instruction(
        memory,
        address,
        first_word,
    )

    result = fetch_decode.fetch_and_decode(
        address
    )

    assert result["opcode"] == Opcode.LOAD
    assert result["destination"] == Register.R2


def test_fetch_decode_store():
    memory, fetch_decode = create_fetch_decode()

    words = Instruction(
        Opcode.STORE,
        source=Register.R1,
        address=10,
    ).encode()

    first_word = words[0]

    address = (0, 1, 0, 0)

    write_instruction(
        memory,
        address,
        first_word,
    )

    result = fetch_decode.fetch_and_decode(
        address
    )

    assert result["opcode"] == Opcode.STORE
    assert result["source"] == Register.R1


def test_fetch_decode_jump():
    memory, fetch_decode = create_fetch_decode()

    word = Instruction(
        Opcode.JUMP,
        address=10,
    ).encode()[0]

    address = (0, 1, 0, 1)

    write_instruction(
        memory,
        address,
        word,
    )

    result = fetch_decode.fetch_and_decode(
        address
    )

    assert result["opcode"] == Opcode.JUMP
    assert result["destination"] is None
    assert result["source"] is None
    assert result["address"] == 10


def test_fetch_decode_halt():
    memory, fetch_decode = create_fetch_decode()

    word = Instruction(
        Opcode.HALT
    ).encode()[0]

    address = (0, 1, 1, 0)

    write_instruction(
        memory,
        address,
        word,
    )

    result = fetch_decode.fetch_and_decode(
        address
    )

    assert result["opcode"] == Opcode.HALT
    assert result["destination"] is None
    assert result["source"] is None
    assert result["address"] is None


def test_fetch_decode_different_addresses():
    memory, fetch_decode = create_fetch_decode()

    word_a = Instruction(
        Opcode.ADD,
        destination=Register.R1,
        source=Register.R2,
    ).encode()[0]

    word_b = Instruction(
        Opcode.SUB,
        destination=Register.R3,
        source=Register.R1,
    ).encode()[0]

    address_a = (0, 0, 0, 0)
    address_b = (0, 0, 0, 1)

    write_instruction(
        memory,
        address_a,
        word_a,
    )

    write_instruction(
        memory,
        address_b,
        word_b,
    )

    result_a = fetch_decode.fetch_and_decode(
        address_a
    )

    result_b = fetch_decode.fetch_and_decode(
        address_b
    )

    assert result_a["opcode"] == Opcode.ADD
    assert result_a["destination"] == Register.R1
    assert result_a["source"] == Register.R2

    assert result_b["opcode"] == Opcode.SUB
    assert result_b["destination"] == Register.R3
    assert result_b["source"] == Register.R1


def test_fetch_decode_does_not_modify_memory():
    memory, fetch_decode = create_fetch_decode()

    address = (0, 1, 1, 1)

    word = Instruction(
        Opcode.ADD,
        destination=Register.R2,
        source=Register.R3,
    ).encode()[0]

    write_instruction(
        memory,
        address,
        word,
    )

    first_result = fetch_decode.fetch_and_decode(
        address
    )

    second_result = fetch_decode.fetch_and_decode(
        address
    )

    assert first_result == second_result

    assert first_result["opcode"] == Opcode.ADD
    assert first_result["destination"] == Register.R2
    assert first_result["source"] == Register.R3


def test_invalid_fetch_unit():
    decoder = InstructionDecoder()

    with pytest.raises(TypeError):
        FetchDecode(
            None,
            decoder,
        )


def test_invalid_decoder():
    instruction_memory = InstructionMemory()

    fetch_unit = FetchUnit(
        instruction_memory
    )

    with pytest.raises(TypeError):
        FetchDecode(
            fetch_unit,
            None,
        )


def test_invalid_program_counter():
    _, fetch_decode = create_fetch_decode()

    with pytest.raises(ValueError):
        fetch_decode.fetch_and_decode(
            (0, 0, 0)
        )