import pytest

from astra.isa.instructions import Instruction, Opcode, Register


# ============================================================
# R-TYPE INSTRUCTIONS
# ============================================================

def test_add_encoding():
    instruction = Instruction(
        Opcode.ADD,
        Register.R0,
        Register.R1
    )

    assert instruction.encode() == (
        (0, 0, 0, 0, 0, 0, 0, 1),
    )


def test_sub_encoding():
    instruction = Instruction(
        Opcode.SUB,
        Register.R1,
        Register.R2
    )

    assert instruction.encode() == (
        (0, 0, 0, 1, 0, 1, 1, 0),
    )


def test_and_encoding():
    instruction = Instruction(
        Opcode.AND,
        Register.R2,
        Register.R3
    )

    assert instruction.encode() == (
        (0, 0, 1, 0, 1, 0, 1, 1),
    )


def test_or_encoding():
    instruction = Instruction(
        Opcode.OR,
        Register.R3,
        Register.R0
    )

    assert instruction.encode() == (
        (0, 0, 1, 1, 1, 1, 0, 0),
    )


def test_xor_encoding():
    instruction = Instruction(
        Opcode.XOR,
        Register.R0,
        Register.R3
    )

    assert instruction.encode() == (
        (0, 1, 0, 0, 0, 0, 1, 1),
    )


# ============================================================
# NOT
# ============================================================

def test_not_encoding():
    instruction = Instruction(
        Opcode.NOT,
        Register.R2
    )

    assert instruction.encode() == (
        (0, 1, 0, 1, 1, 0, 0, 0),
    )


# ============================================================
# LOAD
# ============================================================

def test_load_encoding():
    instruction = Instruction(
        Opcode.LOAD,
        Register.R2,
        address=10
    )

    assert instruction.encode() == (
        (0, 1, 1, 0, 1, 0, 0, 0),
        (0, 0, 0, 0, 1, 0, 1, 0)
    )


def test_load_address_zero():
    instruction = Instruction(
        Opcode.LOAD,
        Register.R0,
        address=0
    )

    assert instruction.encode() == (
        (0, 1, 1, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0)
    )


def test_load_address_max():
    instruction = Instruction(
        Opcode.LOAD,
        Register.R3,
        address=15
    )

    assert instruction.encode() == (
        (0, 1, 1, 0, 1, 1, 0, 0),
        (0, 0, 0, 0, 1, 1, 1, 1)
    )


# ============================================================
# STORE
# ============================================================

def test_store_encoding():
    instruction = Instruction(
        Opcode.STORE,
        source=Register.R2,
        address=10
    )

    assert instruction.encode() == (
        (0, 1, 1, 1, 1, 0, 0, 0),
        (0, 0, 0, 0, 1, 0, 1, 0)
    )


def test_store_address_zero():
    instruction = Instruction(
        Opcode.STORE,
        source=Register.R0,
        address=0
    )

    assert instruction.encode() == (
        (0, 1, 1, 1, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0)
    )


def test_store_address_max():
    instruction = Instruction(
        Opcode.STORE,
        source=Register.R3,
        address=15
    )

    assert instruction.encode() == (
        (0, 1, 1, 1, 1, 1, 0, 0),
        (0, 0, 0, 0, 1, 1, 1, 1)
    )


# ============================================================
# JUMP
# ============================================================

def test_jump_encoding():
    instruction = Instruction(
        Opcode.JUMP,
        address=12
    )

    assert instruction.encode() == (
        (1, 0, 0, 0, 1, 1, 0, 0),
    )


def test_jump_address_zero():
    instruction = Instruction(
        Opcode.JUMP,
        address=0
    )

    assert instruction.encode() == (
        (1, 0, 0, 0, 0, 0, 0, 0),
    )


def test_jump_address_max():
    instruction = Instruction(
        Opcode.JUMP,
        address=15
    )

    assert instruction.encode() == (
        (1, 0, 0, 0, 1, 1, 1, 1),
    )


# ============================================================
# HALT
# ============================================================

def test_halt_encoding():
    instruction = Instruction(Opcode.HALT)

    assert instruction.encode() == (
        (1, 0, 0, 1, 0, 0, 0, 0),
    )


# ============================================================
# BASIC VALIDATION
# ============================================================

def test_invalid_opcode_type():
    with pytest.raises(TypeError):
        Instruction("ADD", Register.R0, Register.R1)


def test_invalid_destination_type():
    with pytest.raises(TypeError):
        Instruction(Opcode.ADD, 0, Register.R1)


def test_invalid_source_type():
    with pytest.raises(TypeError):
        Instruction(Opcode.ADD, Register.R0, 1)


def test_invalid_address_type():
    with pytest.raises(TypeError):
        Instruction(
            Opcode.LOAD,
            Register.R0,
            address="10"
        )


def test_address_below_range():
    with pytest.raises(ValueError):
        Instruction(
            Opcode.LOAD,
            Register.R0,
            address=-1
        )


def test_address_above_range():
    with pytest.raises(ValueError):
        Instruction(
            Opcode.LOAD,
            Register.R0,
            address=16
        )


# ============================================================
# R-TYPE VALIDATION
# ============================================================

def test_r_type_requires_destination():
    with pytest.raises(ValueError):
        Instruction(
            Opcode.ADD,
            source=Register.R1
        )


def test_r_type_requires_source():
    with pytest.raises(ValueError):
        Instruction(
            Opcode.ADD,
            destination=Register.R0
        )


def test_r_type_rejects_address():
    with pytest.raises(ValueError):
        Instruction(
            Opcode.ADD,
            Register.R0,
            Register.R1,
            address=5
        )


# ============================================================
# NOT VALIDATION
# ============================================================

def test_not_requires_destination():
    with pytest.raises(ValueError):
        Instruction(Opcode.NOT)


def test_not_rejects_source():
    with pytest.raises(ValueError):
        Instruction(
            Opcode.NOT,
            Register.R0,
            Register.R1
        )


def test_not_rejects_address():
    with pytest.raises(ValueError):
        Instruction(
            Opcode.NOT,
            Register.R0,
            address=5
        )


# ============================================================
# LOAD VALIDATION
# ============================================================

def test_load_requires_destination():
    with pytest.raises(ValueError):
        Instruction(
            Opcode.LOAD,
            address=5
        )


def test_load_requires_address():
    with pytest.raises(ValueError):
        Instruction(
            Opcode.LOAD,
            Register.R0
        )


def test_load_rejects_source():
    with pytest.raises(ValueError):
        Instruction(
            Opcode.LOAD,
            Register.R0,
            Register.R1,
            address=5
        )


# ============================================================
# STORE VALIDATION
# ============================================================

def test_store_requires_source():
    with pytest.raises(ValueError):
        Instruction(
            Opcode.STORE,
            address=5
        )


def test_store_requires_address():
    with pytest.raises(ValueError):
        Instruction(
            Opcode.STORE,
            source=Register.R0
        )


def test_store_rejects_destination():
    with pytest.raises(ValueError):
        Instruction(
            Opcode.STORE,
            destination=Register.R0,
            source=Register.R1,
            address=5
        )


# ============================================================
# JUMP VALIDATION
# ============================================================

def test_jump_requires_address():
    with pytest.raises(ValueError):
        Instruction(Opcode.JUMP)


def test_jump_rejects_destination():
    with pytest.raises(ValueError):
        Instruction(
            Opcode.JUMP,
            destination=Register.R0,
            address=5
        )


def test_jump_rejects_source():
    with pytest.raises(ValueError):
        Instruction(
            Opcode.JUMP,
            source=Register.R0,
            address=5
        )


# ============================================================
# HALT VALIDATION
# ============================================================

def test_halt_rejects_destination():
    with pytest.raises(ValueError):
        Instruction(
            Opcode.HALT,
            destination=Register.R0
        )


def test_halt_rejects_source():
    with pytest.raises(ValueError):
        Instruction(
            Opcode.HALT,
            source=Register.R0
        )


def test_halt_rejects_address():
    with pytest.raises(ValueError):
        Instruction(
            Opcode.HALT,
            address=5
        )


# ============================================================
# ENCODING WIDTH TESTS
# ============================================================

def test_all_encoded_words_are_8_bits():
    instructions = [
        Instruction(Opcode.ADD, Register.R0, Register.R1),
        Instruction(Opcode.SUB, Register.R1, Register.R2),
        Instruction(Opcode.AND, Register.R2, Register.R3),
        Instruction(Opcode.OR, Register.R3, Register.R0),
        Instruction(Opcode.XOR, Register.R0, Register.R3),
        Instruction(Opcode.NOT, Register.R1),
        Instruction(Opcode.LOAD, Register.R2, address=10),
        Instruction(Opcode.STORE, source=Register.R2, address=10),
        Instruction(Opcode.JUMP, address=12),
        Instruction(Opcode.HALT)
    ]

    for instruction in instructions:
        words = instruction.encode()

        for word in words:
            assert len(word) == 8
            assert all(bit in (0, 1) for bit in word)


def test_load_and_store_have_two_words():
    load = Instruction(
        Opcode.LOAD,
        Register.R0,
        address=5
    )

    store = Instruction(
        Opcode.STORE,
        source=Register.R0,
        address=5
    )

    assert len(load.encode()) == 2
    assert len(store.encode()) == 2


def test_other_instructions_have_one_word():
    instructions = [
        Instruction(Opcode.ADD, Register.R0, Register.R1),
        Instruction(Opcode.SUB, Register.R0, Register.R1),
        Instruction(Opcode.AND, Register.R0, Register.R1),
        Instruction(Opcode.OR, Register.R0, Register.R1),
        Instruction(Opcode.XOR, Register.R0, Register.R1),
        Instruction(Opcode.NOT, Register.R0),
        Instruction(Opcode.JUMP, address=5),
        Instruction(Opcode.HALT)
    ]

    for instruction in instructions:
        assert len(instruction.encode()) == 1