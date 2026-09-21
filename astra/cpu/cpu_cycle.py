from astra.cpu.control_unit import ControlUnit
from astra.cpu.datapath import Datapath
from astra.cpu.fetch_decode import FetchDecode
from astra.cpu.fetch_unit import FetchUnit
from astra.cpu.instruction_memory import InstructionMemory
from astra.isa.decoder import InstructionDecoder
from astra.isa.instructions import Instruction
from astra.logic.sequential import ProgramCounter4Bit


class CPUCycle:
    """
    Executes one CPU instruction cycle.

    Current supported instructions:

        ADD
        SUB
        AND
        OR
        XOR
        NOT

    CPU cycle:

        1. Fetch instruction using the Program Counter.
        2. Decode the instruction.
        3. Generate control signals.
        4. Execute the instruction through the datapath.
        5. Increment the Program Counter.

    LOAD, STORE, JUMP, and HALT are intentionally
    handled in later CPU-cycle stages.
    """

    def __init__(
        self,
        instruction_memory: InstructionMemory,
    ) -> None:

        if not isinstance(
            instruction_memory,
            InstructionMemory
        ):
            raise TypeError(
                "instruction_memory must be an InstructionMemory"
            )

        self.program_counter = ProgramCounter4Bit()

        self.instruction_memory = instruction_memory

        self.fetch_unit = FetchUnit(
            instruction_memory
        )

        self.decoder = InstructionDecoder()

        self.fetch_decode = FetchDecode(
            self.fetch_unit,
            self.decoder
        )

        self.control_unit = ControlUnit()

        self.datapath = Datapath()

    @staticmethod
    def _dict_to_instruction(
        decoded: dict
    ) -> Instruction:
        """
        Convert the current InstructionDecoder dictionary
        representation into an Instruction object.

        The current decoder returns:

            {
                "opcode": ...,
                "destination": ...,
                "source": ...,
                "address": ...
            }

        Datapath and ControlUnit currently operate on
        Instruction objects, so this method provides the
        interface between the two representations.
        """

        return Instruction(
            opcode=decoded["opcode"],
            destination=decoded["destination"],
            source=decoded["source"],
            address=decoded["address"],
        )

    def cycle(
        self,
        clock: int,
    ):
        """
        Execute one CPU cycle.

        Returns:
            (
                decoded_instruction,
                result
            )

        decoded_instruction:
            Dictionary returned by InstructionDecoder.

        result:
            ALU result for an ALU instruction.
        """

        if clock not in (0, 1):
            raise ValueError(
                "clock must be 0 or 1"
            )

        # --------------------------------------------------
        # 1. FETCH
        # --------------------------------------------------

        pc = tuple(
            register.dff.slave.latch.q
            for register in self.program_counter.register.registers
        )

        decoded = self.fetch_decode.fetch_and_decode(
            pc
        )

        # --------------------------------------------------
        # 2. CONVERT DECODER OUTPUT
        # --------------------------------------------------

        instruction = self._dict_to_instruction(
            decoded
        )

        # --------------------------------------------------
        # 3. CONTROL
        # --------------------------------------------------

        control_signals = self.control_unit.decode(
            instruction
        )

        # --------------------------------------------------
        # 4. EXECUTE
        # --------------------------------------------------

        result = None

        if control_signals.register_write == 1:
            result = self.datapath.execute(
                instruction,
                clock
            )

        # --------------------------------------------------
        # 5. UPDATE PROGRAM COUNTER
        # --------------------------------------------------

        self.program_counter.update(
            load_data=(0, 0, 0, 0),
            load=0,
            increment=control_signals.pc_increment,
            reset=0,
            clock=clock
        )

        return decoded, result