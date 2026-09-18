from astra.cpu.alu_control import ALUControl
from astra.isa.instructions import Instruction, Opcode, Register
from astra.logic.alu import alu
from astra.logic.sequential import RegisterFile


def _register_to_bits(
    register: Register
) -> tuple[int, int]:
    """
    Convert a Register enum into its 2-bit register address.

    Register encoding:

        R0 -> 00
        R1 -> 01
        R2 -> 10
        R3 -> 11

    Args:
        register: A Register enum value.

    Returns:
        A 2-bit tuple representing the register address.

    Raises:
        TypeError:
            If register is not a Register.
    """

    if not isinstance(register, Register):
        raise TypeError("register must be a Register")

    value = register.value

    return (
        value // 2,
        value % 2
    )


class Datapath:
    """
    CPU datapath for Astra's ALU instructions.

    The datapath connects:

        Instruction
             |
             v
        ALU Control
             |
             v
        Register File
          /       \
         v         v
      Operand A  Operand B
          \\       /
           v     v
             ALU
              |
              v
           Result
              |
              v
        Register File
           writeback

    Currently supported instructions:

        ADD
        SUB
        AND
        OR
        XOR
        NOT
    """

    def __init__(self) -> None:
        """
        Initialize the CPU datapath.
        """

        self.register_file = RegisterFile()
        self.alu_control = ALUControl()

    def execute(
        self,
        instruction: Instruction,
        clock: int
    ) -> tuple[int, int, int, int]:
        """
        Execute one ALU instruction.

        The operands are read combinationally from the Register File,
        processed by the ALU, and the result is written to the
        destination register.

        Args:
            instruction:
                Astra ISA instruction.

            clock:
                Clock signal used for register writeback.

        Returns:
            The 4-bit ALU result.

        Raises:
            TypeError:
                If instruction is not an Instruction.

            ValueError:
                If the instruction is not an ALU instruction.
        """

        if not isinstance(instruction, Instruction):
            raise TypeError(
                "instruction must be an Instruction"
            )

        operation = self.alu_control.operation(
            instruction.opcode
        )

        destination_address = _register_to_bits(
            instruction.destination
        )

        if instruction.opcode == Opcode.NOT:
            source_address = destination_address
        else:
            source_address = _register_to_bits(
                instruction.source
            )

        operand_a, operand_b = self.register_file.read(
            read_address_a=destination_address,
            read_address_b=source_address
        )

        result, _, _, _, _ = alu(
            operand_a,
            operand_b,
            operation.value
        )

        self.register_file.update(
            write_address=destination_address,
            write_data=result,
            write_enable=1,
            read_address_a=destination_address,
            read_address_b=source_address,
            clock=clock
        )

        return result