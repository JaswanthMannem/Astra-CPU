from enum import Enum


def _to_bits(value: int, width: int) -> tuple[int, ...]:
    bits = []

    for _ in range(width):
        bits.append(value % 2)
        value = value // 2

    bits.reverse()

    return tuple(bits)


class Opcode(Enum):
    """
    4-bit operation codes for Astra ISA v1.

    Each opcode identifies the operation that the CPU must execute.
    """

    ADD = 0
    SUB = 1
    AND = 2
    OR = 3
    XOR = 4
    NOT = 5
    LOAD = 6
    STORE = 7
    JUMP = 8
    HALT = 9


class Register(Enum):
    """
    Registers available in the Astra ISA.

    Each register is identified by a 2-bit value.
    """

    R0 = 0
    R1 = 1
    R2 = 2
    R3 = 3


class Instruction:
    """
    Represents an instruction in the Astra ISA v1.

    Astra instructions use 8-bit words.

    Instruction formats:

    R-type:
        opcode | destination | source
        4 bits |    2 bits   | 2 bits

        Used by:
            ADD, SUB, AND, OR, XOR

    N-type:
        opcode | destination | 00
        4 bits |    2 bits   | 2 bits

        Used by:
            NOT

    M-type:
        Word 1:
            opcode | register | 00
            4 bits |  2 bits  | 2 bits

        Word 2:
            0000 | address
             4 bits | 4 bits

        Used by:
            LOAD, STORE

    J-type:
        opcode | address
        4 bits |  4 bits

        Used by:
            JUMP

    H-type:
        opcode | 0000
        4 bits | 4 bits

        Used by:
            HALT

    LOAD and STORE are two-word instructions.
    All other instructions are one-word instructions.
    """

    def __init__(
        self,
        opcode: Opcode,
        destination: Register | None = None,
        source: Register | None = None,
        address: int | None = None
    ) -> None:

        # Basic type validation
        if not isinstance(opcode, Opcode):
            raise TypeError("opcode must be an Opcode")

        if destination is not None and not isinstance(destination, Register):
            raise TypeError("destination must be a Register")

        if source is not None and not isinstance(source, Register):
            raise TypeError("source must be a Register")

        # Address validation
        if address is not None:
            if not isinstance(address, int):
                raise TypeError("address must be an integer")

            if address < 0 or address > 15:
                raise ValueError("address must be between 0 and 15")

        # Register-register instructions
        register_register_opcodes = (
            Opcode.ADD,
            Opcode.SUB,
            Opcode.AND,
            Opcode.OR,
            Opcode.XOR
        )

        if opcode in register_register_opcodes:

            if destination is None:
                raise ValueError(
                    "destination register is required for this instruction"
                )

            if source is None:
                raise ValueError(
                    "source register is required for this instruction"
                )

            if address is not None:
                raise ValueError(
                    "register-register instruction does not accept an address"
                )

        # NOT instruction
        elif opcode == Opcode.NOT:

            if destination is None:
                raise ValueError(
                    "destination register is required for NOT"
                )

            if source is not None:
                raise ValueError(
                    "NOT instruction does not accept a source register"
                )

            if address is not None:
                raise ValueError(
                    "NOT instruction does not accept an address"
                )

        # LOAD instruction
        elif opcode == Opcode.LOAD:

            if destination is None:
                raise ValueError(
                    "destination register is required for LOAD"
                )

            if source is not None:
                raise ValueError(
                    "LOAD instruction does not accept a source register"
                )

            if address is None:
                raise ValueError(
                    "address is required for LOAD"
                )

        # STORE instruction
        elif opcode == Opcode.STORE:

            if destination is not None:
                raise ValueError(
                    "STORE instruction does not accept a destination register"
                )

            if source is None:
                raise ValueError(
                    "source register is required for STORE"
                )

            if address is None:
                raise ValueError(
                    "address is required for STORE"
                )

        # JUMP instruction
        elif opcode == Opcode.JUMP:

            if destination is not None:
                raise ValueError(
                    "JUMP instruction does not accept a destination register"
                )

            if source is not None:
                raise ValueError(
                    "JUMP instruction does not accept a source register"
                )

            if address is None:
                raise ValueError(
                    "address is required for JUMP"
                )

        # HALT instruction
        elif opcode == Opcode.HALT:

            if destination is not None:
                raise ValueError(
                    "HALT instruction does not accept a destination register"
                )

            if source is not None:
                raise ValueError(
                    "HALT instruction does not accept a source register"
                )

            if address is not None:
                raise ValueError(
                    "HALT instruction does not accept an address"
                )

        self.opcode = opcode
        self.destination = destination
        self.source = source
        self.address = address

    def encode(self) -> tuple[tuple[int, ...], ...]:
        """
        Encode the instruction into one or more 8-bit words.

        Returns:
            A tuple containing one or two 8-bit words.

        R-type:
            opcode | destination | source

        NOT:
            opcode | destination | 00

        LOAD:
            word 1 = opcode | destination | 00
            word 2 = 0000 | address

        STORE:
            word 1 = opcode | source | 00
            word 2 = 0000 | address

        JUMP:
            opcode | address

        HALT:
            opcode | 0000
        """

        opcode_bits = _to_bits(self.opcode.value, 4)

        register_register_opcodes = (
            Opcode.ADD,
            Opcode.SUB,
            Opcode.AND,
            Opcode.OR,
            Opcode.XOR
        )

        # R-type
        if self.opcode in register_register_opcodes:

            destination_bits = _to_bits(
                self.destination.value,
                2
            )

            source_bits = _to_bits(
                self.source.value,
                2
            )

            word = (
                opcode_bits
                + destination_bits
                + source_bits
            )

            return (word,)

        # N-type
        elif self.opcode == Opcode.NOT:

            destination_bits = _to_bits(
                self.destination.value,
                2
            )

            word = (
                opcode_bits
                + destination_bits
                + (0, 0)
            )

            return (word,)

        # M-type: LOAD
        elif self.opcode == Opcode.LOAD:

            destination_bits = _to_bits(
                self.destination.value,
                2
            )

            address_bits = _to_bits(
                self.address,
                4
            )

            word1 = (
                opcode_bits
                + destination_bits
                + (0, 0)
            )

            word2 = (
                (0, 0, 0, 0)
                + address_bits
            )

            return (word1, word2)

        # M-type: STORE
        elif self.opcode == Opcode.STORE:

            source_bits = _to_bits(
                self.source.value,
                2
            )

            address_bits = _to_bits(
                self.address,
                4
            )

            word1 = (
                opcode_bits
                + source_bits
                + (0, 0)
            )

            word2 = (
                (0, 0, 0, 0)
                + address_bits
            )

            return (word1, word2)

        # J-type
        elif self.opcode == Opcode.JUMP:

            address_bits = _to_bits(
                self.address,
                4
            )

            word = (
                opcode_bits
                + address_bits
            )

            return (word,)

        # H-type
        elif self.opcode == Opcode.HALT:

            word = (
                opcode_bits
                + (0, 0, 0, 0)
            )

            return (word,)