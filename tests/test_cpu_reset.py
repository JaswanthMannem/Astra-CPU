from astra.cpu.cpu import CPU
from astra.cpu.instruction_memory import InstructionMemory
from astra.cpu.program_loader import ProgramLoader
from astra.isa.instructions import Instruction, Opcode, Register


def read_register(cpu, address):
    values = cpu.cycle.datapath.register_file.read(
        read_address_a=address,
        read_address_b=address,
    )
    return values[0]


def read_pc(cpu):
    return tuple(
        register.dff.slave.latch.q
        for register in cpu.cycle.program_counter.register.registers
    )


def read_memory(cpu, address):
    return cpu.cycle.data_memory.update(
        address=address,
        data=(0, 0, 0, 0),
        write_enable=0,
        clock=0,
    )


def write_register(cpu, address, value):
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


def write_memory(cpu, address, value):
    cpu.cycle.data_memory.update(
        address=address,
        data=value,
        write_enable=1,
        clock=0,
    )

    cpu.cycle.data_memory.update(
        address=address,
        data=value,
        write_enable=1,
        clock=1,
    )


def make_cpu():
    instruction_memory = InstructionMemory()
    cpu = CPU(instruction_memory)

    program = [
        Instruction(
            opcode=Opcode.HALT,
        )
    ]

    ProgramLoader(instruction_memory).load(program)

    return cpu


def test_reset_clears_program_counter():
    cpu = make_cpu()

    cpu.cycle.program_counter.update(
        load_data=(1, 0, 1, 1),
        load=1,
        increment=0,
        reset=0,
        clock=0,
    )

    cpu.cycle.program_counter.update(
        load_data=(1, 0, 1, 1),
        load=1,
        increment=0,
        reset=0,
        clock=1,
    )

    assert read_pc(cpu) == (1, 0, 1, 1)

    cpu.reset()

    assert read_pc(cpu) == (0, 0, 0, 0)


def test_reset_clears_registers():
    cpu = make_cpu()

    write_register(
        cpu,
        (0, 1),
        (1, 0, 1, 1),
    )

    assert read_register(cpu, (0, 1)) == (1, 0, 1, 1)

    cpu.reset()

    assert read_register(cpu, (0, 1)) == (0, 0, 0, 0)


def test_reset_clears_data_memory():
    cpu = make_cpu()

    address = (1, 0, 1, 0)
    value = (1, 1, 0, 1)

    write_memory(cpu, address, value)

    assert read_memory(cpu, address) == value

    cpu.reset()

    assert read_memory(cpu, address) == (0, 0, 0, 0)


def test_reset_clears_halt_state():
    cpu = make_cpu()

    cpu.run()

    assert cpu.cycle.halted is True

    cpu.reset()

    assert cpu.cycle.halted is False


def test_reset_preserves_instruction_memory():
    instruction_memory = InstructionMemory()
    cpu = CPU(instruction_memory)

    program = [
        Instruction(
            opcode=Opcode.HALT,
        )
    ]

    ProgramLoader(instruction_memory).load(program)

    expected_instruction = (1, 0, 0, 1, 0, 0, 0, 0)

    assert instruction_memory.read((0, 0, 0, 0)) == expected_instruction

    cpu.reset()

    assert instruction_memory.read((0, 0, 0, 0)) == expected_instruction

def test_reset_allows_program_to_run_again():
    instruction_memory = InstructionMemory()
    cpu = CPU(instruction_memory)

    program = [
        Instruction(
            opcode=Opcode.HALT,
        )
    ]

    ProgramLoader(instruction_memory).load(program)

    first_count = cpu.run()

    assert first_count == 1
    assert cpu.cycle.halted is True
    assert read_pc(cpu) == (0, 0, 0, 0)

    cpu.reset()

    assert cpu.cycle.halted is False
    assert read_pc(cpu) == (0, 0, 0, 0)

    second_count = cpu.run()

    assert second_count == 1
    assert cpu.cycle.halted is True