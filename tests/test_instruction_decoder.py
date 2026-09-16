import pytest

from astra.isa.decoder import InstructionDecoder
from astra.isa.instructions import Opcode, Register


decoder = InstructionDecoder()


# ============================================================
# R-TYPE INSTRUCTIONS
# ============================================================

def test_add_decoding():
    word = (0, 0, 0, 0, 0, 0, 0, 1)

    result = decoder.decode(word)

    assert result == {
        "opcode": Opcode.ADD,
        "destination": Register.R0,
        "source": Register.R1,
        "address": None
    }


def test_sub_decoding():
    word = (0, 0, 0, 1, 0, 1, 1, 0)

    result = decoder.decode(word)

    assert result == {
        "opcode": Opcode.SUB,
        "destination": Register.R1,
        "source": Register.R2,
        "address": None
    }


def test_and_decoding():
    word = (0, 0, 1, 0, 1, 0, 1, 1)

    result = decoder.decode(word)

    assert result == {
        "opcode": Opcode.AND,
        "destination": Register.R2,
        "source": Register.R3,
        "address": None
    }


def test_or_decoding():
    word = (0, 0, 1, 1, 1, 1, 0, 0)

    result = decoder.decode(word)

    assert result == {
        "opcode": Opcode.OR,
        "destination": Register.R3,
        "source": Register.R0,
        "address": None
    }


def test_xor_decoding():
    word = (0, 1, 0, 0, 0, 0, 1, 1)

    result = decoder.decode(word)

    assert result == {
        "opcode": Opcode.XOR,
        "destination": Register.R0,
        "source": Register.R3,
        "address": None
    }


# ============================================================
# NOT
# ============================================================

def test_not_decoding():
    word = (0, 1, 0, 1, 1, 0, 0, 0)

    result = decoder.decode(word)

    assert result == {
        "opcode": Opcode.NOT,
        "destination": Register.R2,
        "source": None,
        "address": None
    }


# ============================================================
# LOAD
# ============================================================

def test_load_decoding():
    word = (0, 1, 1, 0, 1, 0, 0, 0)

    result = decoder.decode(word)

    assert result == {
        "opcode": Opcode.LOAD,
        "destination": Register.R2,
        "source": None,
        "address": None
    }


# ============================================================
# STORE
# ============================================================

def test_store_decoding():
    word = (0, 1, 1, 1, 1, 0, 0, 0)

    result = decoder.decode(word)

    assert result == {
        "opcode": Opcode.STORE,
        "destination": None,
        "source": Register.R2,
        "address": None
    }


# ============================================================
# JUMP
# ============================================================

def test_jump_decoding():
    word = (1, 0, 0, 0, 1, 1, 0, 0)

    result = decoder.decode(word)

    assert result == {
        "opcode": Opcode.JUMP,
        "destination": None,
        "source": None,
        "address": 12
    }


def test_jump_address_zero():
    word = (1, 0, 0, 0, 0, 0, 0, 0)

    result = decoder.decode(word)

    assert result["opcode"] == Opcode.JUMP
    assert result["address"] == 0


def test_jump_address_max():
    word = (1, 0, 0, 0, 1, 1, 1, 1)

    result = decoder.decode(word)

    assert result["opcode"] == Opcode.JUMP
    assert result["address"] == 15


# ============================================================
# HALT
# ============================================================

def test_halt_decoding():
    word = (1, 0, 0, 1, 0, 0, 0, 0)

    result = decoder.decode(word)

    assert result == {
        "opcode": Opcode.HALT,
        "destination": None,
        "source": None,
        "address": None
    }


# ============================================================
# INPUT VALIDATION
# ============================================================

def test_word_must_be_tuple():
    with pytest.raises(TypeError):
        decoder.decode([0, 0, 0, 0, 0, 0, 0, 0])


def test_word_must_have_8_bits():
    with pytest.raises(ValueError):
        decoder.decode((0, 0, 0, 0))


def test_word_cannot_have_more_than_8_bits():
    with pytest.raises(ValueError):
        decoder.decode((0, 0, 0, 0, 0, 0, 0, 0, 0))


def test_word_can_only_contain_zero_or_one():
    with pytest.raises(ValueError):
        decoder.decode((0, 0, 0, 0, 2, 0, 0, 0))


def test_word_cannot_contain_negative_bit():
    with pytest.raises(ValueError):
        decoder.decode((0, 0, 0, 0, -1, 0, 0, 0))


# ============================================================
# INVALID OPCODES
# ============================================================

def test_reserved_opcode_10_is_rejected():
    word = (1, 0, 1, 0, 0, 0, 0, 0)

    with pytest.raises(ValueError):
        decoder.decode(word)


def test_reserved_opcode_15_is_rejected():
    word = (1, 1, 1, 1, 0, 0, 0, 0)

    with pytest.raises(ValueError):
        decoder.decode(word)


# ============================================================
# ENCODER → DECODER ROUND TRIP
# ============================================================

def test_add_encode_decode_round_trip():
    from astra.isa.instructions import Instruction

    instruction = Instruction(
        Opcode.ADD,
        Register.R1,
        Register.R2
    )

    encoded_word = instruction.encode()[0]
    decoded = decoder.decode(encoded_word)

    assert decoded["opcode"] == instruction.opcode
    assert decoded["destination"] == instruction.destination
    assert decoded["source"] == instruction.source


def test_not_encode_decode_round_trip():
    from astra.isa.instructions import Instruction

    instruction = Instruction(
        Opcode.NOT,
        Register.R3
    )

    encoded_word = instruction.encode()[0]
    decoded = decoder.decode(encoded_word)

    assert decoded["opcode"] == instruction.opcode
    assert decoded["destination"] == instruction.destination
    assert decoded["source"] is None


def test_jump_encode_decode_round_trip():
    from astra.isa.instructions import Instruction

    instruction = Instruction(
        Opcode.JUMP,
        address=13
    )

    encoded_word = instruction.encode()[0]
    decoded = decoder.decode(encoded_word)

    assert decoded["opcode"] == instruction.opcode
    assert decoded["address"] == instruction.address


# ============================================================
# LOAD / STORE ADDRESS WORD
# ============================================================

def test_decode_load_address():
    word = (0, 0, 0, 0, 1, 0, 1, 0)

    address = decoder.decode_address(word)

    assert address == 10


def test_decode_address_zero():
    word = (0, 0, 0, 0, 0, 0, 0, 0)

    address = decoder.decode_address(word)

    assert address == 0


def test_decode_address_max():
    word = (0, 0, 0, 0, 1, 1, 1, 1)

    address = decoder.decode_address(word)

    assert address == 15


def test_decode_address_invalid_type():
    with pytest.raises(TypeError):
        decoder.decode_address(
            [0, 0, 0, 0, 1, 0, 1, 0]
        )


def test_decode_address_invalid_width():
    with pytest.raises(ValueError):
        decoder.decode_address(
            (0, 0, 0, 0)
        )


def test_decode_address_invalid_bit():
    with pytest.raises(ValueError):
        decoder.decode_address(
            (0, 0, 0, 0, 2, 0, 1, 0)
        )