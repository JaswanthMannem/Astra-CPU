# Astra Assembler

## Overview

Astra includes a two-pass assembler that converts assembly source into `Instruction` objects.

```text
Assembly Source
      |
    Pass 1
      |
 Symbol Table
      |
    Pass 2
      |
Instruction Objects
      |
 Program Loader
      |
Instruction Memory
```

## Pass 1

Pass 1:

- Finds labels
- Calculates instruction-memory addresses
- Accounts for instruction size

## Pass 2

Pass 2:

- Parses instructions
- Converts register names
- Resolves numeric addresses
- Resolves labels
- Creates `Instruction` objects

## Supported Instructions

```text
ADD
SUB
AND
OR
XOR
NOT
LOAD
STORE
JUMP
HALT
```

Instruction and register names are case-insensitive.

## Comments

`#` starts a comment:

```asm
ADD R1, R2    # Add R2 into R1
HALT          # Stop
```

## Labels

Labels end with `:`:

```asm
start:
    ADD R0, R1
    JUMP start
```

Labels can also share a line with an instruction:

```asm
start: ADD R0, R1
```

Valid labels begin with a letter or `_` and may contain letters, digits, and `_`.

## Forward References

```asm
    JUMP finish

    ADD R0, R1

finish:
    HALT
```

Pass 1 discovers `finish`; pass 2 resolves it.

## Addresses

Astra uses 4-bit addresses:

```text
0 through 15
```

Addresses outside this range are rejected.

## Instruction Size

Most instructions occupy one 8-bit word.

`LOAD` and `STORE` occupy two words.

Example:

```asm
LOAD R0, 5
HALT
```

Memory layout:

```text
address 0: LOAD first word
address 1: LOAD address word
address 2: HALT
```

## Program Loading

```python
from astra.isa.assembler import Assembler
from astra.cpu.instruction_memory import InstructionMemory
from astra.cpu.program_loader import ProgramLoader

source = """
LOAD R0, 3
HALT
"""

assembler = Assembler()
program = assembler.assemble(source)

memory = InstructionMemory()

loader = ProgramLoader(memory)
loader.load(program)
```

## Error Handling

The assembler validates:

- Source type
- Unknown instructions
- Invalid registers
- Invalid addresses
- Operand counts
- Duplicate labels
- Undefined labels
- Invalid label names
- Program size

Errors include the source line number where applicable.
