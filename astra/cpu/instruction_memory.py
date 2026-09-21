from astra.logic.gates import and_gate
from astra.logic.mux import mux8


class InstructionMemory:
    """
    A 16 × 8-bit instruction memory.

    The memory contains sixteen 8-bit instruction words.

    Inputs:
        address:
            4-bit instruction address.

        instruction:
            8-bit instruction word to write.

        write_enable:
            Enables writing an instruction.

        clock:
            Clock signal for synchronous writes.

    Output:
        The 8-bit instruction stored at the selected address.

    Notes:
        Instruction memory is currently modeled as a simple
        synchronous storage array.

        Reading is combinational.
        Writing occurs on the rising edge of the clock.
    """

    def __init__(self) -> None:
        """Initialize sixteen 8-bit instruction locations."""

        self.memory = [
            [0, 0, 0, 0, 0, 0, 0, 0]
            for _ in range(16)
        ]

    def _validate_address(
        self,
        address: tuple[int, int, int, int]
    ) -> None:
        """Validate a 4-bit memory address."""

        if len(address) != 4:
            raise ValueError(
                "address must contain exactly 4 bits"
            )

        for bit in address:
            if bit not in (0, 1):
                raise ValueError(
                    "address bits must be 0 or 1"
                )

    def _validate_instruction(
        self,
        instruction: tuple[int, int, int, int, int, int, int, int]
    ) -> None:
        """Validate an 8-bit instruction."""

        if len(instruction) != 8:
            raise ValueError(
                "instruction must contain exactly 8 bits"
            )

        for bit in instruction:
            if bit not in (0, 1):
                raise ValueError(
                    "instruction bits must be 0 or 1"
                )

    def _address_to_int(
        self,
        address: tuple[int, int, int, int]
    ) -> int:
        """Convert a 4-bit address into an integer."""

        return (
            address[0] * 8
            + address[1] * 4
            + address[2] * 2
            + address[3]
        )

    def read(
        self,
        address: tuple[int, int, int, int]
    ) -> tuple[int, int, int, int, int, int, int, int]:
        """
        Read an instruction from memory.

        Reading is combinational and does not require a clock.
        """

        self._validate_address(address)

        index = self._address_to_int(address)

        return tuple(self.memory[index])

    def write(
        self,
        address: tuple[int, int, int, int],
        instruction: tuple[int, int, int, int, int, int, int, int],
        write_enable: int,
        clock: int,
    ) -> None:
        """
        Write an instruction into memory.

        Writing occurs on the rising edge when write_enable is 1.
        """

        self._validate_address(address)
        self._validate_instruction(instruction)

        if write_enable not in (0, 1):
            raise ValueError(
                "write_enable must be 0 or 1"
            )

        if clock not in (0, 1):
            raise ValueError(
                "clock must be 0 or 1"
            )

        if write_enable == 1 and clock == 1:
            index = self._address_to_int(address)
            self.memory[index] = list(instruction)