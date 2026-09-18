import pytest

from astra.cpu.alu_control import ALUControl, ALUOperation
from astra.isa.instructions import Opcode


def test_add():
    control = ALUControl()

    assert control.operation(Opcode.ADD) == ALUOperation.ADD


def test_sub():
    control = ALUControl()

    assert control.operation(Opcode.SUB) == ALUOperation.SUB


def test_and():
    control = ALUControl()

    assert control.operation(Opcode.AND) == ALUOperation.AND


def test_or():
    control = ALUControl()

    assert control.operation(Opcode.OR) == ALUOperation.OR


def test_xor():
    control = ALUControl()

    assert control.operation(Opcode.XOR) == ALUOperation.XOR


def test_not():
    control = ALUControl()

    assert control.operation(Opcode.NOT) == ALUOperation.NOT


def test_load_rejected():
    control = ALUControl()

    with pytest.raises(ValueError):
        control.operation(Opcode.LOAD)


def test_store_rejected():
    control = ALUControl()

    with pytest.raises(ValueError):
        control.operation(Opcode.STORE)


def test_jump_rejected():
    control = ALUControl()

    with pytest.raises(ValueError):
        control.operation(Opcode.JUMP)


def test_halt_rejected():
    control = ALUControl()

    with pytest.raises(ValueError):
        control.operation(Opcode.HALT)


def test_invalid_opcode_type():
    control = ALUControl()

    with pytest.raises(TypeError):
        control.operation(5)