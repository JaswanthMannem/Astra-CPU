from astra.cpu.control_unit import ControlUnit
from astra.cpu.datapath import Datapath, _register_to_bits
from astra.cpu.fetch_decode import FetchDecode
from astra.cpu.fetch_unit import FetchUnit
from astra.cpu.instruction_memory import InstructionMemory
from astra.isa.decoder import InstructionDecoder
from astra.isa.instructions import Instruction, Opcode
from astra.logic.data_memory import DataMemory16x4
from astra.logic.sequential import ProgramCounter4Bit


class CPUCycle:
    """
    Executes one CPU instruction cycle.

    Supported instructions:

        ADD
        SUB
        AND
        OR
        XOR
        NOT
        LOAD
        STORE
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
        self.data_memory = DataMemory16x4()

    @staticmethod
    def _dict_to_instruction(
        decoded: dict
    ) -> Instruction:

        return Instruction(
            opcode=decoded["opcode"],
            destination=decoded["destination"],
            source=decoded["source"],
            address=decoded["address"],
        )

    @staticmethod
    def _bits_to_address(
        bits: tuple[int, int, int, int]
    ) -> int:

        value = 0

        for bit in bits:
            value = value * 2 + bit

        return value

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

    def _current_pc(
        self
    ) -> tuple[int, int, int, int]:

        return tuple(
            register.dff.slave.latch.q
            for register
            in self.program_counter.register.registers
        )

    def _increment_pc(
        self,
        pc: tuple[int, int, int, int]
    ) -> tuple[int, int, int, int]:

        return self.program_counter.incrementer.increment(
            pc
        )

    def _advance_pc(
        self,
        pc: tuple[int, int, int, int],
        amount: int,
        clock: int
    ) -> None:

        next_pc = pc

        for _ in range(amount):
            next_pc = self._increment_pc(
                next_pc
            )

        self.program_counter.update(
            load_data=next_pc,
            load=1,
            increment=0,
            reset=0,
            clock=clock,
        )

    def cycle(
        self,
        clock: int
    ):

        if clock not in (0, 1):
            raise ValueError(
                "clock must be 0 or 1"
            )

        # ---------------------------------------------
        # FETCH
        # ---------------------------------------------

        pc = self._current_pc()

        decoded = self.fetch_decode.fetch_and_decode(
            pc
        )

        opcode = decoded["opcode"]

        # ---------------------------------------------
        # LOAD / STORE
        #
        # These instructions occupy two words:
        #
        #   Word 1 = opcode + register
        #   Word 2 = memory address
        # ---------------------------------------------

        if opcode in (
            Opcode.LOAD,
            Opcode.STORE,
        ):

            pc_value = self._bits_to_address(
                pc
            )

            second_word_address = (
                pc_value + 1
            ) % 16

            second_word_pc = self._address_to_bits(
                second_word_address
            )

            second_word = self.fetch_unit.fetch(
                second_word_pc
            )

            decoded["address"] = (
                self.decoder.decode_address(
                    second_word
                )
            )

        # ---------------------------------------------
        # DECODE
        # ---------------------------------------------

        instruction = self._dict_to_instruction(
            decoded
        )

        control_signals = self.control_unit.decode(
            instruction
        )

        result = None

        # ---------------------------------------------
        # ALU
        # ---------------------------------------------

        if (
            control_signals.register_write == 1
            and control_signals.memory_to_register == 0
        ):

            result = self.datapath.execute(
                instruction,
                clock
            )

        # ---------------------------------------------
        # STORE
        # ---------------------------------------------

        elif control_signals.memory_write == 1:

            source_address = _register_to_bits(
                instruction.source
            )

            _, source_data = (
                self.datapath.register_file.read(
                    read_address_a=source_address,
                    read_address_b=source_address,
                )
            )

            memory_address = self._address_to_bits(
                instruction.address
            )

            result = self.data_memory.update(
                address=memory_address,
                data=source_data,
                write_enable=1,
                clock=clock,
            )

        # ---------------------------------------------
        # LOAD
        # ---------------------------------------------

        elif (
            control_signals.memory_read == 1
            and control_signals.memory_to_register == 1
        ):

            memory_address = self._address_to_bits(
                instruction.address
            )

            memory_data = self.data_memory.update(
                address=memory_address,
                data=(0, 0, 0, 0),
                write_enable=0,
                clock=clock,
            )

            # IMPORTANT:
            # LOAD writes into destination, not source.
            destination_address = _register_to_bits(
                instruction.destination
            )

            self.datapath.register_file.update(
                write_address=destination_address,
                write_data=memory_data,
                write_enable=1,
                read_address_a=destination_address,
                read_address_b=destination_address,
                clock=clock,
            )

            result = memory_data

        # ---------------------------------------------
        # PROGRAM COUNTER
        # ---------------------------------------------

        if opcode in (
            Opcode.LOAD,
            Opcode.STORE,
        ):

            self._advance_pc(
                pc,
                2,
                clock
            )

        elif control_signals.pc_increment == 1:

            self._advance_pc(
                pc,
                1,
                clock
            )

        return decoded, result