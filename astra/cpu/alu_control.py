from enum import Enum

from astra.isa.instructions import Opcode


class ALUOperation(Enum):
    """
    Represents the 3-bit control signal used by the ALU.

    The control signal determines which operation the ALU performs.

    Select signal:
        000: Bitwise AND
        001: Bitwise OR
        010: Bitwise XOR
        011: Bitwise NOT A
        100: Addition
        101: Subtraction
    """

    AND = (0, 0, 0)
    OR = (0, 0, 1)
    XOR = (0, 1, 0)
    NOT = (0, 1, 1)
    ADD = (1, 0, 0)
    SUB = (1, 0, 1)


class ALUControl:
    """
    Converts an ISA opcode into the corresponding ALU operation.

    The ALUControl block acts as a translation layer between
    the ISA instruction and the ALU control signal.

    ISA opcode        ALU operation
    --------------------------------
    ADD               ADD
    SUB               SUB
    AND               AND
    OR                OR
    XOR               XOR
    NOT               NOT

    Instructions such as LOAD, STORE, JUMP, and HALT do not
    represent ALU operations and are rejected.
    """

    def __init__(self) -> None:
        """
        Initialize the opcode-to-ALU-operation mapping.
        """

        self.operations = {
            Opcode.ADD: ALUOperation.ADD,
            Opcode.SUB: ALUOperation.SUB,
            Opcode.AND: ALUOperation.AND,
            Opcode.OR: ALUOperation.OR,
            Opcode.XOR: ALUOperation.XOR,
            Opcode.NOT: ALUOperation.NOT,
        }

    def operation(self, opcode: Opcode) -> ALUOperation:
        """
        Convert an ISA opcode into the corresponding ALU operation.

        Args:
            opcode: An Opcode from the Astra instruction set.

        Returns:
            The corresponding ALUOperation.

        Raises:
            TypeError:
                If opcode is not an Opcode.

            ValueError:
                If the opcode does not represent an ALU operation.
        """

        if not isinstance(opcode, Opcode):
            raise TypeError("opcode must be an Opcode")

        try:
            return self.operations[opcode]
        except KeyError:
            raise ValueError(
                f"opcode {opcode.name} does not represent an ALU operation"
            )