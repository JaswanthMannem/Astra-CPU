import pytest
from astra.logic.gates import (
    and_gate,
    or_gate, 
    not_gate,
    nand_gate,
    nor_gate,
    xor_gate,
    xnor_gate
)



def test_and_gate():
    assert and_gate(0, 0) == 0
    assert and_gate(0, 1) == 0
    assert and_gate(1, 0) == 0
    assert and_gate(1, 1) == 1

def test_and_gate_invalid_input():
    with pytest.raises(ValueError):
        and_gate(2, 1)

def test_or_gate():
    assert or_gate(0, 0) == 0
    assert or_gate(0, 1) == 1
    assert or_gate(1, 0) == 1
    assert or_gate(1, 1) == 1

def test_or_gate_invalid_input():
    with pytest.raises(ValueError):
        or_gate(2, 1)

def test_not_gate():
    assert not_gate(0) == 1
    assert not_gate(1) == 0

def test_not_gate_invalid_input():
    with pytest.raises(ValueError):
        not_gate(2)

def test_nand_gate():
    assert nand_gate(0, 0) == 1
    assert nand_gate(0, 1) == 1
    assert nand_gate(1, 0) == 1
    assert nand_gate(1, 1) == 0


def test_nand_gate_invalid_input():
    with pytest.raises(ValueError):
        nand_gate(2, 1)


def test_nor_gate():
    assert nor_gate(0, 0) == 1
    assert nor_gate(0, 1) == 0
    assert nor_gate(1, 0) == 0
    assert nor_gate(1, 1) == 0


def test_nor_gate_invalid_input():
    with pytest.raises(ValueError):
        nor_gate(2, 1)

def test_xor_gate():
    assert xor_gate(0, 0) == 0
    assert xor_gate(0, 1) == 1
    assert xor_gate(1, 0) == 1
    assert xor_gate(1, 1) == 0


def test_xor_gate_invalid_input():
    with pytest.raises(ValueError):
        xor_gate(2, 1)

def test_xnor_gate():
    assert xnor_gate(0, 0) == 1
    assert xnor_gate(0, 1) == 0
    assert xnor_gate(1, 0) == 0
    assert xnor_gate(1, 1) == 1

def test_xnor_gate_invalid_input():
    with pytest.raises(ValueError):
        xnor_gate(2, 1)
