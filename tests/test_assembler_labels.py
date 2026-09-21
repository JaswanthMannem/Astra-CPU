import pytest

from astra.isa.assembler import Assembler
from astra.isa.instructions import Instruction, Opcode, Register


def test_jump_to_label():
    """Resolve a JUMP target using a label."""
    source = """
    START:
        JUMP START
    """

    instructions = Assembler().assemble(source)

    assert instructions == [
        Instruction(
            opcode=Opcode.JUMP,
            address=0,
        )
    ]


def test_label_address_accounts_for_two_word_instruction():
    """Labels use instruction-memory word addresses."""
    source = """
    LOAD R1, 5
    START:
        JUMP START
    """

    instructions = Assembler().assemble(source)

    assert instructions == [
        Instruction(
            opcode=Opcode.LOAD,
            destination=Register.R1,
            address=5,
        ),
        Instruction(
            opcode=Opcode.JUMP,
            address=2,
        ),
    ]


def test_label_before_instruction():
    """Resolve a label pointing to an instruction."""
    source = """
    START:
        LOAD R1, 5
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
            opcode=Opcode.HALT,
        ),
    ]


def test_multiple_labels():
    """Resolve multiple labels in the same program."""
    source = """
    START:
        JUMP END

    MIDDLE:
        HALT

    END:
        JUMP MIDDLE
    """

    instructions = Assembler().assemble(source)

    assert instructions == [
        Instruction(
            opcode=Opcode.JUMP,
            address=2,
        ),
        Instruction(
            opcode=Opcode.HALT,
        ),
        Instruction(
            opcode=Opcode.JUMP,
            address=1,
        ),
    ]


def test_label_on_same_line_as_instruction():
    """Allow a label and instruction on the same source line."""
    source = """
    START: LOAD R1, 5
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
            opcode=Opcode.HALT,
        ),
    ]


def test_label_only_line():
    """Allow labels to occupy their own source line."""
    source = """
    START:

    HALT
    """

    instructions = Assembler().assemble(source)

    assert instructions == [
        Instruction(
            opcode=Opcode.HALT,
        )
    ]


def test_undefined_label():
    """Reject references to labels that do not exist."""
    source = """
    JUMP MISSING
    """

    with pytest.raises(
        ValueError,
        match="undefined label 'MISSING'",
    ):
        Assembler().assemble(source)


def test_duplicate_label():
    """Reject duplicate label definitions."""
    source = """
    START:
        HALT

    START:
        HALT
    """

    with pytest.raises(
        ValueError,
        match="duplicate label 'START'",
    ):
        Assembler().assemble(source)


def test_invalid_label():
    """Reject labels beginning with invalid characters."""
    source = """
    123START:
        HALT
    """

    with pytest.raises(
        ValueError,
        match="invalid label",
    ):
        Assembler().assemble(source)


def test_label_with_underscore():
    """Allow underscores in labels."""
    source = """
    _LOOP:
        JUMP _LOOP
    """

    instructions = Assembler().assemble(source)

    assert instructions == [
        Instruction(
            opcode=Opcode.JUMP,
            address=0,
        )
    ]


def test_label_with_numbers():
    """Allow numbers after the first label character."""
    source = """
    LOOP1:
        JUMP LOOP1
    """

    instructions = Assembler().assemble(source)

    assert instructions == [
        Instruction(
            opcode=Opcode.JUMP,
            address=0,
        )
    ]


def test_label_and_comment():
    """Allow labels and comments on the same line."""
    source = """
    START:    # program entry
        JUMP START
    """

    instructions = Assembler().assemble(source)

    assert instructions == [
        Instruction(
            opcode=Opcode.JUMP,
            address=0,
        )
    ]


def test_numeric_addresses_still_work():
    """Preserve support for numeric addresses."""
    source = """
    JUMP 10
    """

    instructions = Assembler().assemble(source)

    assert instructions == [
        Instruction(
            opcode=Opcode.JUMP,
            address=10,
        )
    ]