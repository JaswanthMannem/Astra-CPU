from astra.logic.gates import validate_bit, and_gate, or_gate, not_gate
from astra.logic.mux import mux, mux_4bit
from astra.logic.adder import ripple_carry_adder


class SRLatch:
    """
    NOR-based SR latch.

    Inputs:
        S: Set
        R: Reset

    Outputs:
        Q: stored state
        Q_bar: inverse of Q
    """

    def __init__(self) -> None:
        self.q = 0
        self.q_bar = 1

    def update(self, s: int, r: int) -> tuple[int, int]:
        s = validate_bit(s)
        r = validate_bit(r)

        if s == 1 and r == 1:
            raise ValueError("Invalid input: S and R cannot both be 1.")

        if s == 1:
            self.q = 1
            self.q_bar = 0

        elif r == 1:
            self.q = 0
            self.q_bar = 1

        # S=0, R=0 → hold previous state

        return self.q, self.q_bar

class DLatch:
    """
    D (Data) latch.

    Inputs:
        D: data
        Enable: controls whether the latch accepts new data

    Outputs:
        Q: stored state
        Q_bar: inverse of Q
    """

    def __init__(self) -> None:
        self.latch = SRLatch()

    def update(self, d: int, enable: int) -> tuple[int, int]:
        d = validate_bit(d)
        enable = validate_bit(enable)

        s = and_gate(d, enable)
        r = and_gate(not_gate(d), enable)

        return self.latch.update(s, r)

class DFlipFlop:
    """
    Rising-edge triggered D flip-flop.

    Inputs:
        D: data
        Clock: clock signal

    Output:
        Q: stored state
        Q_bar: inverse of Q
    """

    def __init__(self) -> None:
        self.master = DLatch()
        self.slave = DLatch()

    def update(self, d: int, clock: int) -> tuple[int, int]:
        d = validate_bit(d)
        clock = validate_bit(clock)

        master_q, _ = self.master.update(
            d,
            not_gate(clock)
        )

        q, q_bar = self.slave.update(
            master_q,
            clock
        )
        
        return q, q_bar

class Register1Bit:
    """
    A 1-bit register built using a D flip-flop and a multiplexer.

    The register stores one bit of data.

    Inputs:
        d:     Data bit to potentially store.
        load:  If 1, load the value of d.
               If 0, keep the current value.
        clock: Clock signal.

    Output:
        The current stored value Q.

    Behavior:
        - The stored value changes only on the rising edge of the clock.
        - load = 1 -> store d.
        - load = 0 -> keep the current value.
    """

    def __init__(self) -> None:
        """Initialize the register with a D flip-flop."""
        self.dff = DFlipFlop()

    def update(self, d: int, load: int, clock: int) -> int:
        """
        Update the register according to the input signals.

        The multiplexer selects either:
            - the current Q value when load = 0
            - the new D value when load = 1

        The selected value is then passed to the D flip-flop.
        """
        current_q = self.dff.slave.latch.q

        next_d = mux(current_q, d, load)

        q, _ = self.dff.update(next_d, clock)

        return q

class Register4Bit:
    """
    A 4-bit register built using four independent 1-bit registers.

    The register stores four bits of data and supports loading or
    retaining the current value.

    Inputs:
        d:     4-bit data to potentially store.
        load:  If 1, load the new data on the rising clock edge.
               If 0, retain the current value.
        clock: Clock signal.

    Output:
        The current 4-bit stored value.
    """

    def __init__(self) -> None:
        """Initialize four independent 1-bit registers."""
        self.registers = (
            Register1Bit(),
            Register1Bit(),
            Register1Bit(),
            Register1Bit()
        )

    def update(
        self,
        d: tuple[int, int, int, int],
        load: int,
        clock: int
    ) -> tuple[int, int, int, int]:
        """
        Update all four register bits.

        Each input bit is passed to its own Register1Bit, allowing
        all four bits to be stored independently.
        """
        result_bits = []

        for i in range(4):
            q = self.registers[i].update(d[i], load, clock)
            result_bits.append(q)

        return tuple(result_bits)

class Counter4Bit:
    """
    A 4-bit counter built using a 4-bit register and a ripple-carry adder.

    The counter increments its stored value by 1 on each rising clock
    edge when enable is 1. When enable is 0, the current value is held.

    The counter naturally wraps around from 1111 to 0000 because it
    operates on 4-bit values.

    Inputs:
        enable: If 1, increment the counter.
                If 0, retain the current value.
        clock:  Clock signal.

    Output:
        The current 4-bit counter value.
    """

    def __init__(self) -> None:
        """Initialize the counter with a 4-bit register."""
        self.register = Register4Bit()

    def update(self, enable: int, clock: int) -> tuple[int, int, int, int]:
        """
        Update the counter according to enable and clock.

        The current value is incremented using a 4-bit adder.
        A multiplexer selects either the current value or the
        incremented value based on enable. The selected value
        is then stored in the register on the rising clock edge.
        """

        current_q = tuple(
            register.dff.slave.latch.q
            for register in self.register.registers
        )

        incremented_q, _ = ripple_carry_adder(
            current_q,
            (0, 0, 0, 1)
        )

        next_value = mux_4bit(
            current_q,
            incremented_q,
            enable
        )

        q = self.register.update(
            next_value,
            1,
            clock
        )

        return q
        
