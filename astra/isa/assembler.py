from astra.isa.instructions import Instruction, Opcode, Register


class Assembler:
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
        if not isinstance(source, str):
            raise TypeError("source must be a string")

        instructions = []

        for line_number, line in enumerate(source.splitlines(), start=1):
            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            instruction = self._assemble_line(line, line_number)
            instructions.append(instruction)

        return instructions

    def _assemble_line(self, line: str, line_number: int) -> Instruction:
        parts = line.replace(",", " ").split()

        if not parts:
            raise ValueError(
                f"line {line_number}: empty instruction"
            )

        mnemonic = parts[0].upper()

        if mnemonic not in self.OPCODE_MAP:
            raise ValueError(
                f"line {line_number}: unknown instruction '{parts[0]}'"
            )

        opcode = self.OPCODE_MAP[mnemonic]

        if opcode == Opcode.HALT:
            self._expect_operand_count(parts, 1, line_number)
            return Instruction(opcode=opcode)

        if opcode == Opcode.JUMP:
            self._expect_operand_count(parts, 2, line_number)

            address = self._parse_address(
                parts[1],
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

            address = self._parse_address(
                parts[2],
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

            address = self._parse_address(
                parts[2],
                line_number,
            )

            return Instruction(
                opcode=opcode,
                source=source,
                address=address,
            )

        # Remaining instructions are R-type:
        # ADD, SUB, AND, OR, XOR

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

    @staticmethod
    def _expect_operand_count(
        parts: list[str],
        expected: int,
        line_number: int,
    ) -> None:
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
        token = token.upper()

        if token not in self.REGISTER_MAP:
            raise ValueError(
                f"line {line_number}: invalid register '{token}'"
            )

        return self.REGISTER_MAP[token]

    @staticmethod
    def _parse_address(
        token: str,
        line_number: int,
    ) -> int:
        try:
            address = int(token)
        except ValueError:
            raise ValueError(
                f"line {line_number}: invalid address '{token}'"
            )

        if not 0 <= address <= 15:
            raise ValueError(
                f"line {line_number}: address must be between 0 and 15"
            )

        return address