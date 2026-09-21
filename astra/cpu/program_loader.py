from astra.cpu.instruction_memory import InstructionMemory
from astra.isa.instructions import Instruction, Opcode


class ProgramLoader:
    """
    Loads Astra instructions into instruction memory.

    LOAD and STORE occupy two instruction-memory words.
    All other instructions occupy one word.
    """

    def __init__(
        self,
        instruction_memory: InstructionMemory
    ) -> None:

        if not isinstance(
            instruction_memory,
            InstructionMemory
        ):
            raise TypeError(
                "instruction_memory must be an InstructionMemory"
            )

        self.instruction_memory = instruction_memory

    @staticmethod
    def _address_to_bits(
        address: int
    ) -> tuple[int, int, int, int]:

        return (
            (address // 8) % 2,
            (address // 4) % 2,
            (address // 2) % 2,
            address % 2,
        )

    @staticmethod
    def _instruction_size(
        instruction: Instruction
    ) -> int:

        if instruction.opcode in (
            Opcode.LOAD,
            Opcode.STORE,
        ):
            return 2

        return 1

    def load(
        self,
        program: list[Instruction]
    ) -> None:

        if not isinstance(program, list):
            raise TypeError(
                "program must be a list"
            )

        address = 0

        for instruction in program:

            if not isinstance(
                instruction,
                Instruction
            ):
                raise TypeError(
                    "program must contain only Instruction objects"
                )

            encoded = instruction.encode()

            expected_size = self._instruction_size(
                instruction
            )

            if len(encoded) != expected_size:
                raise ValueError(
                    "instruction encoding size does not match instruction size"
                )

            if address + expected_size > 16:
                raise ValueError(
                    "program does not fit in instruction memory"
                )

            for word in encoded:

                memory_address = self._address_to_bits(
                    address
                )

                self.instruction_memory.write(
                    address=memory_address,
                    instruction=word,
                    write_enable=1,
                    clock=0,
                )

                self.instruction_memory.write(
                    address=memory_address,
                    instruction=word,
                    write_enable=1,
                    clock=1,
                )

                address += 1