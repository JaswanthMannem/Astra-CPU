import pytest

from astra.cpu.alu_control import ALUOperation
from astra.cpu.control_unit import ControlSignals, ControlUnit
from astra.isa.instructions import Instruction, Opcode, Register


def test_add_control_signals():
    control_unit = ControlUnit()

    instruction = Instruction(
        Opcode.ADD,
        destination=Register.R1,
        source=Register.R2,
    )

    signals = control_unit.decode(instruction)

    assert signals == ControlSignals(
        alu_operation=ALUOperation.ADD,
        register_write=1,
        memory_read=0,
        memory_write=0,
        pc_load=0,
        pc_increment=1,
        halt=0,
    )


def test_sub_control_signals():
    control_unit = ControlUnit()

    instruction = Instruction(
        Opcode.SUB,
        destination=Register.R1,
        source=Register.R2,
    )

    signals = control_unit.decode(instruction)

    assert signals == ControlSignals(
        alu_operation=ALUOperation.SUB,
        register_write=1,
        memory_read=0,
        memory_write=0,
        pc_load=0,
        pc_increment=1,
        halt=0,
    )


def test_and_control_signals():
    control_unit = ControlUnit()

    instruction = Instruction(
        Opcode.AND,
        destination=Register.R1,
        source=Register.R2,
    )

    signals = control_unit.decode(instruction)

    assert signals == ControlSignals(
        alu_operation=ALUOperation.AND,
        register_write=1,
        memory_read=0,
        memory_write=0,
        pc_load=0,
        pc_increment=1,
        halt=0,
    )


def test_or_control_signals():
    control_unit = ControlUnit()

    instruction = Instruction(
        Opcode.OR,
        destination=Register.R1,
        source=Register.R2,
    )

    signals = control_unit.decode(instruction)

    assert signals == ControlSignals(
        alu_operation=ALUOperation.OR,
        register_write=1,
        memory_read=0,
        memory_write=0,
        pc_load=0,
        pc_increment=1,
        halt=0,
    )


def test_xor_control_signals():
    control_unit = ControlUnit()

    instruction = Instruction(
        Opcode.XOR,
        destination=Register.R1,
        source=Register.R2,
    )

    signals = control_unit.decode(instruction)

    assert signals == ControlSignals(
        alu_operation=ALUOperation.XOR,
        register_write=1,
        memory_read=0,
        memory_write=0,
        pc_load=0,
        pc_increment=1,
        halt=0,
    )


def test_not_control_signals():
    control_unit = ControlUnit()

    instruction = Instruction(
        Opcode.NOT,
        destination=Register.R1,
    )

    signals = control_unit.decode(instruction)

    assert signals == ControlSignals(
        alu_operation=ALUOperation.NOT,
        register_write=1,
        memory_read=0,
        memory_write=0,
        pc_load=0,
        pc_increment=1,
        halt=0,
    )


def test_load_control_signals():
    control_unit = ControlUnit()

    instruction = Instruction(
        Opcode.LOAD,
        destination=Register.R1,
        address=10,
    )

    signals = control_unit.decode(instruction)

    assert signals == ControlSignals(
        alu_operation=None,
        register_write=1,
        memory_read=1,
        memory_write=0,
        pc_load=0,
        pc_increment=1,
        halt=0,
    )


def test_store_control_signals():
    control_unit = ControlUnit()

    instruction = Instruction(
        Opcode.STORE,
        source=Register.R1,
        address=10,
    )

    signals = control_unit.decode(instruction)

    assert signals == ControlSignals(
        alu_operation=None,
        register_write=0,
        memory_read=0,
        memory_write=1,
        pc_load=0,
        pc_increment=1,
        halt=0,
    )


def test_jump_control_signals():
    control_unit = ControlUnit()

    instruction = Instruction(
        Opcode.JUMP,
        address=10,
    )

    signals = control_unit.decode(instruction)

    assert signals == ControlSignals(
        alu_operation=None,
        register_write=0,
        memory_read=0,
        memory_write=0,
        pc_load=1,
        pc_increment=0,
        halt=0,
    )


def test_halt_control_signals():
    control_unit = ControlUnit()

    instruction = Instruction(Opcode.HALT)

    signals = control_unit.decode(instruction)

    assert signals == ControlSignals(
        alu_operation=None,
        register_write=0,
        memory_read=0,
        memory_write=0,
        pc_load=0,
        pc_increment=0,
        halt=1,
    )


def test_invalid_instruction_type():
    control_unit = ControlUnit()

    with pytest.raises(TypeError):
        control_unit.decode("ADD")


def test_control_signals_are_immutable():
    control_unit = ControlUnit()

    instruction = Instruction(
        Opcode.ADD,
        destination=Register.R1,
        source=Register.R2,
    )

    signals = control_unit.decode(instruction)

    with pytest.raises(AttributeError):
        signals.register_write = 0