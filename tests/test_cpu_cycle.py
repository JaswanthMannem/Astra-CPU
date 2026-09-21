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


def read_pc(cpu):
    return tuple(
        register.dff.slave.latch.q
        for register in cpu.program_counter.register.registers
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
        (bits_to_int(address) + 1) % 16
    )

    write_instruction(
        memory,
        next_address,
        encoded[1],
    )


# ============================================================
# Initialization
# ============================================================


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
    assert cpu.data_memory is not None


def test_cpu_cycle_initial_pc_is_zero():
    instruction_memory = InstructionMemory()

    cpu = CPUCycle(
        instruction_memory
    )

    assert read_pc(cpu) == (0, 0, 0, 0)


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
        CPUCycle(None)


# ============================================================
# ALU instructions
# ============================================================


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


# ============================================================
# Program Counter
# ============================================================


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

    assert read_pc(cpu) == (0, 0, 0, 1)


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
    assert read_pc(cpu) == (0, 0, 0, 1)

    cpu.cycle(clock=0)
    cpu.cycle(clock=1)

    r1_after_sub = read_register(
        cpu.datapath.register_file,
        (0, 1),
    )

    assert r1_after_sub == (0, 0, 1, 1)
    assert read_pc(cpu) == (0, 0, 1, 0)


# ============================================================
# STORE
# ============================================================


def test_cpu_cycle_store():
    instruction_memory = InstructionMemory()

    cpu = CPUCycle(
        instruction_memory
    )

    # R1 = 1010
    write_register(
        cpu.datapath.register_file,
        (0, 1),
        (1, 0, 1, 0),
    )

    store = Instruction(
        Opcode.STORE,
        source=Register.R1,
        address=5,
    )

    write_two_word_instruction(
        instruction_memory,
        (0, 0, 0, 0),
        store,
    )

    decoded, result = cpu.cycle(
        clock=0
    )

    cpu.cycle(
        clock=1
    )

    assert decoded["opcode"] == Opcode.STORE
    assert decoded["source"] == Register.R1
    assert decoded["address"] == 5

    memory_value = cpu.data_memory.update(
        address=(0, 1, 0, 1),
        data=(0, 0, 0, 0),
        write_enable=0,
        clock=0,
    )

    assert memory_value == (1, 0, 1, 0)


def test_cpu_cycle_store_does_not_modify_source_register():
    instruction_memory = InstructionMemory()

    cpu = CPUCycle(
        instruction_memory
    )

    original_value = (1, 0, 1, 1)

    write_register(
        cpu.datapath.register_file,
        (1, 0),
        original_value,
    )

    store = Instruction(
        Opcode.STORE,
        source=Register.R2,
        address=12,
    )

    write_two_word_instruction(
        instruction_memory,
        (0, 0, 0, 0),
        store,
    )

    cpu.cycle(clock=0)
    cpu.cycle(clock=1)

    r2 = read_register(
        cpu.datapath.register_file,
        (1, 0),
    )

    assert r2 == original_value


def test_cpu_cycle_store_high_memory_address():
    instruction_memory = InstructionMemory()

    cpu = CPUCycle(
        instruction_memory
    )

    write_register(
        cpu.datapath.register_file,
        (1, 1),
        (0, 1, 1, 1),
    )

    store = Instruction(
        Opcode.STORE,
        source=Register.R3,
        address=15,
    )

    write_two_word_instruction(
        instruction_memory,
        (0, 0, 0, 0),
        store,
    )

    cpu.cycle(clock=0)
    cpu.cycle(clock=1)

    memory_value = cpu.data_memory.update(
        address=(1, 1, 1, 1),
        data=(0, 0, 0, 0),
        write_enable=0,
        clock=0,
    )

    assert memory_value == (0, 1, 1, 1)


def test_cpu_cycle_store_increments_pc_by_two():
    instruction_memory = InstructionMemory()

    cpu = CPUCycle(
        instruction_memory
    )

    store = Instruction(
        Opcode.STORE,
        source=Register.R1,
        address=10,
    )

    write_two_word_instruction(
        instruction_memory,
        (0, 0, 0, 0),
        store,
    )

    cpu.cycle(clock=0)
    cpu.cycle(clock=1)

    assert read_pc(cpu) == (0, 0, 1, 0)


# ============================================================
# LOAD
# ============================================================


def test_cpu_cycle_load():
    instruction_memory = InstructionMemory()

    cpu = CPUCycle(
        instruction_memory
    )

    # M[7] = 1101
    cpu.data_memory.update(
        address=(0, 1, 1, 1),
        data=(1, 1, 0, 1),
        write_enable=1,
        clock=0,
    )

    cpu.data_memory.update(
        address=(0, 1, 1, 1),
        data=(1, 1, 0, 1),
        write_enable=1,
        clock=1,
    )

    load = Instruction(
        Opcode.LOAD,
        destination=Register.R2,
        address=7,
    )

    write_two_word_instruction(
        instruction_memory,
        (0, 0, 0, 0),
        load,
    )

    decoded, result = cpu.cycle(
        clock=0
    )

    cpu.cycle(
        clock=1
    )

    assert decoded["opcode"] == Opcode.LOAD
    assert decoded["destination"] == Register.R2
    assert decoded["address"] == 7

    assert result == (1, 1, 0, 1)

    r2 = read_register(
        cpu.datapath.register_file,
        (1, 0),
    )

    assert r2 == (1, 1, 0, 1)


def test_cpu_cycle_load_writes_destination_register():
    instruction_memory = InstructionMemory()

    cpu = CPUCycle(
        instruction_memory
    )

    # R1 must remain unchanged.
    write_register(
        cpu.datapath.register_file,
        (0, 1),
        (0, 0, 1, 1),
    )

    # M[9] = 1110
    cpu.data_memory.update(
        address=(1, 0, 0, 1),
        data=(1, 1, 1, 0),
        write_enable=1,
        clock=0,
    )

    cpu.data_memory.update(
        address=(1, 0, 0, 1),
        data=(1, 1, 1, 0),
        write_enable=1,
        clock=1,
    )

    load = Instruction(
        Opcode.LOAD,
        destination=Register.R3,
        address=9,
    )

    write_two_word_instruction(
        instruction_memory,
        (0, 0, 0, 0),
        load,
    )

    cpu.cycle(clock=0)
    cpu.cycle(clock=1)

    r1 = read_register(
        cpu.datapath.register_file,
        (0, 1),
    )

    r3 = read_register(
        cpu.datapath.register_file,
        (1, 1),
    )

    assert r1 == (0, 0, 1, 1)
    assert r3 == (1, 1, 1, 0)


def test_cpu_cycle_load_high_memory_address():
    instruction_memory = InstructionMemory()

    cpu = CPUCycle(
        instruction_memory
    )

    # M[15] = 0110
    cpu.data_memory.update(
        address=(1, 1, 1, 1),
        data=(0, 1, 1, 0),
        write_enable=1,
        clock=0,
    )

    cpu.data_memory.update(
        address=(1, 1, 1, 1),
        data=(0, 1, 1, 0),
        write_enable=1,
        clock=1,
    )

    load = Instruction(
        Opcode.LOAD,
        destination=Register.R0,
        address=15,
    )

    write_two_word_instruction(
        instruction_memory,
        (0, 0, 0, 0),
        load,
    )

    cpu.cycle(clock=0)
    cpu.cycle(clock=1)

    r0 = read_register(
        cpu.datapath.register_file,
        (0, 0),
    )

    assert r0 == (0, 1, 1, 0)


def test_cpu_cycle_load_increments_pc_by_two():
    instruction_memory = InstructionMemory()

    cpu = CPUCycle(
        instruction_memory
    )

    load = Instruction(
        Opcode.LOAD,
        destination=Register.R1,
        address=4,
    )

    write_two_word_instruction(
        instruction_memory,
        (0, 0, 0, 0),
        load,
    )

    cpu.cycle(clock=0)
    cpu.cycle(clock=1)

    assert read_pc(cpu) == (0, 0, 1, 0)


# ============================================================
# LOAD followed by ALU
# ============================================================


def test_cpu_cycle_load_then_add():
    instruction_memory = InstructionMemory()

    cpu = CPUCycle(
        instruction_memory
    )

    # M[5] = 0011
    cpu.data_memory.update(
        address=(0, 1, 0, 1),
        data=(0, 0, 1, 1),
        write_enable=1,
        clock=0,
    )

    cpu.data_memory.update(
        address=(0, 1, 0, 1),
        data=(0, 0, 1, 1),
        write_enable=1,
        clock=1,
    )

    # R2 = 0010
    write_register(
        cpu.datapath.register_file,
        (1, 0),
        (0, 0, 1, 0),
    )

    load = Instruction(
        Opcode.LOAD,
        destination=Register.R1,
        address=5,
    )

    add = Instruction(
        Opcode.ADD,
        destination=Register.R1,
        source=Register.R2,
    )

    write_two_word_instruction(
        instruction_memory,
        (0, 0, 0, 0),
        load,
    )

    add_word = add.encode()[0]

    write_instruction(
        instruction_memory,
        (0, 0, 1, 0),
        add_word,
    )

    # LOAD
    cpu.cycle(clock=0)
    cpu.cycle(clock=1)

    assert read_pc(cpu) == (0, 0, 1, 0)

    r1 = read_register(
        cpu.datapath.register_file,
        (0, 1),
    )

    assert r1 == (0, 0, 1, 1)

    # ADD
    cpu.cycle(clock=0)
    cpu.cycle(clock=1)

    r1 = read_register(
        cpu.datapath.register_file,
        (0, 1),
    )

    assert r1 == (0, 1, 0, 1)

    assert read_pc(cpu) == (0, 0, 1, 1)


# ============================================================
# STORE followed by LOAD
# ============================================================


def test_cpu_cycle_store_then_load():
    instruction_memory = InstructionMemory()

    cpu = CPUCycle(
        instruction_memory
    )

    # R1 = 1010
    write_register(
        cpu.datapath.register_file,
        (0, 1),
        (1, 0, 1, 0),
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

    # STORE
    cpu.cycle(clock=0)
    cpu.cycle(clock=1)

    assert read_pc(cpu) == (0, 0, 1, 0)

    # LOAD
    cpu.cycle(clock=0)
    cpu.cycle(clock=1)

    r2 = read_register(
        cpu.datapath.register_file,
        (1, 0),
    )

    assert r2 == (1, 0, 1, 0)

    assert read_pc(cpu) == (0, 1, 0, 0)


# ============================================================
# Multiple LOAD / STORE instructions
# ============================================================


def test_cpu_cycle_multiple_load_store_operations():
    instruction_memory = InstructionMemory()

    cpu = CPUCycle(
        instruction_memory
    )

    # R1 = 0011
    # R2 = 1100

    write_register(
        cpu.datapath.register_file,
        (0, 1),
        (0, 0, 1, 1),
    )

    write_register(
        cpu.datapath.register_file,
        (1, 0),
        (1, 1, 0, 0),
    )

    store_r1 = Instruction(
        Opcode.STORE,
        source=Register.R1,
        address=2,
    )

    store_r2 = Instruction(
        Opcode.STORE,
        source=Register.R2,
        address=14,
    )

    load_r3 = Instruction(
        Opcode.LOAD,
        destination=Register.R3,
        address=2,
    )

    load_r0 = Instruction(
        Opcode.LOAD,
        destination=Register.R0,
        address=14,
    )

    write_two_word_instruction(
        instruction_memory,
        (0, 0, 0, 0),
        store_r1,
    )

    write_two_word_instruction(
        instruction_memory,
        (0, 0, 1, 0),
        store_r2,
    )

    write_two_word_instruction(
        instruction_memory,
        (0, 1, 0, 0),
        load_r3,
    )

    write_two_word_instruction(
        instruction_memory,
        (0, 1, 1, 0),
        load_r0,
    )

    # STORE R1, 2
    cpu.cycle(clock=0)
    cpu.cycle(clock=1)

    assert read_pc(cpu) == (0, 0, 1, 0)

    # STORE R2, 14
    cpu.cycle(clock=0)
    cpu.cycle(clock=1)

    assert read_pc(cpu) == (0, 1, 0, 0)

    # LOAD R3, 2
    cpu.cycle(clock=0)
    cpu.cycle(clock=1)

    assert read_pc(cpu) == (0, 1, 1, 0)

    # LOAD R0, 14
    cpu.cycle(clock=0)
    cpu.cycle(clock=1)

    r3 = read_register(
        cpu.datapath.register_file,
        (1, 1),
    )

    r0 = read_register(
        cpu.datapath.register_file,
        (0, 0),
    )

    assert r3 == (0, 0, 1, 1)
    assert r0 == (1, 1, 0, 0)

    assert read_pc(cpu) == (1, 0, 0, 0)