import pytest

from astra.cpu.instruction_memory import InstructionMemory
from astra.cpu.program_loader import ProgramLoader
from astra.isa.instructions import Instruction, Opcode, Register


def int_to_bits(value):
    return (
        (value // 8) % 2,
        (value // 4) % 2,
        (value // 2) % 2,
        value % 2,
    )


def read_instruction(
    memory,
    address,
):
    return memory.read(
        int_to_bits(address)
    )


def test_program_loader_initializes():
    memory = InstructionMemory()

    loader = ProgramLoader(memory)

    assert loader.instruction_memory is memory


def test_program_loader_rejects_invalid_memory():
    with pytest.raises(TypeError):
        ProgramLoader(None)


def test_program_loader_rejects_non_list():
    memory = InstructionMemory()

    loader = ProgramLoader(memory)

    with pytest.raises(TypeError):
        loader.load(None)


def test_program_loader_rejects_invalid_instruction():
    memory = InstructionMemory()

    loader = ProgramLoader(memory)

    with pytest.raises(TypeError):
        loader.load([None])


def test_program_loader_loads_single_instruction():
    memory = InstructionMemory()

    loader = ProgramLoader(memory)

    instruction = Instruction(
        Opcode.ADD,
        destination=Register.R1,
        source=Register.R2,
    )

    loader.load([instruction])

    assert read_instruction(
        memory,
        0,
    ) == instruction.encode()[0]


def test_program_loader_loads_multiple_instructions():
    memory = InstructionMemory()

    loader = ProgramLoader(memory)

    add = Instruction(
        Opcode.ADD,
        destination=Register.R1,
        source=Register.R2,
    )

    sub = Instruction(
        Opcode.SUB,
        destination=Register.R1,
        source=Register.R2,
    )

    halt = Instruction(
        Opcode.HALT,
    )

    loader.load([
        add,
        sub,
        halt,
    ])

    assert read_instruction(memory, 0) == add.encode()[0]
    assert read_instruction(memory, 1) == sub.encode()[0]
    assert read_instruction(memory, 2) == halt.encode()[0]


def test_program_loader_load_store_use_two_words():
    memory = InstructionMemory()

    loader = ProgramLoader(memory)

    store = Instruction(
        Opcode.STORE,
        source=Register.R1,
        address=5,
    )

    load = Instruction(
        Opcode.LOAD,
        destination=Register.R2,
        address=7,
    )

    halt = Instruction(
        Opcode.HALT,
    )

    loader.load([
        store,
        load,
        halt,
    ])

    store_encoded = store.encode()
    load_encoded = load.encode()

    assert read_instruction(memory, 0) == store_encoded[0]
    assert read_instruction(memory, 1) == store_encoded[1]

    assert read_instruction(memory, 2) == load_encoded[0]
    assert read_instruction(memory, 3) == load_encoded[1]

    assert read_instruction(memory, 4) == halt.encode()[0]


def test_program_loader_fills_memory_sequentially():
    memory = InstructionMemory()

    loader = ProgramLoader(memory)

    instructions = [
        Instruction(
            Opcode.ADD,
            destination=Register.R1,
            source=Register.R2,
        ),
        Instruction(
            Opcode.NOT,
            destination=Register.R3,
        ),
        Instruction(
            Opcode.HALT,
        ),
    ]

    loader.load(instructions)

    assert read_instruction(
        memory,
        0,
    ) == instructions[0].encode()[0]

    assert read_instruction(
        memory,
        1,
    ) == instructions[1].encode()[0]

    assert read_instruction(
        memory,
        2,
    ) == instructions[2].encode()[0]


def test_program_loader_rejects_program_that_is_too_large():
    memory = InstructionMemory()

    loader = ProgramLoader(memory)

    program = [
        Instruction(
            Opcode.HALT,
        )
        for _ in range(17)
    ]

    with pytest.raises(ValueError):
        loader.load(program)


def test_program_loader_rejects_two_word_program_that_does_not_fit():
    memory = InstructionMemory()

    loader = ProgramLoader(memory)

    program = [
        Instruction(
            Opcode.HALT,
        )
        for _ in range(15)
    ]

    program.append(
        Instruction(
            Opcode.STORE,
            source=Register.R1,
            address=5,
        )
    )

    with pytest.raises(ValueError):
        loader.load(program)