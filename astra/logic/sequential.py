from astra.logic.gates import validate_bit, and_gate, or_gate, not_gate
from astra.logic.mux import mux, mux4, mux_4bit
from astra.logic.adder import ripple_carry_adder
from astra.logic.decoder import decoder


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

class RegisterFile:
    """
    A 4 × 4-bit register file.

    The register file contains four independent 4-bit registers and
    provides one write port and one read port.

    Inputs:
        write_address: 2-bit address selecting the register to write.
                       00 -> R0
                       01 -> R1
                       10 -> R2
                       11 -> R3

        write_data:    4-bit value to write.

        write_enable:  If 1, the selected register is written on the
                       rising edge of the clock.
                       If 0, all registers retain their values.

        read_address:  2-bit address selecting the register to read.

        clock:         Clock signal.

    Output:
        The current 4-bit value of the register selected by
        read_address.

    Behavior:
        - Writing occurs only on the rising edge of the clock.
        - Only the register selected by write_address is written.
        - Reading is combinational and does not require a clock edge.
    """

    def __init__(self) -> None:
        """Initialize four independent 4-bit registers."""
        self.registers = (
            Register4Bit(),
            Register4Bit(),
            Register4Bit(),
            Register4Bit()
        )

    def update(
        self,
        write_address: tuple[int, int],
        write_data: tuple[int, int, int, int],
        write_enable: int,
        read_address: tuple[int, int],
        clock: int
    ) -> tuple[int, int, int, int]:
        """
        Perform a register-file write and return the selected read value.

        The write address is decoded into four one-hot signals. Each
        signal is combined with write_enable to determine whether its
        corresponding register should load the new data.

        The four register outputs are then passed through a 4-to-1
        4-bit multiplexer controlled by read_address.
        """

        register_values = []

        # Decode the write address to select one register.
        write_select = decoder(write_address[0], write_address[1])

        # Update all registers. Only the selected register receives
        # an active load signal.
        for i in range(4):
            load = and_gate(write_enable, write_select[i])
            register_value = self.registers[i].update(
                write_data,
                load,
                clock
            )
            register_values.append(register_value)

        # Build a 4-to-1 4-bit multiplexer using 2-to-1 4-bit MUXes.
        output1 = mux_4bit(
            register_values[0],
            register_values[1],
            read_address[1]
        )

        output2 = mux_4bit(
            register_values[2],
            register_values[3],
            read_address[1]
        )

        return mux_4bit(
            output1,
            output2,
            read_address[0]
        )

class RAM4Bit:
    """
    A 4 × 4-bit RAM.

    The RAM contains four 4-bit memory locations addressed by a 2-bit address.

    Inputs:
        address: 2-bit memory address.
        data: 4-bit value to write.
        write_enable: Enables writing to the selected memory location.
        clock: Clock signal for synchronous writes.

    Output:
        The current 4-bit value stored at the selected memory address.

    Behavior:
        - Writes occur only on the rising edge of the clock.
        - Reads are combinational.
        - Only the addressed memory location is written.
    """

    def __init__(self) -> None:
        """Initialize four independent 4-bit memory locations."""
        self.memory = (
            Register4Bit(),
            Register4Bit(),
            Register4Bit(),
            Register4Bit()
        )

    def update(
        self,
        address: tuple[int, int],
        data: tuple[int, int, int, int],
        write_enable: int,
        clock: int
    ) -> tuple[int, int, int, int]:

        memory_values = []

        write_select = decoder(address[0], address[1])

        for i in range(4):
            load = and_gate(write_enable, write_select[i])

            memory_value = self.memory[i].update(
                data,
                load,
                clock
            )

            memory_values.append(memory_value)

        output1 = mux_4bit(
            memory_values[0],
            memory_values[1],
            address[1]
        )

        output2 = mux_4bit(
            memory_values[2],
            memory_values[3],
            address[1]
        )

        return mux_4bit(
            output1,
            output2,
            address[0]
        )

class ProgramCounter4Bit:
    """
    A 4-bit Program Counter (PC).

    The program counter stores the address of the next instruction
    to be executed by the CPU.

    Inputs:
        load_data:    4-bit value to load into the PC.
        load:         If 1, load load_data into the PC.
        increment:    If 1, increment the current PC by 1.
        reset:        If 1, reset the PC to 0000.
        clock:        Clock signal.

    Output:
        The current 4-bit PC value.

    Operation priority:
        reset > load > increment > hold

    Behavior:
        - Reset sets the PC to 0000.
        - Load replaces the current PC with load_data.
        - Increment increases the PC by 1.
        - If no operation is enabled, the PC holds its value.
        - Updates occur on the rising edge of the clock.
        - Incrementing 1111 wraps around to 0000.
    """

    def __init__(self) -> None:
        self.register = Register4Bit()

    def update(
        self,
        load_data: tuple[int, int, int, int],
        load: int,
        increment: int,
        reset: int,
        clock: int
    ) -> tuple[int, int, int, int]:

        current_data = tuple(
            register.dff.slave.latch.q
            for register in self.register.registers
        )

        # Calculate PC + 1.
        incremented_data, _ = ripple_carry_adder(
            current_data,
            (0, 0, 0, 1)
        )

        # Priority: increment < load < reset.
        incremented_result = mux_4bit(
            current_data,
            incremented_data,
            increment
        )

        loaded_result = mux_4bit(
            incremented_result,
            load_data,
            load
        )

        next_data = mux_4bit(
            loaded_result,
            (0, 0, 0, 0),
            reset
        )

        # Store the selected next value on the clock edge.
        q = self.register.update(
            next_data,
            1,
            clock
        )

        return q