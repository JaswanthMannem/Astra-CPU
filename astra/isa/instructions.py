from enum import Enum


class Register(Enum):
    """Registers available in the Astra ISA."""

    R0 = 0
    R1 = 1
    R2 = 2
    R3 = 3


class Opcode(Enum):
    """Operation codes supported by the Astra ISA."""

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


class Instruction:
    """Represent a single Astra machine instruction.

    Astra uses 8-bit instruction words and supports several
    instruction formats:

    R-type:
        opcode(4) | destination(2) | source(2)

    NOT:
        opcode(4) | destination(2) | 00

    LOAD / STORE:
        These instructions require two 8-bit words because
        the opcode, register, and 4-bit memory address require
        10 bits in total.

        First word:
            opcode(4) | register(2) | 00

        Second word:
            0000 | address(4)

    JUMP:
        opcode(4) | address(4)

    HALT:
        opcode(4) | 0000
    """

    def __init__(
        self,
        opcode: Opcode,
        destination: Register | None = None,
        source: Register | None = None,
        address: int | None = None,
    ) -> None:
        """Create an Astra instruction.

        Args:
            opcode: Operation performed by the instruction.
            destination: Destination register for register-based
                and LOAD instructions.
            source: Source register for register-based and STORE
                instructions.
            address: Four-bit memory address for LOAD, STORE, and
                JUMP instructions.

        Raises:
            TypeError: If an argument has an invalid type.
            ValueError: If the instruction format is invalid.
        """
        if not isinstance(opcode, Opcode):
            raise TypeError("opcode must be an Opcode")

        if destination is not None and not isinstance(destination, Register):
            raise TypeError("destination must be a Register")

        if source is not None and not isinstance(source, Register):
            raise TypeError("source must be a Register")

        if address is not None:
            if not isinstance(address, int):
                raise TypeError("address must be an integer")

            if not 0 <= address <= 15:
                raise ValueError("address must be between 0 and 15")

        self.opcode = opcode
        self.destination = destination
        self.source = source
        self.address = address

        self._validate_format()

    def _validate_format(self) -> None:
        """Validate operands according to the instruction format.

        Raises:
            ValueError: If operands do not match the opcode's
                required format.
        """
        if self.opcode in (
            Opcode.ADD,
            Opcode.SUB,
            Opcode.AND,
            Opcode.OR,
            Opcode.XOR,
        ):
            if self.destination is None:
                raise ValueError(
                    f"{self.opcode.name} requires a destination register"
                )

            if self.source is None:
                raise ValueError(
                    f"{self.opcode.name} requires a source register"
                )

            if self.address is not None:
                raise ValueError(
                    f"{self.opcode.name} does not accept an address"
                )

        elif self.opcode == Opcode.NOT:
            if self.destination is None:
                raise ValueError("NOT requires a destination register")

            if self.source is not None:
                raise ValueError("NOT does not accept a source register")

            if self.address is not None:
                raise ValueError("NOT does not accept an address")

        elif self.opcode == Opcode.LOAD:
            if self.destination is None:
                raise ValueError(
                    "LOAD requires a destination register"
                )

            if self.address is None:
                raise ValueError("LOAD requires an address")

            if self.source is not None:
                raise ValueError("LOAD does not accept a source register")

        elif self.opcode == Opcode.STORE:
            if self.source is None:
                raise ValueError("STORE requires a source register")

            if self.address is None:
                raise ValueError("STORE requires an address")

            if self.destination is not None:
                raise ValueError(
                    "STORE does not accept a destination register"
                )

        elif self.opcode == Opcode.JUMP:
            if self.address is None:
                raise ValueError("JUMP requires an address")

            if self.destination is not None:
                raise ValueError(
                    "JUMP does not accept a destination register"
                )

            if self.source is not None:
                raise ValueError(
                    "JUMP does not accept a source register"
                )

        elif self.opcode == Opcode.HALT:
            if self.destination is not None:
                raise ValueError(
                    "HALT does not accept a destination register"
                )

            if self.source is not None:
                raise ValueError(
                    "HALT does not accept a source register"
                )

            if self.address is not None:
                raise ValueError("HALT does not accept an address")

    def __eq__(self, other: object) -> bool:
        """Compare two instructions by their encoded meaning.

        Two Instruction objects are equal when their opcode,
        destination register, source register, and address are
        identical.

        Args:
            other: Object to compare with this instruction.

        Returns:
            True when both instructions represent the same
            instruction; otherwise False.
        """
        if not isinstance(other, Instruction):
            return NotImplemented

        return (
            self.opcode == other.opcode
            and self.destination == other.destination
            and self.source == other.source
            and self.address == other.address
        )

    def __repr__(self) -> str:
        """Return a useful debugging representation."""
        return (
            "Instruction("
            f"opcode={self.opcode!r}, "
            f"destination={self.destination!r}, "
            f"source={self.source!r}, "
            f"address={self.address!r}"
            ")"
        )

    @staticmethod
    def _register_to_bits(register: Register) -> tuple[int, int]:
        """Convert a register into its two-bit encoding.

        Args:
            register: Register to encode.

        Returns:
            Two-bit tuple representing the register.
        """
        value = register.value

        return (
            value // 2,
            value % 2,
        )

    @staticmethod
    def _address_to_bits(address: int) -> tuple[int, int, int, int]:
        """Convert a four-bit address into a bit tuple.

        Args:
            address: Integer address from 0 through 15.

        Returns:
            Four-bit tuple representing the address.
        """
        return (
            (address // 8) % 2,
            (address // 4) % 2,
            (address // 2) % 2,
            address % 2,
        )

    def encode(self) -> tuple[tuple[int, ...], ...]:
        """Encode the instruction into one or two 8-bit words.

        Returns:
            A tuple containing one or two 8-bit instruction words.

        Raises:
            ValueError: If the instruction cannot be encoded.
        """
        opcode_bits = (
            (self.opcode.value // 8) % 2,
            (self.opcode.value // 4) % 2,
            (self.opcode.value // 2) % 2,
            self.opcode.value % 2,
        )

        if self.opcode in (
            Opcode.ADD,
            Opcode.SUB,
            Opcode.AND,
            Opcode.OR,
            Opcode.XOR,
        ):
            destination_bits = self._register_to_bits(
                self.destination
            )
            source_bits = self._register_to_bits(
                self.source
            )

            return (
                opcode_bits
                + destination_bits
                + source_bits,
            )

        if self.opcode == Opcode.NOT:
            destination_bits = self._register_to_bits(
                self.destination
            )

            return (
                opcode_bits
                + destination_bits
                + (0, 0),
            )

        if self.opcode == Opcode.JUMP:
            address_bits = self._address_to_bits(self.address)

            return (
                opcode_bits
                + address_bits,
            )

        if self.opcode == Opcode.HALT:
            return (
                opcode_bits
                + (0, 0, 0, 0),
            )

        if self.opcode in (Opcode.LOAD, Opcode.STORE):
            register = (
                self.destination
                if self.opcode == Opcode.LOAD
                else self.source
            )

            register_bits = self._register_to_bits(register)
            address_bits = self._address_to_bits(self.address)

            first_word = (
                opcode_bits
                + register_bits
                + (0, 0)
            )

            second_word = (
                (0, 0, 0, 0)
                + address_bits
            )

            return (
                first_word,
                second_word,
            )

        raise ValueError(
            f"unsupported opcode: {self.opcode.name}"
        )