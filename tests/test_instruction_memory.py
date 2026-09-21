import pytest

from astra.cpu.instruction_memory import InstructionMemory


def test_instruction_memory_initializes():
    memory = InstructionMemory()

    for address in range(16):
        bits = (
            (address >> 3) & 1,
            (address >> 2) & 1,
            (address >> 1) & 1,
            address & 1,
        )

        assert memory.read(bits) == (
            0, 0, 0, 0, 0, 0, 0, 0
        )


def test_write_and_read_instruction():
    memory = InstructionMemory()

    address = (0, 0, 0, 0)

    instruction = (
        1, 0, 1, 0,
        1, 1, 0, 0
    )

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

    assert memory.read(address) == instruction


def test_write_requires_write_enable():
    memory = InstructionMemory()

    address = (0, 0, 0, 1)

    instruction = (
        1, 1, 0, 0,
        0, 1, 0, 1
    )

    memory.write(
        address=address,
        instruction=instruction,
        write_enable=0,
        clock=1,
    )

    assert memory.read(address) == (
        0, 0, 0, 0,
        0, 0, 0, 0
    )


def test_write_requires_rising_clock():
    memory = InstructionMemory()

    address = (0, 0, 1, 0)

    instruction = (
        1, 0, 0, 1,
        1, 0, 1, 1
    )

    memory.write(
        address=address,
        instruction=instruction,
        write_enable=1,
        clock=0,
    )

    assert memory.read(address) == (
        0, 0, 0, 0,
        0, 0, 0, 0
    )


def test_multiple_instructions():
    memory = InstructionMemory()

    instruction_a = (
        0, 0, 0, 0,
        1, 1, 0, 0
    )

    instruction_b = (
        1, 0, 1, 0,
        0, 1, 1, 1
    )

    address_a = (0, 0, 0, 0)
    address_b = (0, 0, 0, 1)

    memory.write(
        address_a,
        instruction_a,
        1,
        0,
    )

    memory.write(
        address_a,
        instruction_a,
        1,
        1,
    )

    memory.write(
        address_b,
        instruction_b,
        1,
        0,
    )

    memory.write(
        address_b,
        instruction_b,
        1,
        1,
    )

    assert memory.read(address_a) == instruction_a
    assert memory.read(address_b) == instruction_b


def test_writing_one_address_does_not_change_another():
    memory = InstructionMemory()

    instruction = (
        1, 1, 1, 1,
        0, 0, 0, 0
    )

    memory.write(
        address=(0, 0, 0, 0),
        instruction=instruction,
        write_enable=1,
        clock=0,
    )

    memory.write(
        address=(0, 0, 0, 0),
        instruction=instruction,
        write_enable=1,
        clock=1,
    )

    assert memory.read((0, 0, 0, 0)) == instruction

    assert memory.read((0, 0, 0, 1)) == (
        0, 0, 0, 0,
        0, 0, 0, 0
    )


def test_all_sixteen_addresses():
    memory = InstructionMemory()

    instructions = []

    for address in range(16):

        instruction = (
            (address >> 3) & 1,
            (address >> 2) & 1,
            (address >> 1) & 1,
            address & 1,
            1,
            0,
            1,
            0,
        )

        instructions.append(instruction)

        bits = (
            (address >> 3) & 1,
            (address >> 2) & 1,
            (address >> 1) & 1,
            address & 1,
        )

        memory.write(
            address=bits,
            instruction=instruction,
            write_enable=1,
            clock=0,
        )

        memory.write(
            address=bits,
            instruction=instruction,
            write_enable=1,
            clock=1,
        )

    for address in range(16):

        bits = (
            (address >> 3) & 1,
            (address >> 2) & 1,
            (address >> 1) & 1,
            address & 1,
        )

        assert memory.read(bits) == instructions[address]


def test_invalid_address_length():
    memory = InstructionMemory()

    with pytest.raises(ValueError):
        memory.read((0, 0, 0))


def test_invalid_address_bit():
    memory = InstructionMemory()

    with pytest.raises(ValueError):
        memory.read((0, 0, 0, 2))


def test_invalid_instruction_length():
    memory = InstructionMemory()

    with pytest.raises(ValueError):
        memory.write(
            address=(0, 0, 0, 0),
            instruction=(1, 0, 1),
            write_enable=1,
            clock=1,
        )


def test_invalid_instruction_bit():
    memory = InstructionMemory()

    with pytest.raises(ValueError):
        memory.write(
            address=(0, 0, 0, 0),
            instruction=(1, 0, 1, 0, 2, 0, 0, 1),
            write_enable=1,
            clock=1,
        )


def test_invalid_write_enable():
    memory = InstructionMemory()

    with pytest.raises(ValueError):
        memory.write(
            address=(0, 0, 0, 0),
            instruction=(1, 0, 1, 0, 1, 0, 0, 1),
            write_enable=2,
            clock=1,
        )


def test_invalid_clock():
    memory = InstructionMemory()

    with pytest.raises(ValueError):
        memory.write(
            address=(0, 0, 0, 0),
            instruction=(1, 0, 1, 0, 1, 0, 0, 1),
            write_enable=1,
            clock=2,
        )