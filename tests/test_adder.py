import pytest
from astra.logic.adder import half_adder, full_adder, ripple_carry_adder

def test_half_adder():
    assert half_adder(0, 0) == (0, 0)
    assert half_adder(0, 1) == (1, 0)
    assert half_adder(1, 0) == (1, 0)
    assert half_adder(1, 1) == (0, 1)

def test_half_adder_invalid_input():
    with pytest.raises(ValueError):
        half_adder(2, 0)
    with pytest.raises(ValueError):
        half_adder(1, 2)

def test_full_adder():
    assert full_adder(0, 0, 0) == (0, 0)
    assert full_adder(0, 1, 0) == (1, 0)
    assert full_adder(1, 0, 0) == (1, 0)
    assert full_adder(1, 1, 0) == (0, 1)
    assert full_adder(0, 0, 1) == (1, 0)
    assert full_adder(0, 1, 1) == (0, 1)
    assert full_adder(1, 0, 1) == (0, 1)
    assert full_adder(1, 1, 1) == (1, 1)    

def test_full_adder_invalid_input():
    with pytest.raises(ValueError):
        full_adder(2, 0, 0)
    with pytest.raises(ValueError):
        full_adder(1, 2, 0)
    with pytest.raises(ValueError):
        full_adder(1, 1, 2)

def test_ripple_carry_adder():
    assert ripple_carry_adder(
        (0, 0, 0, 0),
        (0, 0, 0, 0)
    ) == ((0, 0, 0, 0), 0)

    assert ripple_carry_adder(
        (0, 0, 0, 1),
        (0, 0, 0, 1)
    ) == ((0, 0, 1, 0), 0)

    assert ripple_carry_adder(
        (0, 0, 1, 1),
        (0, 0, 1, 1)
    ) == ((0, 1, 1, 0), 0)

    assert ripple_carry_adder(
        (1, 1, 1, 1),
        (0, 0, 0, 1)
    ) == ((0, 0, 0, 0), 1)

def test_ripple_carry_adder_invalid_input():
    with pytest.raises(ValueError):
        ripple_carry_adder(
            (0, 0, 0),
            (0, 0, 0, 0)
        )

    with pytest.raises(ValueError):
        ripple_carry_adder(
            (0, 0, 0, 0, 0),
            (0, 0, 0, 0)
        )

    with pytest.raises(ValueError):
        ripple_carry_adder(
            (0, 0, 0, 2),
            (0, 0, 0, 0)
        )

    with pytest.raises(ValueError):
        ripple_carry_adder(
            (0, 0, 0, 0),
            (0, 0, 0, 2)
        )

def test_ripple_carry_adder_with_carry_in():

    assert ripple_carry_adder(
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        1
    ) == ((0, 0, 0, 1), 0)

    assert ripple_carry_adder(
        (0, 0, 0, 1),
        (0, 0, 0, 0),
        1
    ) == ((0, 0, 1, 0), 0)

    assert ripple_carry_adder(
        (1, 1, 1, 1),
        (0, 0, 0, 0),
        1
    ) == ((0, 0, 0, 0), 1)