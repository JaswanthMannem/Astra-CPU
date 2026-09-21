import pytest

from astra.cpu.cpu import CPU
from astra.cpu.instruction_memory import InstructionMemory
from astra.cpu.program_loader import ProgramLoader
from astra.isa.instructions import Instruction, Opcode, Register


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


def write_register(
    cpu,
    address,
    value,
):
    cpu.cycle.datapath.register_file.update(
        write_address=address,
        write_data=value,
        write_enable=1,
        read_address_a=address,
        read_address_b=address,
        clock=0,
    )

    cpu.cycle.datapath.register_file.update(
        write_address=address,
        write_data=value,
        write_enable=1,
        read_address_a=address,
        read_address_b=address,
        clock=1,
    )


# ============================================================
# Basic program execution
# ============================================================


def test_program_executes_until_halt():

    memory = InstructionMemory()

    loader = ProgramLoader(memory)

    program = [
        Instruction(
            Opcode.HALT,
        ),
    ]

    loader.load(program)

    cpu = CPU(memory)

    instruction_count = cpu.run()

    assert instruction_count == 1
    assert cpu.cycle.halted is True
    assert read_pc(cpu) == (0, 0, 0, 0)


# ============================================================
# ALU program
# ============================================================


def test_program_executes_multiple_alu_instructions():

    memory = InstructionMemory()

    loader = ProgramLoader(memory)

    program = [
        Instruction(
            Opcode.ADD,
            destination=Register.R1,
            source=Register.R2,
        ),
        Instruction(
            Opcode.SUB,
            destination=Register.R1,
            source=Register.R2,
        ),
        Instruction(
            Opcode.HALT,
        ),
    ]

    loader.load(program)

    cpu = CPU(memory)

    # R1 = 0011
    write_register(
        cpu,
        (0, 1),
        (0, 0, 1, 1),
    )

    # R2 = 0010
    write_register(
        cpu,
        (1, 0),
        (0, 0, 1, 0),
    )

    instruction_count = cpu.run()

    assert instruction_count == 3

    assert read_register(
        cpu,
        (0, 1),
    ) == (0, 0, 1, 1)

    # ADD -> PC 1
    # SUB -> PC 2
    # HALT -> PC remains 2
    assert read_pc(cpu) == (0, 0, 1, 0)


# ============================================================
# STORE -> LOAD
# ============================================================


def test_program_store_then_load():

    memory = InstructionMemory()

    loader = ProgramLoader(memory)

    program = [
        Instruction(
            Opcode.STORE,
            source=Register.R1,
            address=6,
        ),
        Instruction(
            Opcode.LOAD,
            destination=Register.R2,
            address=6,
        ),
        Instruction(
            Opcode.HALT,
        ),
    ]

    loader.load(program)

    cpu = CPU(memory)

    # R1 = 1010
    write_register(
        cpu,
        (0, 1),
        (1, 0, 1, 0),
    )

    instruction_count = cpu.run()

    assert instruction_count == 3

    assert read_register(
        cpu,
        (1, 0),
    ) == (1, 0, 1, 0)

    # STORE occupies addresses 0,1
    # LOAD occupies addresses 2,3
    # HALT is at address 4
    # HALT does not increment PC.
    assert read_pc(cpu) == (0, 1, 0, 0)


# ============================================================
# LOAD -> ADD
# ============================================================


def test_program_load_then_add():

    memory = InstructionMemory()

    loader = ProgramLoader(memory)

    program = [
        Instruction(
            Opcode.LOAD,
            destination=Register.R1,
            address=5,
        ),
        Instruction(
            Opcode.ADD,
            destination=Register.R1,
            source=Register.R2,
        ),
        Instruction(
            Opcode.HALT,
        ),
    ]

    loader.load(program)

    cpu = CPU(memory)

    # M[5] = 0011
    cpu.cycle.data_memory.update(
        address=(0, 1, 0, 1),
        data=(0, 0, 1, 1),
        write_enable=1,
        clock=0,
    )

    cpu.cycle.data_memory.update(
        address=(0, 1, 0, 1),
        data=(0, 0, 1, 1),
        write_enable=1,
        clock=1,
    )

    # R2 = 0010
    write_register(
        cpu,
        (1, 0),
        (0, 0, 1, 0),
    )

    instruction_count = cpu.run()

    assert instruction_count == 3

    # LOAD: M[5] = 0011
    # ADD: 0011 + 0010 = 0101
    assert read_register(
        cpu,
        (0, 1),
    ) == (0, 1, 0, 1)

    # LOAD occupies addresses 0,1
    # ADD is address 2
    # HALT is address 3
    # HALT does not increment PC.
    assert read_pc(cpu) == (0, 0, 1, 1)


# ============================================================
# JUMP
# ============================================================


def test_program_jump_skips_instruction():

    memory = InstructionMemory()

    loader = ProgramLoader(memory)

    program = [
        Instruction(
            Opcode.JUMP,
            address=3,
        ),
        Instruction(
            Opcode.ADD,
            destination=Register.R1,
            source=Register.R2,
        ),
        Instruction(
            Opcode.ADD,
            destination=Register.R1,
            source=Register.R2,
        ),
        Instruction(
            Opcode.HALT,
        ),
    ]

    loader.load(program)

    cpu = CPU(memory)

    write_register(
        cpu,
        (0, 1),
        (0, 0, 1, 1),
    )

    write_register(
        cpu,
        (1, 0),
        (0, 0, 1, 0),
    )

    instruction_count = cpu.run()

    assert instruction_count == 2

    # ADD instructions at addresses 1 and 2
    # were skipped.
    assert read_register(
        cpu,
        (0, 1),
    ) == (0, 0, 1, 1)

    # JUMP -> address 3
    # HALT stays at address 3.
    assert read_pc(cpu) == (0, 0, 1, 1)


# ============================================================
# JUMP -> ALU -> HALT
# ============================================================


def test_program_jump_then_execute_target():

    memory = InstructionMemory()

    loader = ProgramLoader(memory)

    program = [
        Instruction(
            Opcode.JUMP,
            address=2,
        ),
        Instruction(
            Opcode.HALT,
        ),
        Instruction(
            Opcode.ADD,
            destination=Register.R1,
            source=Register.R2,
        ),
        Instruction(
            Opcode.HALT,
        ),
    ]

    loader.load(program)

    cpu = CPU(memory)

    write_register(
        cpu,
        (0, 1),
        (0, 0, 1, 1),
    )

    write_register(
        cpu,
        (1, 0),
        (0, 0, 1, 0),
    )

    instruction_count = cpu.run()

    assert instruction_count == 3

    # JUMP -> address 2
    # ADD -> R1 = 0011 + 0010 = 0101
    # HALT -> address 3
    assert read_register(
        cpu,
        (0, 1),
    ) == (0, 1, 0, 1)

    assert read_pc(cpu) == (0, 0, 1, 1)