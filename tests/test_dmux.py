import pytest
from astra.logic.dmux import dmux, dmux4, dmux8

def test_dmux():
    assert dmux(0, 0) == (0, 0)
    assert dmux(0, 1) == (0, 0)
    assert dmux(1, 0) == (1, 0)
    assert dmux(1, 1) == (0, 1)

def test_dmux_invalid_input():
    with pytest.raises(ValueError):
        dmux(2, 0)
    with pytest.raises(ValueError):
        dmux(1, 2)

def test_dmux4():
    assert dmux4(0, (0, 0)) == (0, 0, 0, 0)
    assert dmux4(1, (0, 0)) == (1, 0, 0, 0)
    assert dmux4(1, (0, 1)) == (0, 1, 0, 0)
    assert dmux4(1, (1, 0)) == (0, 0, 1, 0)
    assert dmux4(1, (1, 1)) == (0, 0, 0, 1)

def test_dmux4_invalid_input():
    with pytest.raises(ValueError):
        dmux4(2, (0, 0))
    with pytest.raises(ValueError):
        dmux4(1, (2, 0))
    with pytest.raises(ValueError):
        dmux4(1, (0, 2))

def test_dmux8():
    assert dmux8(0, (0, 0, 0)) == (0, 0, 0, 0, 0, 0, 0, 0)
    assert dmux8(1, (0, 0, 0)) == (1, 0, 0, 0, 0, 0, 0, 0)
    assert dmux8(1, (0, 0, 1)) == (0, 1, 0, 0, 0, 0, 0, 0)
    assert dmux8(1, (0, 1, 0)) == (0, 0, 1, 0, 0, 0, 0, 0)
    assert dmux8(1, (1, 1, 1)) == (0, 0, 0, 0, 0, 0, 0, 1)

def test_dmux8_invalid_input():
    with pytest.raises(ValueError):
        dmux8(2, (0, 0, 0))
    with pytest.raises(ValueError):
        dmux8(1, (2, 0, 0))
    with pytest.raises(ValueError):
        dmux8(1, (0, 2, 0))
    with pytest.raises(ValueError):
        dmux8(1, (0, 0, 2))