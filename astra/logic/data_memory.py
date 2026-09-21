from astra.logic.decoder import decoder
from astra.logic.gates import and_gate
from astra.logic.mux import mux_4bit
from astra.logic.sequential import Register4Bit


def _mux4_4bit(
    i0: tuple[int, int, int, int],
    i1: tuple[int, int, int, int],
    i2: tuple[int, int, int, int],
    i3: tuple[int, int, int, int],
    s1: int,
    s0: int,
) -> tuple[int, int, int, int]:

    x = mux_4bit(i0, i1, s0)
    y = mux_4bit(i2, i3, s0)

    return mux_4bit(x, y, s1)


class DataMemory16x4:

    def __init__(self) -> None:
        self.memory = tuple(
            Register4Bit()
            for _ in range(16)
        )

    @staticmethod
    def _validate_address(
        address: tuple[int, int, int, int]
    ) -> None:

        if not isinstance(address, tuple):
            raise TypeError(
                "address must be a tuple"
            )

        if len(address) != 4:
            raise ValueError(
                "address must contain exactly 4 bits"
            )

        for bit in address:
            if bit not in (0, 1):
                raise ValueError(
                    "address bits must be 0 or 1"
                )

    @staticmethod
    def _validate_data(
        data: tuple[int, int, int, int]
    ) -> None:

        if not isinstance(data, tuple):
            raise TypeError(
                "data must be a tuple"
            )

        if len(data) != 4:
            raise ValueError(
                "data must contain exactly 4 bits"
            )

        for bit in data:
            if bit not in (0, 1):
                raise ValueError(
                    "data bits must be 0 or 1"
                )

    @staticmethod
    def _validate_control(
        value: int,
        name: str
    ) -> None:

        if value not in (0, 1):
            raise ValueError(
                f"{name} must be 0 or 1"
            )

    def update(
        self,
        address: tuple[int, int, int, int],
        data: tuple[int, int, int, int],
        write_enable: int,
        clock: int
    ) -> tuple[int, int, int, int]:

        self._validate_address(address)
        self._validate_data(data)

        self._validate_control(
            write_enable,
            "write_enable"
        )

        self._validate_control(
            clock,
            "clock"
        )

        # ---------------------------------------------
        # 4-to-16 decoder
        # ---------------------------------------------

        high_select = decoder(
            address[0],
            address[1]
        )

        low_select = decoder(
            address[2],
            address[3]
        )

        write_select = []

        for high_bit in high_select:
            for low_bit in low_select:
                write_select.append(
                    and_gate(
                        high_bit,
                        low_bit
                    )
                )

        # ---------------------------------------------
        # Write to memory registers
        # ---------------------------------------------

        memory_values = []

        for i in range(16):

            load = and_gate(
                write_enable,
                write_select[i]
            )

            memory_value = self.memory[i].update(
                data,
                load,
                clock
            )

            memory_values.append(
                memory_value
            )

        # ---------------------------------------------
        # Read path
        #
        # 16 × 4-bit
        #       ↓
        # four 4-to-1 4-bit MUXes
        #       ↓
        # one 4-to-1 4-bit MUX
        #       ↓
        # 4-bit output
        # ---------------------------------------------

        level_1 = (
            _mux4_4bit(
                memory_values[0],
                memory_values[1],
                memory_values[2],
                memory_values[3],
                address[2],
                address[3],
            ),

            _mux4_4bit(
                memory_values[4],
                memory_values[5],
                memory_values[6],
                memory_values[7],
                address[2],
                address[3],
            ),

            _mux4_4bit(
                memory_values[8],
                memory_values[9],
                memory_values[10],
                memory_values[11],
                address[2],
                address[3],
            ),

            _mux4_4bit(
                memory_values[12],
                memory_values[13],
                memory_values[14],
                memory_values[15],
                address[2],
                address[3],
            ),
        )

        return _mux4_4bit(
            level_1[0],
            level_1[1],
            level_1[2],
            level_1[3],
            address[0],
            address[1],
        )