from dataclasses import dataclass

from astra.cpu.alu_control import ALUControl, ALUOperation
from astra.isa.instructions import Instruction, Opcode


@dataclass(frozen=True)
class ControlSignals:
    alu_operation: ALUOperation | None
    register_write: int
    memory_read: int
    memory_write: int
    memory_to_register: int
    pc_load: int
    pc_increment: int
    halt: int


class ControlUnit:

    def __init__(self) -> None:
        self.alu_control = ALUControl()

        self.controls = {
            Opcode.ADD: ControlSignals(
                self.alu_control.operation(Opcode.ADD),
                1, 0, 0, 0, 0, 1, 0
            ),

            Opcode.SUB: ControlSignals(
                self.alu_control.operation(Opcode.SUB),
                1, 0, 0, 0, 0, 1, 0
            ),

            Opcode.AND: ControlSignals(
                self.alu_control.operation(Opcode.AND),
                1, 0, 0, 0, 0, 1, 0
            ),

            Opcode.OR: ControlSignals(
                self.alu_control.operation(Opcode.OR),
                1, 0, 0, 0, 0, 1, 0
            ),

            Opcode.XOR: ControlSignals(
                self.alu_control.operation(Opcode.XOR),
                1, 0, 0, 0, 0, 1, 0
            ),

            Opcode.NOT: ControlSignals(
                self.alu_control.operation(Opcode.NOT),
                1, 0, 0, 0, 0, 1, 0
            ),

            Opcode.LOAD: ControlSignals(
                None,
                1, 1, 0, 1, 0, 1, 0
            ),

            Opcode.STORE: ControlSignals(
                None,
                0, 0, 1, 0, 0, 1, 0
            ),

            Opcode.JUMP: ControlSignals(
                None,
                0, 0, 0, 0, 1, 0, 0
            ),

            Opcode.HALT: ControlSignals(
                None,
                0, 0, 0, 0, 0, 0, 1
            ),
        }

    def decode(
        self,
        instruction: Instruction
    ) -> ControlSignals:

        if not isinstance(instruction, Instruction):
            raise TypeError(
                "instruction must be an Instruction"
            )

        return self.controls[instruction.opcode]