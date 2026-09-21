import pytest

from astra.logic.data_memory import DataMemory16x4


def write_memory(
    memory,
    address,
    data,
):
    memory.update(
        address=address,
        data=data,
        write_enable=1,
        clock=0,
    )

    memory.update(
        address=address,
        data=data,
        write_enable=1,
        clock=1,
    )


def test_initial_memory_is_zero():
    memory = DataMemory16x4()

    for address in (
        (0, 0, 0, 0),
        (0, 0, 0, 1),
        (0, 1, 0, 0),
        (1, 0, 1, 0),
        (1, 1, 1, 1),
    ):
        result = memory.update(
            address=address,
            data=(1, 1, 1, 1),
            write_enable=0,
            clock=0,
        )

        assert result == (0, 0, 0, 0)


def test_write_and_read_address_zero():
    memory = DataMemory16x4()

    write_memory(
        memory,
        (0, 0, 0, 0),
        (1, 0, 1, 0),
    )

    result = memory.update(
        address=(0, 0, 0, 0),
        data=(0, 0, 0, 0),
        write_enable=0,
        clock=0,
    )

    assert result == (1, 0, 1, 0)


def test_write_and_read_high_address():
    memory = DataMemory16x4()

    write_memory(
        memory,
        (1, 1, 1, 1),
        (0, 1, 1, 0),
    )

    result = memory.update(
        address=(1, 1, 1, 1),
        data=(0, 0, 0, 0),
        write_enable=0,
        clock=0,
    )

    assert result == (0, 1, 1, 0)


def test_multiple_addresses():
    memory = DataMemory16x4()

    write_memory(
        memory,
        (0, 0, 0, 1),
        (0, 0, 1, 1),
    )

    write_memory(
        memory,
        (1, 0, 1, 0),
        (1, 0, 1, 0),
    )

    result_a = memory.update(
        address=(0, 0, 0, 1),
        data=(0, 0, 0, 0),
        write_enable=0,
        clock=0,
    )

    result_b = memory.update(
        address=(1, 0, 1, 0),
        data=(0, 0, 0, 0),
        write_enable=0,
        clock=0,
    )

    assert result_a == (0, 0, 1, 1)
    assert result_b == (1, 0, 1, 0)


def test_write_does_not_modify_other_addresses():
    memory = DataMemory16x4()

    write_memory(
        memory,
        (0, 0, 1, 1),
        (1, 1, 0, 0),
    )

    result = memory.update(
        address=(0, 0, 1, 0),
        data=(0, 0, 0, 0),
        write_enable=0,
        clock=0,
    )

    assert result == (0, 0, 0, 0)


def test_write_enable_zero_does_not_write():
    memory = DataMemory16x4()

    memory.update(
        address=(0, 1, 0, 1),
        data=(1, 1, 1, 1),
        write_enable=0,
        clock=1,
    )

    result = memory.update(
        address=(0, 1, 0, 1),
        data=(0, 0, 0, 0),
        write_enable=0,
        clock=0,
    )

    assert result == (0, 0, 0, 0)


def test_write_requires_clock():
    memory = DataMemory16x4()

    memory.update(
        address=(0, 0, 1, 0),
        data=(1, 1, 1, 1),
        write_enable=1,
        clock=0,
    )

    result = memory.update(
        address=(0, 0, 1, 0),
        data=(0, 0, 0, 0),
        write_enable=0,
        clock=0,
    )

    assert result == (0, 0, 0, 0)


def test_invalid_address_length():
    memory = DataMemory16x4()

    with pytest.raises(ValueError):
        memory.update(
            address=(0, 0, 0),
            data=(0, 0, 0, 0),
            write_enable=0,
            clock=0,
        )


def test_invalid_data_length():
    memory = DataMemory16x4()

    with pytest.raises(ValueError):
        memory.update(
            address=(0, 0, 0, 0),
            data=(0, 0, 0),
            write_enable=0,
            clock=0,
        )


def test_invalid_address_bit():
    memory = DataMemory16x4()

    with pytest.raises(ValueError):
        memory.update(
            address=(0, 0, 0, 2),
            data=(0, 0, 0, 0),
            write_enable=0,
            clock=0,
        )


def test_invalid_data_bit():
    memory = DataMemory16x4()

    with pytest.raises(ValueError):
        memory.update(
            address=(0, 0, 0, 0),
            data=(0, 0, 0, 2),
            write_enable=0,
            clock=0,
        )


def test_invalid_write_enable():
    memory = DataMemory16x4()

    with pytest.raises(ValueError):
        memory.update(
            address=(0, 0, 0, 0),
            data=(0, 0, 0, 0),
            write_enable=2,
            clock=0,
        )