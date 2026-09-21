from astra.cpu.cpu_cycle import CPUCycle
from astra.cpu.instruction_memory import InstructionMemory


class CPU:
    """
    Top-level Astra CPU.

    The CPU executes instructions using CPUCycle.

    Public operations:

        step() -> execute one instruction
        run()  -> execute until HALT
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

        self.cycle = CPUCycle(
            instruction_memory
        )

    def step(self):
        """
        Execute one complete instruction.

        A CPU instruction consists of two clock phases:

            clock = 0
            clock = 1

        Returns:

            (decoded_instruction, result)
        """

        decoded, result = self.cycle.cycle(
            clock=0
        )

        # If the CPU was already halted before this step.
        if decoded is None:
            return None, result

        second_decoded, second_result = self.cycle.cycle(
            clock=1
        )

        # HALT sets halted during clock 0.
        #
        # Therefore clock 1 returns (None, None).
        # The instruction executed during clock 0 is
        # still the result of this CPU step.
        if second_decoded is None:
            return decoded, result

        return second_decoded, second_result

    def run(self):
        """
        Execute instructions until HALT.

        Returns the number of instructions executed.
        """

        instruction_count = 0

        while not self.cycle.halted:

            self.step()

            instruction_count += 1

        return instruction_count