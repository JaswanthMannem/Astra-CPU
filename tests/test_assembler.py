import pytest

from astra.isa.assembler import Assembler
from astra.isa.instructions import Instruction, Opcode, Register


def test_assemble_add():
    source = "ADD R1, R2"

    instructions = Assembler().assemble(source)

    assert instructions == [
        Instruction(
            opcode=Opcode.ADD,
            destination=Register.R1,
            source=Register.R2,
        )
    ]


def test_assemble_all_r_type_instructions():
    source = """
    ADD R1, R2
    SUB R1, R2
    AND R1, R2
    OR R1, R2
    XOR R1, R2
    """

    instructions = Assembler().assemble(source)

    assert instructions == [
        Instruction(Opcode.ADD, Register.R1, Register.R2),
        Instruction(Opcode.SUB, Register.R1, Register.R2),
        Instruction(Opcode.AND, Register.R1, Register.R2),
        Instruction(Opcode.OR, Register.R1, Register.R2),
        Instruction(Opcode.XOR, Register.R1, Register.R2),
    ]


def test_assemble_not():
    source = "NOT R1"

    instructions = Assembler().assemble(source)

    assert instructions == [
        Instruction(
            opcode=Opcode.NOT,
            destination=Register.R1,
        )
    ]


def test_assemble_load():
    source = "LOAD R1, 5"

    instructions = Assembler().assemble(source)

    assert instructions == [
        Instruction(
            opcode=Opcode.LOAD,
            destination=Register.R1,
            address=5,
        )
    ]


def test_assemble_store():
    source = "STORE R1, 7"

    instructions = Assembler().assemble(source)

    assert instructions == [
        Instruction(
            opcode=Opcode.STORE,
            source=Register.R1,
            address=7,
        )
    ]


def test_assemble_jump():
    source = "JUMP 10"

    instructions = Assembler().assemble(source)

    assert instructions == [
        Instruction(
            opcode=Opcode.JUMP,
            address=10,
        )
    ]


def test_assemble_halt():
    source = "HALT"

    instructions = Assembler().assemble(source)

    assert instructions == [
        Instruction(
            opcode=Opcode.HALT,
        )
    ]


def test_assemble_complete_program():
    source = """
    LOAD R1, 5
    LOAD R2, 6
    ADD R1, R2
    STORE R1, 7
    HALT
    """

    instructions = Assembler().assemble(source)

    assert instructions == [
        Instruction(
            opcode=Opcode.LOAD,
            destination=Register.R1,
            address=5,
        ),
        Instruction(
            opcode=Opcode.LOAD,
            destination=Register.R2,
            address=6,
        ),
        Instruction(
            opcode=Opcode.ADD,
            destination=Register.R1,
            source=Register.R2,
        ),
        Instruction(
            opcode=Opcode.STORE,
            source=Register.R1,
            address=7,
        ),
        Instruction(
            opcode=Opcode.HALT,
        ),
    ]


def test_assembler_ignores_blank_lines():
    source = """

    ADD R1, R2


    HALT

    """

    instructions = Assembler().assemble(source)

    assert len(instructions) == 2


def test_assembler_ignores_comments():
    source = """
    # Load value
    LOAD R1, 5

    # Add registers
    ADD R1, R2

    HALT
    """

    instructions = Assembler().assemble(source)

    assert len(instructions) == 3


def test_assembler_is_case_insensitive():
    source = """
    load r1, 5
    add r1, r2
    halt
    """

    instructions = Assembler().assemble(source)

    assert instructions == [
        Instruction(
            opcode=Opcode.LOAD,
            destination=Register.R1,
            address=5,
        ),
        Instruction(
            opcode=Opcode.ADD,
            destination=Register.R1,
            source=Register.R2,
        ),
        Instruction(
            opcode=Opcode.HALT,
        ),
    ]


def test_invalid_instruction():
    with pytest.raises(ValueError, match="unknown instruction"):
        Assembler().assemble("FOO R1, R2")


def test_invalid_register():
    with pytest.raises(ValueError, match="invalid register"):
        Assembler().assemble("ADD R4, R1")


def test_invalid_address():
    with pytest.raises(
        ValueError,
        match="address must be between 0 and 15",
    ):
        Assembler().assemble("JUMP 16")


def test_negative_address():
    with pytest.raises(
        ValueError,
        match="address must be between 0 and 15",
    ):
        Assembler().assemble("LOAD R1, -1")


def test_wrong_operand_count():
    with pytest.raises(
        ValueError,
        match="expected 2 operand",
    ):
        Assembler().assemble("ADD R1")


def test_halt_with_operand():
    with pytest.raises(
        ValueError,
        match="expected 0 operand",
    ):
        Assembler().assemble("HALT R1")


def test_jump_without_address():
    with pytest.raises(
        ValueError,
        match="expected 1 operand",
    ):
        Assembler().assemble("JUMP")


def test_load_without_address():
    with pytest.raises(
        ValueError,
        match="expected 2 operand",
    ):
        Assembler().assemble("LOAD R1")


def test_store_without_address():
    with pytest.raises(
        ValueError,
        match="expected 2 operand",
    ):
        Assembler().assemble("STORE R1")


def test_non_string_source():
    with pytest.raises(TypeError, match="source must be a string"):
        Assembler().assemble(None)