from astra.cpu.instruction_memory import InstructionMemory


class FetchUnit:
    """
    Fetches instruction words from Instruction Memory.

    The Fetch Unit connects the Program Counter address
    to the Instruction Memory.

    PC:
        4-bit address

    Instruction Memory:
        16 × 8-bit

    Output:
        8-bit instruction word
    """

    def __init__(
        self,
        instruction_memory: InstructionMemory
    ) -> None:
        """
        Initialize the Fetch Unit.

        Args:
            instruction_memory:
                Instruction memory used by the CPU.
        """

        if not isinstance(
            instruction_memory,
            InstructionMemory
        ):
            raise TypeError(
                "instruction_memory must be an InstructionMemory"
            )

        self.instruction_memory = instruction_memory

    def fetch(
        self,
        program_counter: tuple[int, int, int, int]
    ) -> tuple[
        int, int, int, int,
        int, int, int, int
    ]:
        """
        Fetch the instruction at the current PC address.

        Args:
            program_counter:
                4-bit program counter value.

        Returns:
            8-bit instruction word.
        """

        if len(program_counter) != 4:
            raise ValueError(
                "program_counter must contain exactly 4 bits"
            )

        for bit in program_counter:
            if bit not in (0, 1):
                raise ValueError(
                    "program_counter bits must be 0 or 1"
                )

        return self.instruction_memory.read(
            program_counter
        )