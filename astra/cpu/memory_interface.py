from astra.logic.sequential import RAM4Bit


class MemoryInterface:
    """
    Interface between the CPU and the 4 × 4-bit RAM.

    The current RAM contains:

        4 memory locations
        4 bits per location

    Therefore:

        address = 2 bits
        data    = 4 bits

    The Memory Interface separates the CPU-level memory
    read/write control from the underlying RAM implementation.
    """

    def __init__(self) -> None:
        """Initialize the memory interface."""

        self.ram = RAM4Bit()

    def access(
        self,
        address: tuple[int, int],
        write_data: tuple[int, int, int, int],
        memory_read: int,
        memory_write: int,
        clock: int,
    ) -> tuple[int, int, int, int]:
        """
        Perform a memory access.

        Args:
            address:
                2-bit memory address.

            write_data:
                4-bit data that may be written to memory.

            memory_read:
                Enables memory read.

            memory_write:
                Enables memory write.

            clock:
                Clock signal.

        Returns:
            4-bit value read from memory.

        Behavior:

            memory_read = 1
                Read the selected memory location.

            memory_write = 1
                Write write_data to the selected location.

            memory_read = 0
                Return zero.

            memory_write = 0
                No memory location is written.
        """

        if len(address) != 2:
            raise ValueError(
                "address must contain exactly 2 bits"
            )

        for bit in address:
            if bit not in (0, 1):
                raise ValueError(
                    "address bits must be 0 or 1"
                )

        if len(write_data) != 4:
            raise ValueError(
                "write_data must contain exactly 4 bits"
            )

        for bit in write_data:
            if bit not in (0, 1):
                raise ValueError(
                    "write_data bits must be 0 or 1"
                )

        if memory_read not in (0, 1):
            raise ValueError(
                "memory_read must be 0 or 1"
            )

        if memory_write not in (0, 1):
            raise ValueError(
                "memory_write must be 0 or 1"
            )

        if clock not in (0, 1):
            raise ValueError(
                "clock must be 0 or 1"
            )

        memory_data = self.ram.update(
            address=address,
            data=write_data,
            write_enable=memory_write,
            clock=clock,
        )

        if memory_read == 0:
            return (0, 0, 0, 0)

        return memory_data