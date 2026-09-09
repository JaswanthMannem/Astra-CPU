from astra.logic.bitwise import (
    not_4bit,
    and_4bit,
    or_4bit,
    xor_4bit,
    zero_flag,
    negative_flag,
    overflow_flag
)


def test_not_4bit():
    assert not_4bit((0, 0, 0, 0)) == (1, 1, 1, 1)
    assert not_4bit((1, 1, 1, 1)) == (0, 0, 0, 0)
    assert not_4bit((1, 0, 1, 0)) == (0, 1, 0, 1)


def test_and_4bit():
    assert and_4bit((0, 0, 0, 0), (0, 0, 0, 0)) == (0, 0, 0, 0)
    assert and_4bit((1, 1, 1, 1), (1, 1, 1, 1)) == (1, 1, 1, 1)
    assert and_4bit((1, 0, 1, 0), (1, 1, 0, 0)) == (1, 0, 0, 0)


def test_or_4bit():
    assert or_4bit((0, 0, 0, 0), (0, 0, 0, 0)) == (0, 0, 0, 0)
    assert or_4bit((1, 1, 1, 1), (0, 0, 0, 0)) == (1, 1, 1, 1)
    assert or_4bit((1, 0, 1, 0), (0, 1, 0, 0)) == (1, 1, 1, 0)


def test_xor_4bit():
    assert xor_4bit((0, 0, 0, 0), (0, 0, 0, 0)) == (0, 0, 0, 0)
    assert xor_4bit((1, 1, 1, 1), (1, 1, 1, 1)) == (0, 0, 0, 0)
    assert xor_4bit((1, 0, 1, 0), (0, 1, 0, 0)) == (1, 1, 1, 0)

def test_zero_flag():

    assert zero_flag((0, 0, 0, 0)) == 1

    assert zero_flag((0, 0, 0, 1)) == 0
    assert zero_flag((0, 0, 1, 0)) == 0
    assert zero_flag((0, 1, 0, 0)) == 0
    assert zero_flag((1, 0, 0, 0)) == 0

    assert zero_flag((1, 1, 1, 1)) == 0

def test_negative_flag():

    assert negative_flag((0, 0, 0, 0)) == 0
    assert negative_flag((0, 1, 0, 1)) == 0
    assert negative_flag((0, 0, 1, 1)) == 0

    assert negative_flag((1, 0, 0, 0)) == 1
    assert negative_flag((1, 0, 1, 0)) == 1
    assert negative_flag((1, 1, 1, 1)) == 1

def test_overflow_flag():

    # 7 + 1 = -8 -> overflow
    assert overflow_flag(
        (0, 1, 1, 1),
        (0, 0, 0, 1),
        (1, 0, 0, 0),
        0
    ) == 1

    # -8 + -1 = 7 -> overflow
    assert overflow_flag(
        (1, 0, 0, 0),
        (1, 1, 1, 1),
        (0, 1, 1, 1),
        0
    ) == 1

    # 3 + 2 = 5 -> no overflow
    assert overflow_flag(
        (0, 0, 1, 1),
        (0, 0, 1, 0),
        (0, 1, 0, 1),
        0
    ) == 0

    # -3 + -2 = -5 -> no overflow
    assert overflow_flag(
        (1, 1, 0, 1),
        (1, 1, 1, 0),
        (1, 0, 1, 1),
        0
    ) == 0

    # 7 - (-1) = 8 -> overflow
    assert overflow_flag(
        (0, 1, 1, 1),
        (1, 1, 1, 1),
        (1, 0, 0, 0),
        1
    ) == 1

    # -8 - 1 = -9 -> overflow
    assert overflow_flag(
        (1, 0, 0, 0),
        (0, 0, 0, 1),
        (0, 1, 1, 1),
        1
    ) == 1

    # 5 - 2 = 3 -> no overflow
    assert overflow_flag(
        (0, 1, 0, 1),
        (0, 0, 1, 0),
        (0, 0, 1, 1),
        1
    ) == 0