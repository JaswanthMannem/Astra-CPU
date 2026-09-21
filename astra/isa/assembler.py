from astra.isa.instructions import Instruction, Opcode, Register


class Assembler:
    """Assemble Astra assembly source into Instruction objects.

    The assembler uses two passes.

    Pass 1:
        Discover labels and calculate their instruction-memory
        addresses.

    Pass 2:
        Parse instructions and resolve label references.

    Astra instruction sizes are measured in 8-bit instruction
    memory words. Most instructions occupy one word, while
    LOAD and STORE occupy two words.
    """

    REGISTER_MAP = {
        "R0": Register.R0,
        "R1": Register.R1,
        "R2": Register.R2,
        "R3": Register.R3,
    }

    OPCODE_MAP = {
        "ADD": Opcode.ADD,
        "SUB": Opcode.SUB,
        "AND": Opcode.AND,
        "OR": Opcode.OR,
        "XOR": Opcode.XOR,
        "NOT": Opcode.NOT,
        "LOAD": Opcode.LOAD,
        "STORE": Opcode.STORE,
        "JUMP": Opcode.JUMP,
        "HALT": Opcode.HALT,
    }

    def assemble(self, source: str) -> list[Instruction]:
        """Assemble Astra assembly source.

        Args:
            source: Assembly source code.

        Returns:
            List of assembled Instruction objects.

        Raises:
            TypeError: If source is not a string.
            ValueError: If the source contains invalid syntax,
                duplicate labels, undefined labels, or an invalid
                instruction.
        """
        if not isinstance(source, str):
            raise TypeError("source must be a string")

        lines = source.splitlines()

        symbols = self._first_pass(lines)

        instructions = []

        for line_number, line in enumerate(lines, start=1):
            line = self._strip_comment(line).strip()

            if not line:
                continue

            line = self._remove_label(line)

            if not line:
                continue

            instruction = self._assemble_line(
                line,
                line_number,
                symbols,
            )

            instructions.append(instruction)

        return instructions

    def _first_pass(self, lines: list[str]) -> dict[str, int]:
        """Build the symbol table from assembly labels.

        Args:
            lines: Assembly source lines.

        Returns:
            Mapping from label names to instruction-memory addresses.
        """
        symbols = {}
        address = 0

        for line_number, line in enumerate(lines, start=1):
            line = self._strip_comment(line).strip()

            if not line:
                continue

            if ":" in line:
                label, remainder = line.split(":", 1)

                label = label.strip()

                self._validate_label(label, line_number)

                if label in symbols:
                    raise ValueError(
                        f"line {line_number}: "
                        f"duplicate label '{label}'"
                    )

                symbols[label] = address

                line = remainder.strip()

                if not line:
                    continue

            parts = line.replace(",", " ").split()

            mnemonic = parts[0].upper()

            if mnemonic not in self.OPCODE_MAP:
                raise ValueError(
                    f"line {line_number}: "
                    f"unknown instruction '{parts[0]}'"
                )

            opcode = self.OPCODE_MAP[mnemonic]

            address += self._instruction_size(opcode)

        return symbols

    def _assemble_line(
        self,
        line: str,
        line_number: int,
        symbols: dict[str, int],
    ) -> Instruction:
        """Assemble one instruction line.

        Args:
            line: Instruction source without comments or labels.
            line_number: Original source line number.
            symbols: Symbol table created during pass 1.

        Returns:
            Assembled Instruction object.
        """
        parts = line.replace(",", " ").split()

        if not parts:
            raise ValueError(
                f"line {line_number}: empty instruction"
            )

        mnemonic = parts[0].upper()

        if mnemonic not in self.OPCODE_MAP:
            raise ValueError(
                f"line {line_number}: "
                f"unknown instruction '{parts[0]}'"
            )

        opcode = self.OPCODE_MAP[mnemonic]

        if opcode == Opcode.HALT:
            self._expect_operand_count(parts, 1, line_number)

            return Instruction(opcode=opcode)

        if opcode == Opcode.JUMP:
            self._expect_operand_count(parts, 2, line_number)

            address = self._parse_address_or_label(
                parts[1],
                symbols,
                line_number,
            )

            return Instruction(
                opcode=opcode,
                address=address,
            )

        if opcode == Opcode.NOT:
            self._expect_operand_count(parts, 2, line_number)

            destination = self._parse_register(
                parts[1],
                line_number,
            )

            return Instruction(
                opcode=opcode,
                destination=destination,
            )

        if opcode == Opcode.LOAD:
            self._expect_operand_count(parts, 3, line_number)

            destination = self._parse_register(
                parts[1],
                line_number,
            )

            address = self._parse_address_or_label(
                parts[2],
                symbols,
                line_number,
            )

            return Instruction(
                opcode=opcode,
                destination=destination,
                address=address,
            )

        if opcode == Opcode.STORE:
            self._expect_operand_count(parts, 3, line_number)

            source = self._parse_register(
                parts[1],
                line_number,
            )

            address = self._parse_address_or_label(
                parts[2],
                symbols,
                line_number,
            )

            return Instruction(
                opcode=opcode,
                source=source,
                address=address,
            )

        self._expect_operand_count(parts, 3, line_number)

        destination = self._parse_register(
            parts[1],
            line_number,
        )

        source = self._parse_register(
            parts[2],
            line_number,
        )

        return Instruction(
            opcode=opcode,
            destination=destination,
            source=source,
        )

    def _parse_address_or_label(
        self,
        token: str,
        symbols: dict[str, int],
        line_number: int,
    ) -> int:
        """Resolve a numeric address or symbolic label.

        Args:
            token: Numeric address or label name.
            symbols: Symbol table.
            line_number: Source line number.

        Returns:
            Resolved four-bit address.
        """
        try:
            address = int(token)
        except ValueError:
            if token not in symbols:
                raise ValueError(
                    f"line {line_number}: "
                    f"undefined label '{token}'"
                )

            address = symbols[token]

        if not 0 <= address <= 15:
            raise ValueError(
                f"line {line_number}: "
                "address must be between 0 and 15"
            )

        return address

    @staticmethod
    def _instruction_size(opcode: Opcode) -> int:
        """Return the number of instruction-memory words required.

        Args:
            opcode: Instruction opcode.

        Returns:
            One for single-word instructions and two for LOAD/STORE.
        """
        if opcode in (Opcode.LOAD, Opcode.STORE):
            return 2

        return 1

    @staticmethod
    def _strip_comment(line: str) -> str:
        """Remove an assembly comment from a source line."""
        return line.split("#", 1)[0]

    @staticmethod
    def _remove_label(line: str) -> str:
        """Remove a label definition from a source line."""
        if ":" not in line:
            return line

        _, remainder = line.split(":", 1)

        return remainder.strip()

    @staticmethod
    def _validate_label(
        label: str,
        line_number: int,
    ) -> None:
        """Validate an assembly label name."""
        if not label:
            raise ValueError(
                f"line {line_number}: empty label"
            )

        if not label[0].isalpha() and label[0] != "_":
            raise ValueError(
                f"line {line_number}: "
                f"invalid label '{label}'"
            )

        if not all(
            character.isalnum() or character == "_"
            for character in label
        ):
            raise ValueError(
                f"line {line_number}: "
                f"invalid label '{label}'"
            )

    @staticmethod
    def _expect_operand_count(
        parts: list[str],
        expected: int,
        line_number: int,
    ) -> None:
        """Validate the number of tokens in an instruction."""
        if len(parts) != expected:
            raise ValueError(
                f"line {line_number}: expected "
                f"{expected - 1} operand(s), "
                f"got {len(parts) - 1}"
            )

    def _parse_register(
        self,
        token: str,
        line_number: int,
    ) -> Register:
        """Convert a register token into a Register enum."""
        token = token.upper()

        if token not in self.REGISTER_MAP:
            raise ValueError(
                f"line {line_number}: "
                f"invalid register '{token}'"
            )

        return self.REGISTER_MAP[token]