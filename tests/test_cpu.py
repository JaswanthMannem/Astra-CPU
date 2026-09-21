import pytest

from astra.cpu.cpu import CPU
from astra.cpu.instruction_memory import InstructionMemory
from astra.isa.instructions import Instruction, Opcode, Register


def int_to_bits(value):
    return (
        (value // 8) % 2,
        (value // 4) % 2,
        (value // 2) % 2,
        value % 2,
    )


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


def write_two_word_instruction(
    memory,
    address,
    instruction,
):
    encoded = instruction.encode()

    assert len(encoded) == 2

    write_instruction(
        memory,
        address,
        encoded[0],
    )

    next_address = int_to_bits(
        (
            address[0] * 8
            + address[1] * 4
            + address[2] * 2
            + address[3]
            + 1
        ) % 16
    )

    write_instruction(
        memory,
        next_address,
        encoded[1],
    )


def read_register(
    cpu,
    address,
):
    values = cpu.cycle.datapath.register_file.read(
        read_address_a=address,
        read_address_b=address,
    )

    return values[0]


def read_pc(cpu):
    return tuple(
        register.dff.slave.latch.q
        for register
        in cpu.cycle.program_counter.register.registers
    )


# ============================================================
# Initialization
# ============================================================


def test_cpu_initializes():
    instruction_memory = InstructionMemory()

    cpu = CPU(
        instruction_memory
    )

    assert cpu.instruction_memory is instruction_memory
    assert cpu.cycle is not None


def test_cpu_rejects_invalid_instruction_memory():
    with pytest.raises(TypeError):
        CPU(None)


# ============================================================
# STEP
# ============================================================


def test_cpu_step_executes_add():
    instruction_memory = InstructionMemory()

    cpu = CPU(
        instruction_memory
    )

    # R1 = 0011
    cpu.cycle.datapath.register_file.update(
        write_address=(0, 1),
        write_data=(0, 0, 1, 1),
        write_enable=1,
        read_address_a=(0, 1),
        read_address_b=(0, 1),
        clock=0,
    )

    cpu.cycle.datapath.register_file.update(
        write_address=(0, 1),
        write_data=(0, 0, 1, 1),
        write_enable=1,
        read_address_a=(0, 1),
        read_address_b=(0, 1),
        clock=1,
    )

    # R2 = 0010
    cpu.cycle.datapath.register_file.update(
        write_address=(1, 0),
        write_data=(0, 0, 1, 0),
        write_enable=1,
        read_address_a=(1, 0),
        read_address_b=(1, 0),
        clock=0,
    )

    cpu.cycle.datapath.register_file.update(
        write_address=(1, 0),
        write_data=(0, 0, 1, 0),
        write_enable=1,
        read_address_a=(1, 0),
        read_address_b=(1, 0),
        clock=1,
    )

    add = Instruction(
        Opcode.ADD,
        destination=Register.R1,
        source=Register.R2,
    )

    write_instruction(
        instruction_memory,
        (0, 0, 0, 0),
        add.encode()[0],
    )

    decoded, result = cpu.step()

    assert decoded["opcode"] == Opcode.ADD
    assert result == (0, 1, 0, 1)

    assert read_register(
        cpu,
        (0, 1),
    ) == (0, 1, 0, 1)

    assert read_pc(cpu) == (0, 0, 0, 1)


# ============================================================
# STEP - LOAD / STORE
# ============================================================


def test_cpu_step_store_then_load():
    instruction_memory = InstructionMemory()

    cpu = CPU(
        instruction_memory
    )

    # R1 = 1010
    cpu.cycle.datapath.register_file.update(
        write_address=(0, 1),
        write_data=(1, 0, 1, 0),
        write_enable=1,
        read_address_a=(0, 1),
        read_address_b=(0, 1),
        clock=0,
    )

    cpu.cycle.datapath.register_file.update(
        write_address=(0, 1),
        write_data=(1, 0, 1, 0),
        write_enable=1,
        read_address_a=(0, 1),
        read_address_b=(0, 1),
        clock=1,
    )

    store = Instruction(
        Opcode.STORE,
        source=Register.R1,
        address=6,
    )

    load = Instruction(
        Opcode.LOAD,
        destination=Register.R2,
        address=6,
    )

    write_two_word_instruction(
        instruction_memory,
        (0, 0, 0, 0),
        store,
    )

    write_two_word_instruction(
        instruction_memory,
        (0, 0, 1, 0),
        load,
    )

    decoded, _ = cpu.step()

    assert decoded["opcode"] == Opcode.STORE
    assert read_pc(cpu) == (0, 0, 1, 0)

    decoded, result = cpu.step()

    assert decoded["opcode"] == Opcode.LOAD
    assert result == (1, 0, 1, 0)

    assert read_register(
        cpu,
        (1, 0),
    ) == (1, 0, 1, 0)

    assert read_pc(cpu) == (0, 1, 0, 0)


# ============================================================
# JUMP
# ============================================================


def test_cpu_step_jump():
    instruction_memory = InstructionMemory()

    cpu = CPU(
        instruction_memory
    )

    jump = Instruction(
        Opcode.JUMP,
        address=10,
    )

    write_instruction(
        instruction_memory,
        (0, 0, 0, 0),
        jump.encode()[0],
    )

    decoded, result = cpu.step()

    assert decoded["opcode"] == Opcode.JUMP
    assert result is None

    assert read_pc(cpu) == (1, 0, 1, 0)


# ============================================================
# HALT
# ============================================================


def test_cpu_step_halt():
    instruction_memory = InstructionMemory()

    cpu = CPU(
        instruction_memory
    )

    halt = Instruction(
        Opcode.HALT,
    )

    write_instruction(
        instruction_memory,
        (0, 0, 0, 0),
        halt.encode()[0],
    )

    decoded, result = cpu.step()

    assert decoded["opcode"] == Opcode.HALT
    assert result is None

    assert cpu.cycle.halted is True
    assert read_pc(cpu) == (0, 0, 0, 0)


def test_cpu_step_after_halt():
    instruction_memory = InstructionMemory()

    cpu = CPU(
        instruction_memory
    )

    halt = Instruction(
        Opcode.HALT,
    )

    write_instruction(
        instruction_memory,
        (0, 0, 0, 0),
        halt.encode()[0],
    )

    cpu.step()

    result = cpu.step()

    assert result == (None, None)

    assert read_pc(cpu) == (0, 0, 0, 0)


# ============================================================
# RUN
# ============================================================


def test_cpu_run_until_halt():
    instruction_memory = InstructionMemory()

    cpu = CPU(
        instruction_memory
    )

    halt = Instruction(
        Opcode.HALT,
    )

    write_instruction(
        instruction_memory,
        (0, 0, 0, 0),
        halt.encode()[0],
    )

    instruction_count = cpu.run()

    assert instruction_count == 1
    assert cpu.cycle.halted is True
    assert read_pc(cpu) == (0, 0, 0, 0)


def test_cpu_run_multiple_instructions():
    instruction_memory = InstructionMemory()

    cpu = CPU(
        instruction_memory
    )

    jump = Instruction(
        Opcode.JUMP,
        address=2,
    )

    halt = Instruction(
        Opcode.HALT,
    )

    write_instruction(
        instruction_memory,
        (0, 0, 0, 0),
        jump.encode()[0],
    )

    write_instruction(
        instruction_memory,
        (0, 0, 0, 1),
        halt.encode()[0],
    )

    write_instruction(
        instruction_memory,
        (0, 0, 1, 0),
        halt.encode()[0],
    )

    instruction_count = cpu.run()

    assert instruction_count == 2
    assert cpu.cycle.halted is True
    assert read_pc(cpu) == (0, 0, 1, 0)