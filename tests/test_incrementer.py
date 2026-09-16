import pytest

from astra.logic.incrementer import Incrementer4Bit


incrementer = Incrementer4Bit()


def test_increment_zero():
    assert incrementer.increment((0, 0, 0, 0)) == (0, 0, 0, 1)


def test_increment_one():
    assert incrementer.increment((0, 0, 0, 1)) == (0, 0, 1, 0)


def test_increment_three():
    assert incrementer.increment((0, 0, 1, 1)) == (0, 1, 0, 0)


def test_increment_seven():
    assert incrementer.increment((0, 1, 1, 1)) == (1, 0, 0, 0)


def test_increment_fourteen():
    assert incrementer.increment((1, 1, 1, 0)) == (1, 1, 1, 1)


def test_increment_wraparound():
    assert incrementer.increment((1, 1, 1, 1)) == (0, 0, 0, 0)


def test_all_4bit_values():
    expected_values = [
        (0, 0, 0, 1),
        (0, 0, 1, 0),
        (0, 0, 1, 1),
        (0, 1, 0, 0),
        (0, 1, 0, 1),
        (0, 1, 1, 0),
        (0, 1, 1, 1),
        (1, 0, 0, 0),
        (1, 0, 0, 1),
        (1, 0, 1, 0),
        (1, 0, 1, 1),
        (1, 1, 0, 0),
        (1, 1, 0, 1),
        (1, 1, 1, 0),
        (1, 1, 1, 1),
        (0, 0, 0, 0),
    ]

    for value in range(16):
        input_bits = (
            (value >> 3) & 1,
            (value >> 2) & 1,
            (value >> 1) & 1,
            value & 1,
        )

        assert incrementer.increment(input_bits) == expected_values[value]


def test_invalid_bit():
    with pytest.raises(ValueError):
        incrementer.increment((0, 0, 0, 2))


def test_negative_bit():
    with pytest.raises(ValueError):
        incrementer.increment((0, 0, 0, -1))


def test_wrong_input_width():
    with pytest.raises(ValueError):
        incrementer.increment((0, 0, 0))


def test_too_many_bits():
    with pytest.raises(ValueError):
        incrementer.increment((0, 0, 0, 0, 0))