import pytest

from astra.cpu.cpu_cycle import CPUCycle
from astra.cpu.instruction_memory import InstructionMemory
from astra.isa.instructions import (
    Instruction,
    Opcode,
    Register,
)


def bits_to_int(bits):
    value = 0

    for bit in bits:
        value = value * 2 + bit

    return value


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


def write_register(
    register_file,
    address,
    value,
):
    register_file.update(
        write_address=address,
        write_data=value,
        write_enable=1,
        read_address_a=address,
        read_address_b=address,
        clock=0,
    )

    register_file.update(
        write_address=address,
        write_data=value,
        write_enable=1,
        read_address_a=address,
        read_address_b=address,
        clock=1,
    )


def read_register(
    register_file,
    address,
):
    values = register_file.read(
        read_address_a=address,
        read_address_b=address,
    )

    return values[0]


def test_cpu_cycle_initializes():
    instruction_memory = InstructionMemory()

    cpu = CPUCycle(
        instruction_memory
    )

    assert cpu.instruction_memory is instruction_memory
    assert cpu.fetch_unit.instruction_memory is instruction_memory
    assert cpu.program_counter is not None
    assert cpu.fetch_decode is not None
    assert cpu.control_unit is not None
    assert cpu.datapath is not None


def test_cpu_cycle_add():
    instruction_memory = InstructionMemory()

    cpu = CPUCycle(
        instruction_memory
    )

    write_register(
        cpu.datapath.register_file,
        (0, 1),
        (0, 0, 1, 1),
    )

    write_register(
        cpu.datapath.register_file,
        (1, 0),
        (0, 1, 0, 1),
    )

    word = Instruction(
        Opcode.ADD,
        destination=Register.R1,
        source=Register.R2,
    ).encode()[0]

    write_instruction(
        instruction_memory,
        (0, 0, 0, 0),
        word,
    )

    decoded, result = cpu.cycle(
        clock=0
    )

    cpu.cycle(
        clock=1
    )

    assert decoded["opcode"] == Opcode.ADD
    assert decoded["destination"] == Register.R1
    assert decoded["source"] == Register.R2

    assert result == (1, 0, 0, 0)

    r1 = read_register(
        cpu.datapath.register_file,
        (0, 1),
    )

    assert r1 == (1, 0, 0, 0)


def test_cpu_cycle_sub():
    instruction_memory = InstructionMemory()

    cpu = CPUCycle(
        instruction_memory
    )

    write_register(
        cpu.datapath.register_file,
        (0, 1),
        (0, 1, 0, 1),
    )

    write_register(
        cpu.datapath.register_file,
        (1, 0),
        (0, 0, 1, 1),
    )

    word = Instruction(
        Opcode.SUB,
        destination=Register.R1,
        source=Register.R2,
    ).encode()[0]

    write_instruction(
        instruction_memory,
        (0, 0, 0, 0),
        word,
    )

    decoded, result = cpu.cycle(
        clock=0
    )

    cpu.cycle(
        clock=1
    )

    assert decoded["opcode"] == Opcode.SUB
    assert result == (0, 0, 1, 0)

    r1 = read_register(
        cpu.datapath.register_file,
        (0, 1),
    )

    assert r1 == (0, 0, 1, 0)


def test_cpu_cycle_and():
    instruction_memory = InstructionMemory()

    cpu = CPUCycle(
        instruction_memory
    )

    write_register(
        cpu.datapath.register_file,
        (0, 1),
        (1, 1, 0, 0),
    )

    write_register(
        cpu.datapath.register_file,
        (1, 0),
        (1, 0, 1, 0),
    )

    word = Instruction(
        Opcode.AND,
        destination=Register.R1,
        source=Register.R2,
    ).encode()[0]

    write_instruction(
        instruction_memory,
        (0, 0, 0, 0),
        word,
    )

    decoded, result = cpu.cycle(
        clock=0
    )

    cpu.cycle(
        clock=1
    )

    assert decoded["opcode"] == Opcode.AND
    assert result == (1, 0, 0, 0)


def test_cpu_cycle_or():
    instruction_memory = InstructionMemory()

    cpu = CPUCycle(
        instruction_memory
    )

    write_register(
        cpu.datapath.register_file,
        (0, 1),
        (1, 0, 0, 0),
    )

    write_register(
        cpu.datapath.register_file,
        (1, 0),
        (0, 1, 0, 0),
    )

    word = Instruction(
        Opcode.OR,
        destination=Register.R1,
        source=Register.R2,
    ).encode()[0]

    write_instruction(
        instruction_memory,
        (0, 0, 0, 0),
        word,
    )

    decoded, result = cpu.cycle(
        clock=0
    )

    cpu.cycle(
        clock=1
    )

    assert decoded["opcode"] == Opcode.OR
    assert result == (1, 1, 0, 0)


def test_cpu_cycle_xor():
    instruction_memory = InstructionMemory()

    cpu = CPUCycle(
        instruction_memory
    )

    write_register(
        cpu.datapath.register_file,
        (0, 1),
        (1, 1, 0, 0),
    )

    write_register(
        cpu.datapath.register_file,
        (1, 0),
        (1, 0, 1, 0),
    )

    word = Instruction(
        Opcode.XOR,
        destination=Register.R1,
        source=Register.R2,
    ).encode()[0]

    write_instruction(
        instruction_memory,
        (0, 0, 0, 0),
        word,
    )

    decoded, result = cpu.cycle(
        clock=0
    )

    cpu.cycle(
        clock=1
    )

    assert decoded["opcode"] == Opcode.XOR
    assert result == (0, 1, 1, 0)


def test_cpu_cycle_not():
    instruction_memory = InstructionMemory()

    cpu = CPUCycle(
        instruction_memory
    )

    write_register(
        cpu.datapath.register_file,
        (0, 1),
        (1, 0, 1, 0),
    )

    word = Instruction(
        Opcode.NOT,
        destination=Register.R1,
    ).encode()[0]

    write_instruction(
        instruction_memory,
        (0, 0, 0, 0),
        word,
    )

    decoded, result = cpu.cycle(
        clock=0
    )

    cpu.cycle(
        clock=1
    )

    assert decoded["opcode"] == Opcode.NOT
    assert result == (0, 1, 0, 1)

    r1 = read_register(
        cpu.datapath.register_file,
        (0, 1),
    )

    assert r1 == (0, 1, 0, 1)


def test_cpu_cycle_increments_pc():
    instruction_memory = InstructionMemory()

    cpu = CPUCycle(
        instruction_memory
    )

    word = Instruction(
        Opcode.ADD,
        destination=Register.R1,
        source=Register.R2,
    ).encode()[0]

    write_instruction(
        instruction_memory,
        (0, 0, 0, 0),
        word,
    )

    cpu.cycle(
        clock=0
    )

    cpu.cycle(
        clock=1
    )

    pc = tuple(
        register.dff.slave.latch.q
        for register in cpu.program_counter.register.registers
    )

    assert pc == (0, 0, 0, 1)


def test_cpu_cycle_multiple_instructions():
    instruction_memory = InstructionMemory()

    cpu = CPUCycle(
        instruction_memory
    )

    write_register(
        cpu.datapath.register_file,
        (0, 1),
        (0, 0, 1, 1),
    )

    write_register(
        cpu.datapath.register_file,
        (1, 0),
        (0, 0, 1, 0),
    )

    add_word = Instruction(
        Opcode.ADD,
        destination=Register.R1,
        source=Register.R2,
    ).encode()[0]

    sub_word = Instruction(
        Opcode.SUB,
        destination=Register.R1,
        source=Register.R2,
    ).encode()[0]

    write_instruction(
        instruction_memory,
        (0, 0, 0, 0),
        add_word,
    )

    write_instruction(
        instruction_memory,
        (0, 0, 0, 1),
        sub_word,
    )

    cpu.cycle(clock=0)
    cpu.cycle(clock=1)

    r1_after_add = read_register(
        cpu.datapath.register_file,
        (0, 1),
    )

    assert r1_after_add == (0, 1, 0, 1)

    cpu.cycle(clock=0)
    cpu.cycle(clock=1)

    r1_after_sub = read_register(
        cpu.datapath.register_file,
        (0, 1),
    )

    assert r1_after_sub == (0, 0, 1, 1)


def test_cpu_cycle_invalid_clock():
    instruction_memory = InstructionMemory()

    cpu = CPUCycle(
        instruction_memory
    )

    with pytest.raises(ValueError):
        cpu.cycle(
            clock=2
        )


def test_cpu_cycle_invalid_instruction_memory():
    with pytest.raises(TypeError):
        CPUCycle(
            None
        )