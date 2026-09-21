# Astra

Astra is a **from-scratch 4-bit CPU architecture and emulator implemented in Python**.

The project is built bottom-up from logic gates to a complete programmable CPU. The goal is to understand how the major components of a processor fit together rather than hiding the architecture behind high-level abstractions.

> **Astra V1: 415 tests passing**

---

## Architecture

```text
Assembly Source
      |
   Assembler
      |
Instruction Objects
      |
 Program Loader
      |
Instruction Memory
      |
     CPU
   /     \
Control  Datapath
 Unit      |
         +-- Register File
         +-- ALU
         +-- ALU Control
         +-- Data Memory
         |
      Program Counter
```

Astra is constructed in layers:

```text
Logic Gates
     ↓
Bitwise Logic
     ↓
MUX / DMUX / Decoder / Encoder
     ↓
Adders
     ↓
ALU
     ↓
Latches / Flip-Flops
     ↓
Registers
     ↓
Register File / RAM
     ↓
Program Counter
     ↓
ISA
     ↓
Instruction Decoder
     ↓
ALU Control
     ↓
Datapath
     ↓
Control Unit
     ↓
CPU Cycle
     ↓
CPU
     ↓
Program Loader
     ↓
Assembler
```

---

## V1 Specifications

| Component | Specification |
|---|---|
| Datapath | 4-bit |
| General-purpose registers | 4 |
| Register width | 4-bit |
| Data memory | 16 × 4-bit |
| Instruction memory | 16 × 8-bit |
| Instruction width | 8-bit |
| Register addressing | 2-bit |
| Memory addressing | 4-bit |
| Program counter | 4-bit |
| Assembler | Two-pass |
| Labels | Supported |

---

## Registers

Astra V1 has four general-purpose registers:

```text
R0 = 00
R1 = 01
R2 = 10
R3 = 11
```

Each register stores a 4-bit value.

---

## ALU

The 4-bit ALU supports:

```text
ADD
SUB
AND
OR
XOR
NOT
```

Subtraction is implemented using two's-complement addition:

```text
A - B = A + NOT(B) + 1
```

---

## Memory

### Data Memory

Astra V1 has:

```text
16 words × 4 bits
```

Addresses range from:

```text
0000 → 1111
```

### Instruction Memory

Instruction memory has:

```text
16 words × 8 bits
```

`LOAD` and `STORE` use two instruction-memory words because the ISA requires both a register field and a 4-bit memory address.

---

## Program Counter

The program counter is 4 bits wide.

It supports:

- Hold
- Increment
- Load
- Reset

Priority:

```text
RESET > LOAD > INCREMENT > HOLD
```

It wraps around:

```text
1111 → 0000
```

---

## ISA

Astra V1 supports:

| Opcode | Binary | Instruction |
|---|---|---|
| ADD | `0000` | Addition |
| SUB | `0001` | Subtraction |
| AND | `0010` | Bitwise AND |
| OR | `0011` | Bitwise OR |
| XOR | `0100` | Bitwise XOR |
| NOT | `0101` | Bitwise NOT |
| LOAD | `0110` | Load memory into register |
| STORE | `0111` | Store register into memory |
| JUMP | `1000` | Unconditional jump |
| HALT | `1001` | Stop execution |

Opcodes `1010` through `1111` are reserved.

Example:

```asm
ADD R0, R1
SUB R2, R0
AND R1, R2
OR R3, R1
XOR R0, R3
NOT R0

LOAD R1, 5
STORE R1, 8

JUMP 0
HALT
```

---

## Assembler

Astra includes a two-pass assembler:

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
```

The assembler supports:

- Case-insensitive instructions
- Case-insensitive registers
- `#` comments
- Blank lines
- Labels
- Forward label references
- Backward label references
- Numeric addresses
- Duplicate-label validation
- Undefined-label validation
- Register validation
- Address validation
- Operand-count validation

Example:

```asm
start:
    LOAD R0, 5
    ADD R0, R1
    JUMP finish

finish:
    HALT
```

Labels represent instruction-memory word addresses.

---

## Project Structure

```text
Astra/
├── astra/
│   ├── logic/
│   │   ├── gates.py
│   │   ├── bitwise.py
│   │   ├── mux.py
│   │   ├── dmux.py
│   │   ├── decoder.py
│   │   ├── encoder.py
│   │   ├── adder.py
│   │   ├── alu.py
│   │   ├── sequential.py
│   │   ├── incrementer.py
│   │   ├── program_counter.py
│   │   └── data_memory.py
│   │
│   ├── isa/
│   │   ├── instructions.py
│   │   ├── decoder.py
│   │   └── assembler.py
│   │
│   └── cpu/
│       ├── alu_control.py
│       ├── datapath.py
│       ├── control_unit.py
│       ├── memory_interface.py
│       ├── instruction_memory.py
│       ├── fetch_unit.py
│       ├── fetch_decode.py
│       ├── cpu_cycle.py
│       ├── cpu.py
│       └── program_loader.py
│
├── examples/
│   ├── add.asm
│   ├── subtract.asm
│   ├── load_store.asm
│   ├── jump.asm
│   └── labels.asm
│
├── tests/
│
├── docs/
│   ├── architecture.md
│   ├── isa.md
│   ├── assembler.md
│   └── getting-started.md
│
└── README.md
```

---

## Getting Started

If using `uv`:

```bash
uv sync
```

Run the complete test suite:

```bash
uv run pytest
```

Expected V1 result:

```text
415 passed
```

---

## Running a Program

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

---

## Example Programs

The `examples/` directory contains:

```text
examples/
├── add.asm
├── subtract.asm
├── load_store.asm
├── jump.asm
└── labels.asm
```

These examples are covered by integration tests.

---

## Testing

The project follows:

```text
Implement
   ↓
Write Tests
   ↓
Run Tests
   ↓
Fix
   ↓
Run Full Suite
   ↓
Commit
```

Run everything:

```bash
uv run pytest tests
```

Run an individual test file:

```bash
uv run pytest tests/test_alu.py
```

Run assembler tests:

```bash
uv run pytest tests/test_assembler.py
```

Run CPU execution tests:

```bash
uv run pytest tests/test_program_execution.py
```

---

## Design Philosophy

Astra intentionally models hardware concepts explicitly.

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

The purpose is to make the architecture inspectable and understand how higher-level processor components are constructed from simpler digital components.

---

## CPU Execution

At a high level:

```text
FETCH
  ↓
DECODE
  ↓
EXECUTE
  ↓
WRITE RESULT
  ↓
UPDATE PC
```

For memory instructions, the CPU additionally interacts with data memory.

---

## Reset

```python
cpu.reset()
```

Reset clears:

- Program counter
- Register file
- Data memory
- Halt state

The loaded instruction memory is preserved.

---

## Current Status

### Astra V1 — Complete

```text
[✓] Logic gates
[✓] Combinational logic
[✓] Adders
[✓] ALU
[✓] Sequential logic
[✓] Registers
[✓] Register file
[✓] RAM
[✓] Program counter
[✓] ISA
[✓] Instruction decoder
[✓] Datapath
[✓] Control unit
[✓] Instruction memory
[✓] Data memory
[✓] CPU cycle
[✓] CPU
[✓] CPU reset
[✓] Program loader
[✓] Two-pass assembler
[✓] Labels
[✓] End-to-end execution
[✓] Example programs
[✓] Documentation
[✓] 415 tests passing
```

---

## V1 Boundary

V1 intentionally does not include:

- Conditional branches
- CALL / RET
- Stack
- Interrupts
- Pipeline
- Cache
- I/O peripherals
- Larger datapath widths
- Larger register files

These can be introduced in future versions.

---

## Documentation

Detailed documentation:

- [`docs/architecture.md`](docs/architecture.md)
- [`docs/isa.md`](docs/isa.md)
- [`docs/assembler.md`](docs/assembler.md)
- [`docs/getting-started.md`](docs/getting-started.md)

---

## Version

```text
Astra V1.0.0
```

V1 represents the first complete programmable CPU implementation in the Astra project.

---

## License

MIT License
