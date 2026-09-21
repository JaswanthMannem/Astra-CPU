from astra.cpu.cpu_cycle import CPUCycle
from astra.cpu.instruction_memory import InstructionMemory


class CPU:
    def __init__(self, instruction_memory):
        if not isinstance(instruction_memory, InstructionMemory):
            raise TypeError(
                "instruction_memory must be an InstructionMemory"
            )

        self.instruction_memory = instruction_memory
        self.cycle = CPUCycle(instruction_memory)

    def reset(self):
        """Reset CPU execution state while preserving the loaded program."""

        zero = (0, 0, 0, 0)

        # Reset Program Counter
        self.cycle.program_counter.update(
            load_data=zero,
            load=1,
            increment=0,
            reset=0,
            clock=0,
        )

        self.cycle.program_counter.update(
            load_data=zero,
            load=1,
            increment=0,
            reset=0,
            clock=1,
        )

        # Reset Register File
        for address in (
            (0, 0),
            (0, 1),
            (1, 0),
            (1, 1),
        ):
            self.cycle.datapath.register_file.update(
                write_address=address,
                write_data=zero,
                write_enable=1,
                read_address_a=address,
                read_address_b=address,
                clock=0,
            )

            self.cycle.datapath.register_file.update(
                write_address=address,
                write_data=zero,
                write_enable=1,
                read_address_a=address,
                read_address_b=address,
                clock=1,
            )

        # Reset Data Memory
        for address_value in range(16):
            address = (
                (address_value // 8) % 2,
                (address_value // 4) % 2,
                (address_value // 2) % 2,
                address_value % 2,
            )

            self.cycle.data_memory.update(
                address=address,
                data=zero,
                write_enable=1,
                clock=0,
            )

            self.cycle.data_memory.update(
                address=address,
                data=zero,
                write_enable=1,
                clock=1,
            )

        # Clear HALT state
        self.cycle.halted = False

    def step(self):
        decoded, result = self.cycle.cycle(clock=0)

        if decoded is None:
            return None, result

        second_decoded, second_result = self.cycle.cycle(clock=1)

        if second_decoded is None:
            return decoded, result

        return second_decoded, second_result

    def run(self):
        instruction_count = 0

        while not self.cycle.halted:
            self.step()
            instruction_count += 1

        return instruction_count