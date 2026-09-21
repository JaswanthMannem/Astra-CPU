from astra.cpu.cpu import CPU
from astra.cpu.instruction_memory import InstructionMemory
from astra.cpu.program_loader import ProgramLoader
from astra.isa.assembler import Assembler


def make_cpu(source: str) -> CPU:
    """Assemble and load an Astra assembly program.

    Args:
        source: Astra assembly source code.

    Returns:
        CPU with the assembled program loaded.
    """
    instruction_memory = InstructionMemory()

    program = Assembler().assemble(source)

    ProgramLoader(instruction_memory).load(program)

    return CPU(instruction_memory)


def read_register(
    cpu: CPU,
    address: tuple[int, int],
) -> tuple[int, int, int, int]:
    """Read a register from the CPU register file."""
    values = cpu.cycle.datapath.register_file.read(
        read_address_a=address,
        read_address_b=address,
    )

    return values[0]


def write_memory(
    cpu: CPU,
    address: tuple[int, int, int, int],
    data: tuple[int, int, int, int],
) -> None:
    """Write a four-bit value into data memory."""
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


def read_pc(cpu: CPU) -> tuple[int, int, int, int]:
    """Read the current four-bit program counter."""
    return tuple(
        register.dff.slave.latch.q
        for register in cpu.cycle.program_counter.register.registers
    )


def test_forward_label_jump_executes_target():
    """Verify a forward label is resolved and executed by the CPU."""
    source = """
    JUMP COMPUTE

    SKIP:
        LOAD R1, 5

    COMPUTE:
        LOAD R1, 6
        HALT
    """

    cpu = make_cpu(source)

    write_memory(
        cpu,
        (0, 1, 1, 0),
        (0, 1, 0, 1),
    )

    cpu.run()

    assert read_register(cpu, (0, 1)) == (0, 1, 0, 1)
    assert cpu.cycle.halted is True


def test_backward_label_jump_executes_target():
    """Verify a backward label is resolved and executed."""
    source = """
    START:
        LOAD R1, 5
        JUMP END

    MIDDLE:
        LOAD R1, 6

    END:
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
        (0, 1, 1, 1),
    )

    cpu.run()

    # LOAD at START executes.
    # JUMP END skips MIDDLE.
    assert read_register(cpu, (0, 1)) == (1, 0, 1, 0)
    assert cpu.cycle.halted is True


def test_label_address_accounts_for_load_size():
    """Verify labels use instruction-memory word addresses."""
    source = """
    LOAD R1, 5
    JUMP TARGET

    SKIP:
        LOAD R2, 6

    TARGET:
        LOAD R2, 7
        HALT
    """

    cpu = make_cpu(source)

    write_memory(
        cpu,
        (0, 1, 0, 1),
        (0, 0, 0, 1),
    )

    write_memory(
        cpu,
        (0, 1, 1, 0),
        (0, 0, 1, 0),
    )

    write_memory(
        cpu,
        (0, 1, 1, 1),
        (1, 0, 0, 1),
    )

    cpu.run()

    # TARGET is after the two-word LOAD instructions.
    # Memory[7] = 9.
    assert read_register(cpu, (1, 0)) == (1, 0, 0, 1)
    assert cpu.cycle.halted is True


def test_labels_with_comments_and_blank_lines():
    """Verify labels work with comments and blank lines."""
    source = """
    # Start program

    START:

        # Jump to computation
        JUMP COMPUTE


    SKIP:
        LOAD R1, 5

    COMPUTE:
        LOAD R1, 6

        # Finish
        HALT
    """

    cpu = make_cpu(source)

    write_memory(
        cpu,
        (0, 1, 1, 0),
        (1, 1, 0, 0),
    )

    cpu.run()

    # COMPUTE should execute directly.
    assert read_register(cpu, (0, 1)) == (1, 1, 0, 0)
    assert cpu.cycle.halted is True


def test_reset_and_execute_label_program_again():
    """Verify a label-based program can execute after reset."""
    source = """
    START:
        LOAD R1, 5
        JUMP FINISH

    FINISH:
        HALT
    """

    cpu = make_cpu(source)

    write_memory(
        cpu,
        (0, 1, 0, 1),
        (0, 1, 1, 0),
    )

    first_count = cpu.run()

    assert first_count == 3
    assert read_register(cpu, (0, 1)) == (0, 1, 1, 0)
    assert cpu.cycle.halted is True

    cpu.reset()

    assert read_pc(cpu) == (0, 0, 0, 0)
    assert cpu.cycle.halted is False

    # Reset clears data memory.
    second_count = cpu.run()

    assert second_count == 3
    assert read_register(cpu, (0, 1)) == (0, 0, 0, 0)
    assert cpu.cycle.halted is True