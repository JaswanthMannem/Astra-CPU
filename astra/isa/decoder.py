from astra.isa.instructions import Opcode, Register


def _bits_to_int(bits: tuple[int, ...]) -> int:
    """
    Convert a tuple of binary bits into an integer.

    Example:
        (1, 0, 1, 0) -> 10
    """

    value = 0

    for bit in bits:
        value = value * 2 + bit

    return value


class InstructionDecoder:
    """
    Decodes Astra ISA machine-code words.

    Astra instructions are encoded using 8-bit words.

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
        4 bits | 4 bits

        Used by:
            JUMP

    H-type:
        opcode | 0000
        4 bits | 4 bits

        Used by:
            HALT
    """

    def decode(
        self,
        word: tuple[int, int, int, int, int, int, int, int]
    ) -> dict:

        # ----------------------------------------------------
        # Validate input
        # ----------------------------------------------------

        if not isinstance(word, tuple):
            raise TypeError("word must be a tuple")

        if len(word) != 8:
            raise ValueError("word must contain exactly 8 bits")

        for bit in word:
            if bit not in (0, 1):
                raise ValueError("word must contain only 0 or 1")

        # ----------------------------------------------------
        # Decode opcode
        # ----------------------------------------------------

        opcode_value = _bits_to_int(word[:4])

        try:
            opcode = Opcode(opcode_value)
        except ValueError:
            raise ValueError(
                f"invalid opcode: {opcode_value}"
            )

        # ----------------------------------------------------
        # R-type instructions
        # ----------------------------------------------------

        register_register_opcodes = (
            Opcode.ADD,
            Opcode.SUB,
            Opcode.AND,
            Opcode.OR,
            Opcode.XOR
        )

        if opcode in register_register_opcodes:

            destination_value = _bits_to_int(word[4:6])
            source_value = _bits_to_int(word[6:8])

            destination = Register(destination_value)
            source = Register(source_value)

            return {
                "opcode": opcode,
                "destination": destination,
                "source": source,
                "address": None
            }

        # ----------------------------------------------------
        # NOT
        # ----------------------------------------------------

        elif opcode == Opcode.NOT:

            destination_value = _bits_to_int(word[4:6])

            destination = Register(destination_value)

            return {
                "opcode": opcode,
                "destination": destination,
                "source": None,
                "address": None
            }

        # ----------------------------------------------------
        # LOAD
        # ----------------------------------------------------

        elif opcode == Opcode.LOAD:

            destination_value = _bits_to_int(word[4:6])

            destination = Register(destination_value)

            return {
                "opcode": opcode,
                "destination": destination,
                "source": None,
                "address": None
            }

        # ----------------------------------------------------
        # STORE
        # ----------------------------------------------------

        elif opcode == Opcode.STORE:

            source_value = _bits_to_int(word[4:6])

            source = Register(source_value)

            return {
                "opcode": opcode,
                "destination": None,
                "source": source,
                "address": None
            }

        # ----------------------------------------------------
        # JUMP
        # ----------------------------------------------------

        elif opcode == Opcode.JUMP:

            address = _bits_to_int(word[4:8])

            return {
                "opcode": opcode,
                "destination": None,
                "source": None,
                "address": address
            }

        # ----------------------------------------------------
        # HALT
        # ----------------------------------------------------

        elif opcode == Opcode.HALT:

            return {
                "opcode": opcode,
                "destination": None,
                "source": None,
                "address": None
            }

    def decode_address(
            self,
            word: tuple[int, int, int, int, int, int, int, int]
        ) -> int:
            """
            Decode the address operand from an 8-bit operand word.

            The address word uses the format:

                0000 | address
                4 bits | 4 bits

            Example:

                00001010 -> 10
            """

            if not isinstance(word, tuple):
                raise TypeError("word must be a tuple")

            if len(word) != 8:
                raise ValueError("word must contain exactly 8 bits")

            for bit in word:
                if bit not in (0, 1):
                    raise ValueError("word must contain only 0 or 1")

            return _bits_to_int(word[4:8])