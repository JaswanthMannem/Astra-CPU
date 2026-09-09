import pytest

from astra.logic.sequential import SRLatch, DLatch, DFlipFlop, Register1Bit, Register4Bit, Counter4Bit, RegisterFile


def test_sr_latch_initial_state():
    latch = SRLatch()

    assert latch.update(0, 0) == (0, 1)


def test_sr_latch_set():
    latch = SRLatch()

    assert latch.update(1, 0) == (1, 0)


def test_sr_latch_hold_after_set():
    latch = SRLatch()

    latch.update(1, 0)

    assert latch.update(0, 0) == (1, 0)


def test_sr_latch_reset():
    latch = SRLatch()

    latch.update(1, 0)

    assert latch.update(0, 1) == (0, 1)


def test_sr_latch_hold_after_reset():
    latch = SRLatch()

    latch.update(1, 0)
    latch.update(0, 1)

    assert latch.update(0, 0) == (0, 1)


def test_sr_latch_set_reset_set():
    latch = SRLatch()

    latch.update(1, 0)
    latch.update(0, 1)

    assert latch.update(1, 0) == (1, 0)


def test_sr_latch_invalid_state():
    latch = SRLatch()

    with pytest.raises(ValueError):
        latch.update(1, 1)

def test_d_latch_initial_state():
    latch = DLatch()

    assert latch.update(0, 0) == (0, 1)


def test_d_latch_store_one():
    latch = DLatch()

    assert latch.update(1, 1) == (1, 0)


def test_d_latch_store_zero():
    latch = DLatch()

    latch.update(1, 1)

    assert latch.update(0, 1) == (0, 1)


def test_d_latch_hold_one():
    latch = DLatch()

    latch.update(1, 1)

    assert latch.update(0, 0) == (1, 0)


def test_d_latch_hold_zero():
    latch = DLatch()

    latch.update(0, 1)

    assert latch.update(1, 0) == (0, 1)


def test_d_latch_enable_changes_data():
    latch = DLatch()

    assert latch.update(1, 1) == (1, 0)
    assert latch.update(0, 1) == (0, 1)
    assert latch.update(1, 0) == (0, 1)

def test_d_flip_flop_initial_state():
    flip_flop = DFlipFlop()

    assert flip_flop.update(0, 0) == (0, 1)


def test_d_flip_flop_rising_edge_captures_one():
    flip_flop = DFlipFlop()

    flip_flop.update(1, 0)

    assert flip_flop.update(1, 1) == (1, 0)


def test_d_flip_flop_rising_edge_captures_zero():
    flip_flop = DFlipFlop()

    flip_flop.update(1, 0)
    flip_flop.update(1, 1)

    flip_flop.update(0, 0)

    assert flip_flop.update(0, 1) == (0, 1)


def test_d_flip_flop_holds_between_edges():
    flip_flop = DFlipFlop()

    flip_flop.update(1, 0)
    flip_flop.update(1, 1)

    # Change D while clock remains HIGH.
    assert flip_flop.update(0, 1) == (1, 0)


def test_d_flip_flop_does_not_capture_on_falling_edge():
    flip_flop = DFlipFlop()

    flip_flop.update(1, 0)
    flip_flop.update(1, 1)

    # D changes while clock goes LOW.
    flip_flop.update(0, 0)

    # Q should still contain the previous value.
    assert flip_flop.update(0, 0) == (1, 0)

def test_register1bit_initial_state():
    register = Register1Bit()

    assert register.update(0, 0, 0) == 0


def test_register1bit_loads_data_on_rising_edge():
    register = Register1Bit()

    # Before rising edge, Q should remain unchanged
    assert register.update(1, 1, 0) == 0

    # Rising edge -> load D
    assert register.update(1, 1, 1) == 1


def test_register1bit_holds_when_load_is_zero():
    register = Register1Bit()

    # Store 1
    register.update(1, 1, 0)
    assert register.update(1, 1, 1) == 1

    # load = 0 -> keep 1
    assert register.update(0, 0, 0) == 1
    assert register.update(0, 0, 1) == 1


def test_register1bit_can_load_zero():
    register = Register1Bit()

    # First store 1
    register.update(1, 1, 0)
    assert register.update(1, 1, 1) == 1

    # Now load 0
    assert register.update(0, 1, 0) == 1
    assert register.update(0, 1, 1) == 0


def test_register1bit_does_not_change_without_rising_edge():
    register = Register1Bit()

    # Store 1
    register.update(1, 1, 0)
    assert register.update(1, 1, 1) == 1

    # Change D while clock remains high
    assert register.update(0, 1, 1) == 1


def test_register1bit_multiple_values():
    register = Register1Bit()

    # Load 1
    register.update(1, 1, 0)
    assert register.update(1, 1, 1) == 1

    # Hold 1
    assert register.update(0, 0, 0) == 1
    assert register.update(0, 0, 1) == 1

    # Load 0
    assert register.update(0, 1, 0) == 1
    assert register.update(0, 1, 1) == 0

    # Hold 0
    assert register.update(1, 0, 0) == 0
    assert register.update(1, 0, 1) == 0

def test_register4bit_initial_state():
    register = Register4Bit()

    assert register.update((0, 0, 0, 0), 0, 0) == (0, 0, 0, 0)


def test_register4bit_loads_data_on_rising_edge():
    register = Register4Bit()

    # Before rising edge, value should remain unchanged
    assert register.update((1, 0, 1, 0), 1, 0) == (0, 0, 0, 0)

    # Rising edge -> store data
    assert register.update((1, 0, 1, 0), 1, 1) == (1, 0, 1, 0)


def test_register4bit_holds_when_load_is_zero():
    register = Register4Bit()

    # Store 1010
    register.update((1, 0, 1, 0), 1, 0)
    assert register.update((1, 0, 1, 0), 1, 1) == (1, 0, 1, 0)

    # load = 0 -> keep 1010
    assert register.update((0, 1, 0, 1), 0, 0) == (1, 0, 1, 0)
    assert register.update((0, 1, 0, 1), 0, 1) == (1, 0, 1, 0)


def test_register4bit_can_load_new_data():
    register = Register4Bit()

    # Store 1010
    register.update((1, 0, 1, 0), 1, 0)
    assert register.update((1, 0, 1, 0), 1, 1) == (1, 0, 1, 0)

    # Load 0111
    assert register.update((0, 1, 1, 1), 1, 0) == (1, 0, 1, 0)
    assert register.update((0, 1, 1, 1), 1, 1) == (0, 1, 1, 1)


def test_register4bit_stores_each_bit_independently():
    register = Register4Bit()

    # Store 1001
    register.update((1, 0, 0, 1), 1, 0)
    assert register.update((1, 0, 0, 1), 1, 1) == (1, 0, 0, 1)

    # Change only selected bits
    assert register.update((0, 1, 0, 0), 1, 0) == (1, 0, 0, 1)
    assert register.update((0, 1, 0, 0), 1, 1) == (0, 1, 0, 0)


def test_register4bit_does_not_change_without_rising_edge():
    register = Register4Bit()

    # Store 1100
    register.update((1, 1, 0, 0), 1, 0)
    assert register.update((1, 1, 0, 0), 1, 1) == (1, 1, 0, 0)

    # Change D while clock remains high
    assert register.update((0, 0, 1, 1), 1, 1) == (1, 1, 0, 0)

def test_counter4bit_initial_state():
    counter = Counter4Bit()

    assert counter.update(0, 0) == (0, 0, 0, 0)


def test_counter4bit_increments_on_rising_edge():
    counter = Counter4Bit()

    # No rising edge yet
    assert counter.update(1, 0) == (0, 0, 0, 0)

    # Rising edge -> 0000 → 0001
    assert counter.update(1, 1) == (0, 0, 0, 1)


def test_counter4bit_multiple_increments():
    counter = Counter4Bit()

    assert counter.update(1, 0) == (0, 0, 0, 0)
    assert counter.update(1, 1) == (0, 0, 0, 1)

    assert counter.update(1, 0) == (0, 0, 0, 1)
    assert counter.update(1, 1) == (0, 0, 1, 0)

    assert counter.update(1, 0) == (0, 0, 1, 0)
    assert counter.update(1, 1) == (0, 0, 1, 1)

    assert counter.update(1, 0) == (0, 0, 1, 1)
    assert counter.update(1, 1) == (0, 1, 0, 0)


def test_counter4bit_holds_when_disabled():
    counter = Counter4Bit()

    # Count to 1
    counter.update(1, 0)
    assert counter.update(1, 1) == (0, 0, 0, 1)

    # Disable counter
    assert counter.update(0, 0) == (0, 0, 0, 1)
    assert counter.update(0, 1) == (0, 0, 0, 1)

    # Still disabled
    assert counter.update(0, 0) == (0, 0, 0, 1)
    assert counter.update(0, 1) == (0, 0, 0, 1)


def test_counter4bit_resumes_after_enable():
    counter = Counter4Bit()

    # Count to 1
    counter.update(1, 0)
    assert counter.update(1, 1) == (0, 0, 0, 1)

    # Hold at 1
    counter.update(0, 0)
    assert counter.update(0, 1) == (0, 0, 0, 1)

    # Enable again -> 2
    assert counter.update(1, 0) == (0, 0, 0, 1)
    assert counter.update(1, 1) == (0, 0, 1, 0)


def test_counter4bit_wraps_around():
    counter = Counter4Bit()

    # Reach 1111
    for _ in range(15):
        counter.update(1, 0)
        counter.update(1, 1)

    assert counter.update(0, 0) == (1, 1, 1, 1)

    # Prepare 0000 while clock is low
    assert counter.update(1, 0) == (1, 1, 1, 1)

    # Rising edge -> 1111 + 0001 → 0000
    assert counter.update(1, 1) == (0, 0, 0, 0)


def test_counter4bit_does_not_increment_without_rising_edge():
    counter = Counter4Bit()

    # Count to 1
    counter.update(1, 0)
    assert counter.update(1, 1) == (0, 0, 0, 1)

    # Clock remains high; should not increment again
    assert counter.update(1, 1) == (0, 0, 0, 1)
    assert counter.update(1, 1) == (0, 0, 0, 1)


def test_counter4bit_full_cycle():
    counter = Counter4Bit()

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

    for expected in expected_values:
        counter.update(1, 0)
        assert counter.update(1, 1) == expected

def test_register_file_initial_state():
    register_file = RegisterFile()

    assert register_file.update(
        (0, 0),
        (0, 0, 0, 0),
        0,
        (0, 0),
        0
    ) == (0, 0, 0, 0)


def test_register_file_write_r0():
    register_file = RegisterFile()

    register_file.update(
        (0, 0),
        (1, 0, 1, 0),
        1,
        (0, 0),
        0
    )

    assert register_file.update(
        (0, 0),
        (1, 0, 1, 0),
        1,
        (0, 0),
        1
    ) == (1, 0, 1, 0)


def test_register_file_write_r1():
    register_file = RegisterFile()

    register_file.update(
        (0, 1),
        (1, 1, 0, 0),
        1,
        (0, 1),
        0
    )

    assert register_file.update(
        (0, 1),
        (1, 1, 0, 0),
        1,
        (0, 1),
        1
    ) == (1, 1, 0, 0)


def test_register_file_write_r2():
    register_file = RegisterFile()

    register_file.update(
        (1, 0),
        (1, 0, 1, 0),
        1,
        (1, 0),
        0
    )

    assert register_file.update(
        (1, 0),
        (1, 0, 1, 0),
        1,
        (1, 0),
        1
    ) == (1, 0, 1, 0)


def test_register_file_write_r3():
    register_file = RegisterFile()

    register_file.update(
        (1, 1),
        (0, 1, 1, 0),
        1,
        (1, 1),
        0
    )

    assert register_file.update(
        (1, 1),
        (0, 1, 1, 0),
        1,
        (1, 1),
        1
    ) == (0, 1, 1, 0)


def test_register_file_only_selected_register_changes():
    register_file = RegisterFile()

    # Write 0011 to R0.
    register_file.update(
        (0, 0),
        (0, 0, 1, 1),
        1,
        (0, 0),
        0
    )

    register_file.update(
        (0, 0),
        (0, 0, 1, 1),
        1,
        (0, 0),
        1
    )

    # Write 1010 to R2.
    register_file.update(
        (1, 0),
        (1, 0, 1, 0),
        1,
        (1, 0),
        0
    )

    register_file.update(
        (1, 0),
        (1, 0, 1, 0),
        1,
        (1, 0),
        1
    )

    # R0 should still contain 0011.
    assert register_file.update(
        (0, 0),
        (0, 0, 0, 0),
        0,
        (0, 0),
        0
    ) == (0, 0, 1, 1)

    # R2 should contain 1010.
    assert register_file.update(
        (0, 0),
        (0, 0, 0, 0),
        0,
        (1, 0),
        0
    ) == (1, 0, 1, 0)


def test_register_file_write_disabled():
    register_file = RegisterFile()

    # Attempt to write 1111 to R1 with write disabled.
    register_file.update(
        (0, 1),
        (1, 1, 1, 1),
        0,
        (0, 1),
        0
    )

    register_file.update(
        (0, 1),
        (1, 1, 1, 1),
        0,
        (0, 1),
        1
    )

    # R1 should remain 0000.
    assert register_file.update(
        (0, 0),
        (0, 0, 0, 0),
        0,
        (0, 1),
        0
    ) == (0, 0, 0, 0)


def test_register_file_write_requires_rising_edge():
    register_file = RegisterFile()

    # Write is prepared while clock is low.
    assert register_file.update(
        (1, 0),
        (1, 1, 0, 1),
        1,
        (1, 0),
        0
    ) == (0, 0, 0, 0)

    # Rising edge commits the value.
    assert register_file.update(
        (1, 0),
        (1, 1, 0, 1),
        1,
        (1, 0),
        1
    ) == (1, 1, 0, 1)


def test_register_file_read_all_registers():
    register_file = RegisterFile()

    # R0 = 0011
    register_file.update((0, 0), (0, 0, 1, 1), 1, (0, 0), 0)
    register_file.update((0, 0), (0, 0, 1, 1), 1, (0, 0), 1)

    # R1 = 0101
    register_file.update((0, 1), (0, 1, 0, 1), 1, (0, 1), 0)
    register_file.update((0, 1), (0, 1, 0, 1), 1, (0, 1), 1)

    # R2 = 1001
    register_file.update((1, 0), (1, 0, 0, 1), 1, (1, 0), 0)
    register_file.update((1, 0), (1, 0, 0, 1), 1, (1, 0), 1)

    # R3 = 1110
    register_file.update((1, 1), (1, 1, 1, 0), 1, (1, 1), 0)
    register_file.update((1, 1), (1, 1, 1, 0), 1, (1, 1), 1)

    # Read R0
    assert register_file.update(
        (0, 0), (0, 0, 0, 0), 0, (0, 0), 0
    ) == (0, 0, 1, 1)

    # Read R1
    assert register_file.update(
        (0, 0), (0, 0, 0, 0), 0, (0, 1), 0
    ) == (0, 1, 0, 1)

    # Read R2
    assert register_file.update(
        (0, 0), (0, 0, 0, 0), 0, (1, 0), 0
    ) == (1, 0, 0, 1)

    # Read R3
    assert register_file.update(
        (0, 0), (0, 0, 0, 0), 0, (1, 1), 0
    ) == (1, 1, 1, 0)