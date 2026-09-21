from astra.cpu.fetch_unit import FetchUnit
from astra.isa.decoder import InstructionDecoder
from astra.isa.instructions import Instruction


class FetchDecode:
    """
    Combines instruction fetching and instruction decoding.

    Flow:

        Program Counter
              ↓
        Instruction Memory
              ↓
          8-bit word
              ↓
        Instruction Decoder
              ↓
          Instruction
    """

    def __init__(
        self,
        fetch_unit: FetchUnit,
        decoder: InstructionDecoder,
    ) -> None:
        """
        Initialize the Fetch + Decode unit.
        """

        if not isinstance(fetch_unit, FetchUnit):
            raise TypeError(
                "fetch_unit must be a FetchUnit"
            )

        if not isinstance(decoder, InstructionDecoder):
            raise TypeError(
                "decoder must be an InstructionDecoder"
            )

        self.fetch_unit = fetch_unit
        self.decoder = decoder

    def fetch_and_decode(
        self,
        program_counter: tuple[int, int, int, int],
    ) -> Instruction:
        """
        Fetch and decode the instruction at the current PC.
        """

        instruction_word = self.fetch_unit.fetch(
            program_counter
        )

        return self.decoder.decode(
            instruction_word
        )