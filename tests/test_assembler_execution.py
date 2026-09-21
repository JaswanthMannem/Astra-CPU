from astra.cpu.cpu import CPU
from astra.cpu.instruction_memory import InstructionMemory
from astra.cpu.program_loader import ProgramLoader
from astra.isa.assembler import Assembler


def make_cpu(source: str) -> CPU:
    """Assemble and load an Astra assembly program into a CPU.

    Args:
        source: Astra assembly source code.

    Returns:
        CPU instance with the assembled program loaded.
    """
    instruction_memory = InstructionMemory()

    program = Assembler().assemble(source)

    ProgramLoader(instruction_memory).load(program)

    return CPU(instruction_memory)


def read_register(
    cpu: CPU,
    address: tuple[int, int],
) -> tuple[int, int, int, int]:
    """Read a four-bit value from the CPU register file.

    Args:
        cpu: CPU instance.
        address: Two-bit register address.

    Returns:
        Four-bit register value.
    """
    values = cpu.cycle.datapath.register_file.read(
        read_address_a=address,
        read_address_b=address,
    )

    return values[0]


def read_memory(
    cpu: CPU,
    address: tuple[int, int, int, int],
) -> tuple[int, int, int, int]:
    """Read a four-bit value from data memory.

    Args:
        cpu: CPU instance.
        address: Four-bit memory address.

    Returns:
        Four-bit memory value.
    """
    return cpu.cycle.data_memory.update(
        address=address,
        data=(0, 0, 0, 0),
        write_enable=0,
        clock=0,
    )


def write_memory(
    cpu: CPU,
    address: tuple[int, int, int, int],
    data: tuple[int, int, int, int],
) -> None:
    """Write a four-bit value into data memory.

    Args:
        cpu: CPU instance.
        address: Four-bit memory address.
        data: Four-bit value to write.
    """
    cpu.cycle.data_memory.update(
        address=address,
        data=data,
        write_enable=1,
        clock=0,
    )

    cpu.cycle.data_memory.update(
        address=address,
        data=data,
        write_enable=1,
        clock=1,
    )


def test_assemble_and_execute_load_add_store():
    """Execute LOAD, ADD, STORE, and HALT from assembly source."""
    source = """
    LOAD R1, 5
    LOAD R2, 6
    ADD R1, R2
    STORE R1, 7
    HALT
    """

    cpu = make_cpu(source)

    write_memory(
        cpu,
        (0, 1, 0, 1),
        (0, 1, 0, 1),
    )

    write_memory(
        cpu,
        (0, 1, 1, 0),
        (0, 1, 1, 0),
    )

    instruction_count = cpu.run()

    assert instruction_count == 5

    assert read_register(cpu, (0, 1)) == (1, 0, 1, 1)
    assert read_register(cpu, (1, 0)) == (0, 1, 1, 0)

    assert read_memory(
        cpu,
        (0, 1, 1, 1),
    ) == (1, 0, 1, 1)

    assert cpu.cycle.halted is True


def test_assemble_and_execute_sub():
    """Execute subtraction through the assembly interface."""
    source = """
    LOAD R1, 5
    LOAD R2, 6
    SUB R1, R2
    HALT
    """

    cpu = make_cpu(source)

    write_memory(
        cpu,
        (0, 1, 0, 1),
        (0, 1, 0, 1),
    )

    write_memory(
        cpu,
        (0, 1, 1, 0),
        (0, 0, 1, 0),
    )

    cpu.run()

    # 5 - 2 = 3
    assert read_register(cpu, (0, 1)) == (0, 0, 1, 1)


def test_assemble_and_execute_logical_operations():
    """Execute AND, OR, and XOR instructions from assembly."""
    source = """
    LOAD R1, 5
    LOAD R2, 6
    AND R1, R2
    OR R1, R2
    XOR R1, R2
    HALT
    """

    cpu = make_cpu(source)

    write_memory(
        cpu,
        (0, 1, 0, 1),
        (1, 0, 1, 0),
    )

    write_memory(
        cpu,
        (0, 1, 1, 0),
        (1, 1, 0, 0),
    )

    cpu.run()

    # 1010 AND 1100 = 1000
    # 1000 OR  1100 = 1100
    # 1100 XOR 1100 = 0000
    assert read_register(cpu, (0, 1)) == (0, 0, 0, 0)


def test_assemble_and_execute_not():
    """Execute a NOT instruction from assembly."""
    source = """
    LOAD R1, 5
    NOT R1
    HALT
    """

    cpu = make_cpu(source)

    write_memory(
        cpu,
        (0, 1, 0, 1),
        (1, 0, 1, 0),
    )

    cpu.run()

    # NOT 1010 = 0101
    assert read_register(cpu, (0, 1)) == (0, 1, 0, 1)


def test_assemble_and_execute_jump():
    """Verify that assembly JUMP skips an instruction."""
    source = """
    JUMP 3
    LOAD R1, 5
    ADD R1, R2
    LOAD R1, 6
    HALT
    """

    cpu = make_cpu(source)

    cpu.run()

    # JUMP 3 skips addresses 1 and 2.
    # LOAD at address 3 executes.
    #
    # Memory[6] is initially zero.
    assert read_register(cpu, (0, 1)) == (0, 0, 0, 0)

    assert cpu.cycle.halted is True


def test_assemble_and_execute_comments():
    """Verify that comments and blank lines are ignored."""
    source = """
    # Load first value.
    LOAD R1, 5

    # Load second value.
    LOAD R2, 6

    # Add values.
    ADD R1, R2

    # Stop execution.
    HALT
    """

    cpu = make_cpu(source)

    write_memory(
        cpu,
        (0, 1, 0, 1),
        (0, 0, 1, 1),
    )

    write_memory(
        cpu,
        (0, 1, 1, 0),
        (0, 0, 1, 0),
    )

    cpu.run()

    # 3 + 2 = 5
    assert read_register(cpu, (0, 1)) == (0, 1, 0, 1)


def test_assemble_reset_and_execute_again():
    """Verify that an assembled program can execute after reset."""
    source = """
    LOAD R1, 5
    HALT
    """

    cpu = make_cpu(source)

    write_memory(
        cpu,
        (0, 1, 0, 1),
        (1, 0, 1, 0),
    )

    first_count = cpu.run()

    assert first_count == 2
    assert read_register(cpu, (0, 1)) == (1, 0, 1, 0)

    cpu.reset()

    assert cpu.cycle.halted is False
    assert read_register(cpu, (0, 1)) == (0, 0, 0, 0)

    # Reset clears data memory, so Memory[5] is now zero.
    second_count = cpu.run()

    assert second_count == 2
    assert read_register(cpu, (0, 1)) == (0, 0, 0, 0)