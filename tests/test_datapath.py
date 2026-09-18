import pytest

from astra.cpu.datapath import Datapath
from astra.isa.instructions import Instruction, Opcode, Register


def write_register(
    datapath: Datapath,
    register: Register,
    value: tuple[int, int, int, int]
) -> None:
    """
    Write a 4-bit value into a register.

    A complete clock cycle is used so that the master-slave
    D flip-flop captures the value correctly.

    Clock sequence:

        0 -> master captures data
        1 -> slave captures master
    """

    address = (
        register.value // 2,
        register.value % 2
    )

    datapath.register_file.update(
        write_address=address,
        write_data=value,
        write_enable=1,
        read_address_a=address,
        read_address_b=address,
        clock=0
    )

    datapath.register_file.update(
        write_address=address,
        write_data=value,
        write_enable=1,
        read_address_a=address,
        read_address_b=address,
        clock=1
    )


def read_register(
    datapath: Datapath,
    register: Register
) -> tuple[int, int, int, int]:
    """
    Read the current value of a register.
    """

    address = (
        register.value // 2,
        register.value % 2
    )

    read_data_a, _ = datapath.register_file.read(
        read_address_a=address,
        read_address_b=address
    )

    return read_data_a


def test_add():
    """
    Test:

        R0 = 0011
        R1 = 0101

        ADD R0, R1

        R0 = 1000
    """

    datapath = Datapath()

    write_register(
        datapath,
        Register.R0,
        (0, 0, 1, 1)
    )

    write_register(
        datapath,
        Register.R1,
        (0, 1, 0, 1)
    )

    instruction = Instruction(
        Opcode.ADD,
        destination=Register.R0,
        source=Register.R1
    )

    result = datapath.execute(instruction, 0)

    assert result == (1, 0, 0, 0)

    datapath.execute(instruction, 1)

    assert read_register(
        datapath,
        Register.R0
    ) == (1, 0, 0, 0)


def test_sub():
    """
    Test:

        R0 = 0101
        R1 = 0001

        SUB R0, R1

        R0 = 0100
    """

    datapath = Datapath()

    write_register(
        datapath,
        Register.R0,
        (0, 1, 0, 1)
    )

    write_register(
        datapath,
        Register.R1,
        (0, 0, 0, 1)
    )

    instruction = Instruction(
        Opcode.SUB,
        destination=Register.R0,
        source=Register.R1
    )

    result = datapath.execute(instruction, 0)

    assert result == (0, 1, 0, 0)

    datapath.execute(instruction, 1)

    assert read_register(
        datapath,
        Register.R0
    ) == (0, 1, 0, 0)


def test_and():
    """
    Test:

        R0 = 1100
        R1 = 1010

        AND R0, R1

        R0 = 1000
    """

    datapath = Datapath()

    write_register(
        datapath,
        Register.R0,
        (1, 1, 0, 0)
    )

    write_register(
        datapath,
        Register.R1,
        (1, 0, 1, 0)
    )

    instruction = Instruction(
        Opcode.AND,
        destination=Register.R0,
        source=Register.R1
    )

    result = datapath.execute(instruction, 0)

    assert result == (1, 0, 0, 0)

    datapath.execute(instruction, 1)

    assert read_register(
        datapath,
        Register.R0
    ) == (1, 0, 0, 0)


def test_or():
    """
    Test:

        R0 = 1100
        R1 = 1010

        OR R0, R1

        R0 = 1110
    """

    datapath = Datapath()

    write_register(
        datapath,
        Register.R0,
        (1, 1, 0, 0)
    )

    write_register(
        datapath,
        Register.R1,
        (1, 0, 1, 0)
    )

    instruction = Instruction(
        Opcode.OR,
        destination=Register.R0,
        source=Register.R1
    )

    result = datapath.execute(instruction, 0)

    assert result == (1, 1, 1, 0)

    datapath.execute(instruction, 1)

    assert read_register(
        datapath,
        Register.R0
    ) == (1, 1, 1, 0)


def test_xor():
    """
    Test:

        R0 = 1100
        R1 = 1010

        XOR R0, R1

        R0 = 0110
    """

    datapath = Datapath()

    write_register(
        datapath,
        Register.R0,
        (1, 1, 0, 0)
    )

    write_register(
        datapath,
        Register.R1,
        (1, 0, 1, 0)
    )

    instruction = Instruction(
        Opcode.XOR,
        destination=Register.R0,
        source=Register.R1
    )

    result = datapath.execute(instruction, 0)

    assert result == (0, 1, 1, 0)

    datapath.execute(instruction, 1)

    assert read_register(
        datapath,
        Register.R0
    ) == (0, 1, 1, 0)


def test_not():
    """
    Test:

        R0 = 1010

        NOT R0

        R0 = 0101
    """

    datapath = Datapath()

    write_register(
        datapath,
        Register.R0,
        (1, 0, 1, 0)
    )

    instruction = Instruction(
        Opcode.NOT,
        destination=Register.R0
    )

    result = datapath.execute(instruction, 0)

    assert result == (0, 1, 0, 1)

    datapath.execute(instruction, 1)

    assert read_register(
        datapath,
        Register.R0
    ) == (0, 1, 0, 1)


def test_destination_register_is_updated():
    """
    Verify that the ALU result is written to the destination
    register and the source register remains unchanged.
    """

    datapath = Datapath()

    write_register(
        datapath,
        Register.R0,
        (0, 0, 1, 1)
    )

    write_register(
        datapath,
        Register.R1,
        (0, 1, 0, 1)
    )

    instruction = Instruction(
        Opcode.ADD,
        destination=Register.R0,
        source=Register.R1
    )

    datapath.execute(instruction, 0)
    datapath.execute(instruction, 1)

    assert read_register(
        datapath,
        Register.R0
    ) == (1, 0, 0, 0)

    assert read_register(
        datapath,
        Register.R1
    ) == (0, 1, 0, 1)


def test_registers_are_read_without_clock():
    """
    Verify that RegisterFile reads are combinational.

    Reading registers should return their current values
    regardless of the clock signal.
    """

    datapath = Datapath()

    write_register(
        datapath,
        Register.R0,
        (1, 0, 1, 0)
    )

    write_register(
        datapath,
        Register.R1,
        (0, 1, 0, 1)
    )

    address_r0 = (0, 0)
    address_r1 = (0, 1)

    read_a, read_b = datapath.register_file.read(
        read_address_a=address_r0,
        read_address_b=address_r1
    )

    assert read_a == (1, 0, 1, 0)
    assert read_b == (0, 1, 0, 1)


def test_unsupported_load():
    """
    LOAD is not yet supported by this datapath.
    """

    datapath = Datapath()

    instruction = Instruction(
        Opcode.LOAD,
        destination=Register.R0,
        address=5
    )

    with pytest.raises(ValueError):
        datapath.execute(instruction, 0)


def test_unsupported_store():
    """
    STORE is not yet supported by this datapath.
    """

    datapath = Datapath()

    instruction = Instruction(
        Opcode.STORE,
        source=Register.R0,
        address=5
    )

    with pytest.raises(ValueError):
        datapath.execute(instruction, 0)


def test_unsupported_jump():
    """
    JUMP is not yet supported by this datapath.
    """

    datapath = Datapath()

    instruction = Instruction(
        Opcode.JUMP,
        address=5
    )

    with pytest.raises(ValueError):
        datapath.execute(instruction, 0)


def test_unsupported_halt():
    """
    HALT is not yet supported by this datapath.
    """

    datapath = Datapath()

    instruction = Instruction(
        Opcode.HALT
    )

    with pytest.raises(ValueError):
        datapath.execute(instruction, 0)


def test_invalid_instruction_type():
    """
    Verify that the datapath rejects invalid instruction types.
    """

    datapath = Datapath()

    with pytest.raises(TypeError):
        datapath.execute(5, 0)