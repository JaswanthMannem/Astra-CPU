import pytest

from astra.logic.mux import mux, mux4, mux8

def test_mux():
    assert mux(0, 0, 0) == 0
    assert mux(0, 1, 0) == 0
    assert mux(1, 0, 0) == 1
    assert mux(1, 1, 0) == 1
    assert mux(0, 0, 1) == 0
    assert mux(0, 1, 1) == 1
    assert mux(1, 0, 1) == 0
    assert mux(1, 1, 1) == 1

def test_mux_invalid_input():
    with pytest.raises(ValueError):
        mux(2, 1, 0)
    with pytest.raises(ValueError):
        mux(1, 2, 0)
    with pytest.raises(ValueError):
        mux(1, 1, 2)

def test_mux4():
    assert mux4(0, 1, 1, 0, 0, 0) == 0
    assert mux4(0, 1, 1, 0, 0, 1) == 1
    assert mux4(0, 1, 1, 0, 1, 0) == 1
    assert mux4(0, 1, 1, 0, 1, 1) == 0

def test_mux4_invalid_input():
    with pytest.raises(ValueError):
        mux4(2, 0, 0, 0, 0, 0)

    with pytest.raises(ValueError):
        mux4(0, 2, 0, 0, 0, 0)

    with pytest.raises(ValueError):
        mux4(0, 0, 2, 0, 0, 0)

    with pytest.raises(ValueError):
        mux4(0, 0, 0, 2, 0, 0)

    with pytest.raises(ValueError):
        mux4(0, 0, 0, 0, 2, 0)

    with pytest.raises(ValueError):
        mux4(0, 0, 0, 0, 0, 2)

def test_mux8():
    assert mux8(0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0) == 0
    assert mux8(0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1) == 1
    assert mux8(0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0) == 1
    assert mux8(0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1) == 0
    assert mux8(0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0) == 0
    assert mux8(0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1) == 1
    assert mux8(0, 1, 1, 0, 0, 1, 1, 0, 1, 1 ,0) == 1

def test_mux8_invalid_input():
    with pytest.raises(ValueError):
        mux8(2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    with pytest.raises(ValueError):
        mux8(0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    with pytest.raises(ValueError):
        mux8(0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0)

    with pytest.raises(ValueError):
        mux8(0, 0, 0, 2, 0, 0, 0, 0, 0, 0 ,0)

    with pytest.raises(ValueError):
        mux8(0, 0 ,0 ,2 ,2 ,2 ,2 ,2 ,2 ,2 ,2)