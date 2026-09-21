import pytest

from astra.cpu.memory_interface import MemoryInterface


def test_memory_interface_initializes():
    memory = MemoryInterface()

    assert memory.ram is not None


def test_memory_read_disabled_returns_zero():
    memory = MemoryInterface()

    result = memory.access(
        address=(0, 0),
        write_data=(1, 0, 1, 0),
        memory_read=0,
        memory_write=0,
        clock=0,
    )

    assert result == (0, 0, 0, 0)


def test_write_and_read_memory():
    memory = MemoryInterface()

    address = (0, 0)
    data = (1, 0, 1, 0)

    memory.access(
        address=address,
        write_data=data,
        memory_read=0,
        memory_write=1,
        clock=0,
    )

    memory.access(
        address=address,
        write_data=data,
        memory_read=0,
        memory_write=1,
        clock=1,
    )

    result = memory.access(
        address=address,
        write_data=(0, 0, 0, 0),
        memory_read=1,
        memory_write=0,
        clock=0,
    )

    assert result == data


def test_write_does_not_affect_other_addresses():
    memory = MemoryInterface()

    data = (1, 1, 0, 1)

    memory.access(
        address=(0, 0),
        write_data=data,
        memory_read=0,
        memory_write=1,
        clock=0,
    )

    memory.access(
        address=(0, 0),
        write_data=data,
        memory_read=0,
        memory_write=1,
        clock=1,
    )

    result = memory.access(
        address=(0, 1),
        write_data=(0, 0, 0, 0),
        memory_read=1,
        memory_write=0,
        clock=0,
    )

    assert result == (0, 0, 0, 0)


def test_multiple_memory_locations():
    memory = MemoryInterface()

    data0 = (1, 0, 0, 1)
    data1 = (0, 1, 1, 0)

    memory.access(
        address=(0, 0),
        write_data=data0,
        memory_read=0,
        memory_write=1,
        clock=0,
    )

    memory.access(
        address=(0, 0),
        write_data=data0,
        memory_read=0,
        memory_write=1,
        clock=1,
    )

    memory.access(
        address=(0, 1),
        write_data=data1,
        memory_read=0,
        memory_write=1,
        clock=0,
    )

    memory.access(
        address=(0, 1),
        write_data=data1,
        memory_read=0,
        memory_write=1,
        clock=1,
    )

    result0 = memory.access(
        address=(0, 0),
        write_data=(0, 0, 0, 0),
        memory_read=1,
        memory_write=0,
        clock=0,
    )

    result1 = memory.access(
        address=(0, 1),
        write_data=(0, 0, 0, 0),
        memory_read=1,
        memory_write=0,
        clock=0,
    )

    assert result0 == data0
    assert result1 == data1


def test_memory_write_disabled():
    memory = MemoryInterface()

    original_data = (1, 0, 1, 1)
    new_data = (0, 1, 0, 0)

    memory.access(
        address=(0, 0),
        write_data=original_data,
        memory_read=0,
        memory_write=1,
        clock=0,
    )

    memory.access(
        address=(0, 0),
        write_data=original_data,
        memory_read=0,
        memory_write=1,
        clock=1,
    )

    memory.access(
        address=(0, 0),
        write_data=new_data,
        memory_read=0,
        memory_write=0,
        clock=0,
    )

    memory.access(
        address=(0, 0),
        write_data=new_data,
        memory_read=0,
        memory_write=0,
        clock=1,
    )

    result = memory.access(
        address=(0, 0),
        write_data=(0, 0, 0, 0),
        memory_read=1,
        memory_write=0,
        clock=0,
    )

    assert result == original_data


def test_all_memory_addresses():
    memory = MemoryInterface()

    values = {
        (0, 0): (1, 0, 0, 0),
        (0, 1): (0, 1, 0, 0),
        (1, 0): (0, 0, 1, 0),
        (1, 1): (0, 0, 0, 1),
    }

    for address, data in values.items():

        memory.access(
            address=address,
            write_data=data,
            memory_read=0,
            memory_write=1,
            clock=0,
        )

        memory.access(
            address=address,
            write_data=data,
            memory_read=0,
            memory_write=1,
            clock=1,
        )

    for address, expected in values.items():

        result = memory.access(
            address=address,
            write_data=(0, 0, 0, 0),
            memory_read=1,
            memory_write=0,
            clock=0,
        )

        assert result == expected


def test_invalid_address_length():
    memory = MemoryInterface()

    with pytest.raises(ValueError):
        memory.access(
            address=(0,),
            write_data=(1, 0, 1, 0),
            memory_read=1,
            memory_write=0,
            clock=0,
        )


def test_invalid_address_bit():
    memory = MemoryInterface()

    with pytest.raises(ValueError):
        memory.access(
            address=(0, 2),
            write_data=(1, 0, 1, 0),
            memory_read=1,
            memory_write=0,
            clock=0,
        )


def test_invalid_data_length():
    memory = MemoryInterface()

    with pytest.raises(ValueError):
        memory.access(
            address=(0, 0),
            write_data=(1, 0, 1),
            memory_read=1,
            memory_write=0,
            clock=0,
        )


def test_invalid_data_bit():
    memory = MemoryInterface()

    with pytest.raises(ValueError):
        memory.access(
            address=(0, 0),
            write_data=(1, 0, 2, 0),
            memory_read=1,
            memory_write=0,
            clock=0,
        )


def test_invalid_memory_read():
    memory = MemoryInterface()

    with pytest.raises(ValueError):
        memory.access(
            address=(0, 0),
            write_data=(1, 0, 1, 0),
            memory_read=2,
            memory_write=0,
            clock=0,
        )


def test_invalid_memory_write():
    memory = MemoryInterface()

    with pytest.raises(ValueError):
        memory.access(
            address=(0, 0),
            write_data=(1, 0, 1, 0),
            memory_read=0,
            memory_write=2,
            clock=0,
        )


def test_invalid_clock():
    memory = MemoryInterface()

    with pytest.raises(ValueError):
        memory.access(
            address=(0, 0),
            write_data=(1, 0, 1, 0),
            memory_read=0,
            memory_write=1,
            clock=2,
        )