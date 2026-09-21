# Getting Started with Astra

## Overview

Astra is a from-scratch 4-bit CPU implementation written in Python.

Recommended workflow:

```text
Implement
   ->
Test
   ->
Fix
   ->
Run full test suite
   ->
Commit
   ->
Next component
```

## Project Structure

```text
Astra/
├── astra/
│   ├── logic/
│   ├── isa/
│   └── cpu/
└── tests/
```

## Setup

If using `uv`:

```bash
uv sync
```

## Run Tests

```bash
uv run pytest
```

or:

```bash
pytest
```

## Run Individual Tests

```bash
uv run pytest tests/test_gates.py
uv run pytest tests/test_alu.py
uv run pytest tests/test_assembler.py
uv run pytest tests/test_program_execution.py
```

## Basic CPU Workflow

```text
Assembly
   |
Assembler
   |
Instruction Objects
   |
ProgramLoader
   |
InstructionMemory
   |
CPU
```

Example:

```python
from astra.isa.assembler import Assembler
from astra.cpu.instruction_memory import InstructionMemory
from astra.cpu.program_loader import ProgramLoader
from astra.cpu.cpu import CPU

source = """
ADD R0, R1
HALT
"""

assembler = Assembler()
program = assembler.assemble(source)

instruction_memory = InstructionMemory()

loader = ProgramLoader(instruction_memory)
loader.load(program)

cpu = CPU(instruction_memory)
cpu.reset()
cpu.run()
```

## Data Memory

Programs using LOAD or STORE need data-memory values initialized before execution.

Data memory and instruction memory are separate.

## Reset

```python
cpu.reset()
```

Reset clears:

- Program counter
- Registers
- Data memory
- Halt state

The loaded instruction program is preserved.

## Step Execution

```python
cpu.step()
```

This executes one complete CPU instruction and is useful for debugging.

## Assembly Example

```asm
ADD R0, R1
SUB R2, R0
AND R1, R2
OR R3, R1
XOR R0, R3
NOT R0
HALT
```

## Label Example

```asm
start:
    ADD R0, R1
    JUMP finish

finish:
    HALT
```

## Development Philosophy

Astra intentionally models hardware concepts explicitly:

```text
Gates
  ->
Mux / Decoder / Adder
  ->
ALU / Registers / Memory
  ->
Datapath / Control
  ->
CPU
```

## V1 Feature Set

- 4-bit datapath
- 4 general-purpose registers
- 16x4 data memory
- 16x8 instruction memory
- ADD
- SUB
- AND
- OR
- XOR
- NOT
- LOAD
- STORE
- JUMP
- HALT
- CPU reset
- Two-pass assembler
- Labels
- End-to-end execution

## V1 Boundary

V1 intentionally does not include:

- Conditional branches
- Stack
- CALL/RET
- Interrupts
- Pipeline
- Cache
- Larger datapath widths
- I/O peripherals

## Final Verification

Before considering a V1 change complete:

```bash
uv run pytest
```

Then inspect:

```bash
git status
git diff --stat
```

Commit only after implementation and tests are verified.
