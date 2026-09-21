import pytest

from astra.cpu.fetch_unit import FetchUnit
from astra.cpu.instruction_memory import InstructionMemory


def test_fetch_unit_initializes():
    instruction_memory = InstructionMemory()

    fetch_unit = FetchUnit(
        instruction_memory
    )

    assert fetch_unit.instruction_memory is instruction_memory


def test_fetch_instruction():
    instruction_memory = InstructionMemory()

    address = (0, 0, 0, 0)

    instruction = (
        1, 0, 1, 0,
        1, 1, 0, 0
    )

    instruction_memory.write(
        address=address,
        instruction=instruction,
        write_enable=1,
        clock=0,
    )

    instruction_memory.write(
        address=address,
        instruction=instruction,
        write_enable=1,
        clock=1,
    )

    fetch_unit = FetchUnit(
        instruction_memory
    )

    result = fetch_unit.fetch(address)

    assert result == instruction


def test_fetch_multiple_instructions():
    instruction_memory = InstructionMemory()

    instruction_a = (
        0, 0, 0, 0,
        1, 0, 1, 0
    )

    instruction_b = (
        0, 0, 0, 1,
        1, 1, 0, 0
    )

    address_a = (0, 0, 0, 0)
    address_b = (0, 0, 0, 1)

    instruction_memory.write(
        address=address_a,
        instruction=instruction_a,
        write_enable=1,
        clock=0,
    )

    instruction_memory.write(
        address=address_a,
        instruction=instruction_a,
        write_enable=1,
        clock=1,
    )

    instruction_memory.write(
        address=address_b,
        instruction=instruction_b,
        write_enable=1,
        clock=0,
    )

    instruction_memory.write(
        address=address_b,
        instruction=instruction_b,
        write_enable=1,
        clock=1,
    )

    fetch_unit = FetchUnit(
        instruction_memory
    )

    assert fetch_unit.fetch(address_a) == instruction_a
    assert fetch_unit.fetch(address_b) == instruction_b


def test_fetch_all_instruction_addresses():
    instruction_memory = InstructionMemory()

    instructions = {}

    for address in range(16):

        address_bits = (
            (address >> 3) & 1,
            (address >> 2) & 1,
            (address >> 1) & 1,
            address & 1,
        )

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

        instructions[address] = instruction

        instruction_memory.write(
            address=address_bits,
            instruction=instruction,
            write_enable=1,
            clock=0,
        )

        instruction_memory.write(
            address=address_bits,
            instruction=instruction,
            write_enable=1,
            clock=1,
        )

    fetch_unit = FetchUnit(
        instruction_memory
    )

    for address in range(16):

        address_bits = (
            (address >> 3) & 1,
            (address >> 2) & 1,
            (address >> 1) & 1,
            address & 1,
        )

        assert (
            fetch_unit.fetch(address_bits)
            == instructions[address]
        )


def test_fetch_does_not_modify_memory():
    instruction_memory = InstructionMemory()

    address = (0, 1, 0, 0)

    instruction = (
        1, 1, 0, 1,
        0, 1, 1, 0
    )

    instruction_memory.write(
        address=address,
        instruction=instruction,
        write_enable=1,
        clock=0,
    )

    instruction_memory.write(
        address=address,
        instruction=instruction,
        write_enable=1,
        clock=1,
    )

    fetch_unit = FetchUnit(
        instruction_memory
    )

    first_fetch = fetch_unit.fetch(address)
    second_fetch = fetch_unit.fetch(address)

    assert first_fetch == instruction
    assert second_fetch == instruction


def test_invalid_program_counter_length():
    instruction_memory = InstructionMemory()
    fetch_unit = FetchUnit(instruction_memory)

    with pytest.raises(ValueError):
        fetch_unit.fetch((0, 0, 0))


def test_invalid_program_counter_bit():
    instruction_memory = InstructionMemory()
    fetch_unit = FetchUnit(instruction_memory)

    with pytest.raises(ValueError):
        fetch_unit.fetch((0, 0, 0, 2))


def test_invalid_instruction_memory():
    with pytest.raises(TypeError):
        FetchUnit(None)