from pathlib import Path

from astra.cpu.cpu import CPU
from astra.cpu.program_loader import ProgramLoader
from astra.cpu.instruction_memory import InstructionMemory
from astra.isa.assembler import Assembler


EXAMPLES_DIR = Path(__file__).parent.parent / "examples"


def run_example(filename: str) -> CPU:
    source = (EXAMPLES_DIR / filename).read_text()

    assembler = Assembler()
    program = assembler.assemble(source)

    instruction_memory = InstructionMemory()
    loader = ProgramLoader(instruction_memory)
    loader.load(program)

    cpu = CPU(instruction_memory)
    cpu.reset()

    return cpu


def read_register(cpu: CPU, register_index: int) -> tuple[int, int, int, int]:
    address = (
        (register_index // 2) // 2,
        (register_index // 2) % 2,
        register_index % 2,
    )

    # RegisterFile uses a 2-bit address.
    address = (
        (register_index // 2),
        (register_index % 2),
    )

    return cpu.cycle.datapath.register_file.read(
        read_address_a=address,
        read_address_b=address,
    )[0]


def bits_to_int(bits: tuple[int, int, int, int]) -> int:
    return (
        bits[0] * 8
        + bits[1] * 4
        + bits[2] * 2
        + bits[3]
    )


def read_memory(cpu: CPU, address: int) -> tuple[int, int, int, int]:
    address_bits = (
        (address // 8) % 2,
        (address // 4) % 2,
        (address // 2) % 2,
        address % 2,
    )

    return cpu.cycle.data_memory.update(
        address=address_bits,
        data=(0, 0, 0, 0),
        write_enable=0,
        clock=0,
    )


def test_add_example() -> None:
    cpu = run_example("add.asm")

    # R0 = 5, R1 = 3
    register_file = cpu.cycle.datapath.register_file

    register_file.update(
        write_address=(0, 0),
        write_data=(0, 1, 0, 1),
        write_enable=1,
        read_address_a=(0, 0),
        read_address_b=(0, 0),
        clock=0,
    )
    register_file.update(
        write_address=(0, 0),
        write_data=(0, 1, 0, 1),
        write_enable=1,
        read_address_a=(0, 0),
        read_address_b=(0, 0),
        clock=1,
    )

    register_file.update(
        write_address=(0, 1),
        write_data=(0, 0, 1, 1),
        write_enable=1,
        read_address_a=(0, 1),
        read_address_b=(0, 1),
        clock=0,
    )
    register_file.update(
        write_address=(0, 1),
        write_data=(0, 0, 1, 1),
        write_enable=1,
        read_address_a=(0, 1),
        read_address_b=(0, 1),
        clock=1,
    )

    cpu.run()

    result = register_file.read(
        read_address_a=(0, 0),
        read_address_b=(0, 0),
    )[0]

    assert bits_to_int(result) == 8


def test_subtract_example() -> None:
    cpu = run_example("subtract.asm")

    register_file = cpu.cycle.datapath.register_file

    # R0 = 5
    register_file.update(
        write_address=(0, 0),
        write_data=(0, 1, 0, 1),
        write_enable=1,
        read_address_a=(0, 0),
        read_address_b=(0, 0),
        clock=0,
    )
    register_file.update(
        write_address=(0, 0),
        write_data=(0, 1, 0, 1),
        write_enable=1,
        read_address_a=(0, 0),
        read_address_b=(0, 0),
        clock=1,
    )

    # R1 = 2
    register_file.update(
        write_address=(0, 1),
        write_data=(0, 0, 1, 0),
        write_enable=1,
        read_address_a=(0, 1),
        read_address_b=(0, 1),
        clock=0,
    )
    register_file.update(
        write_address=(0, 1),
        write_data=(0, 0, 1, 0),
        write_enable=1,
        read_address_a=(0, 1),
        read_address_b=(0, 1),
        clock=1,
    )

    cpu.run()

    result = register_file.read(
        read_address_a=(0, 0),
        read_address_b=(0, 0),
    )[0]

    assert bits_to_int(result) == 3


def test_load_store_example() -> None:
    cpu = run_example("load_store.asm")

    # Initialize:
    # MEM[3] = 5
    # R1 = 2
    address = (0, 0, 1, 1)

    cpu.cycle.data_memory.update(
        address=address,
        data=(0, 1, 0, 1),
        write_enable=1,
        clock=0,
    )
    cpu.cycle.data_memory.update(
        address=address,
        data=(0, 1, 0, 1),
        write_enable=1,
        clock=1,
    )

    cpu.cycle.datapath.register_file.update(
        write_address=(0, 1),
        write_data=(0, 0, 1, 0),
        write_enable=1,
        read_address_a=(0, 1),
        read_address_b=(0, 1),
        clock=0,
    )
    cpu.cycle.datapath.register_file.update(
        write_address=(0, 1),
        write_data=(0, 0, 1, 0),
        write_enable=1,
        read_address_a=(0, 1),
        read_address_b=(0, 1),
        clock=1,
    )

    cpu.run()

    # 5 + 2 = 7, stored at MEM[4].
    result = cpu.cycle.data_memory.update(
        address=(0, 1, 0, 0),
        data=(0, 0, 0, 0),
        write_enable=0,
        clock=0,
    )

    assert bits_to_int(result) == 7


def test_jump_example() -> None:
    cpu = run_example("jump.asm")

    cpu.run()

    assert cpu.cycle.halted is True

    pc = tuple(
        register.dff.slave.latch.q
        for register in cpu.cycle.program_counter.register.registers
    )

    assert bits_to_int(pc) == 2


def test_labels_example() -> None:
    cpu = run_example("labels.asm")

    cpu.run()

    assert cpu.cycle.halted is True

    pc = tuple(
        register.dff.slave.latch.q
        for register in cpu.cycle.program_counter.register.registers
    )

    assert bits_to_int(pc) == 2