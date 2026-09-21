# Astra — Roadmap

Astra is a computer architecture project built from the ground up, starting with basic digital logic and gradually building toward a complete working computer.

The project is developed incrementally:

```text
small components
    ↓
combinational logic
    ↓
arithmetic
    ↓
ALU
    ↓
sequential logic
    ↓
registers
    ↓
memory
    ↓
datapath
    ↓
ISA
    ↓
CPU
    ↓
assembler
    ↓
programs
    ↓
complete computer
```

The goal is not only to make Astra work, but to understand how each layer is constructed from the layer below it.

---

# 🗺️ Roadmap

## Phase 1 — Basic Logic Gates

Build and test the fundamental Boolean operations.

- [x] AND gate
- [x] OR gate
- [x] XOR gate
- [x] NOT gate
- [x] NAND gate
- [x] NOR gate
- [x] XNOR gate
- [x] Input validation
- [x] Unit tests

### Goal

Understand and implement the basic building blocks used by all higher-level digital circuits.

---

## Phase 2 — Multiplexers & Selectors

Build components that allow Astra to select and route data.

- [x] 2-to-1 MUX
- [x] 4-to-1 MUX
- [x] 8-to-1 MUX
- [x] 1-to-2 DEMUX
- [x] 1-to-4 DEMUX
- [x] Unit tests
- [x] Invalid-input tests

### Goal

Build reliable data-selection and routing components.

---

## Phase 3 — Encoders & Decoders

Build components for translating between input combinations and encoded representations.

- [x] 2-to-4 Decoder
- [x] 4-to-2 Encoder
- [x] Input validation
- [x] Invalid-state handling
- [x] Unit tests

### Goal

Understand how digital systems represent and decode control information.

---

## Phase 4 — Multi-Bit Logic

Extend 1-bit operations to operate on multiple bits.

- [x] 4-bit AND
- [x] 4-bit OR
- [x] 4-bit XOR
- [x] 4-bit NOT
- [x] 4-bit MUX
- [x] Multi-bit input validation
- [x] Unit tests

### Implementation Principle

Astra is built one bit at a time.

```text
A = A3 A2 A1 A0
B = B3 B2 B1 B0

A3, B3 → operation
A2, B2 → operation
A1, B1 → operation
A0, B0 → operation
```

The same 1-bit operation is reused for every bit.

---

## Phase 5 — Arithmetic

Build arithmetic components from previously implemented logic.

### Half Adder

- [x] Sum output
- [x] Carry output
- [x] Truth-table tests

### Full Adder

- [x] Sum output
- [x] Carry output
- [x] Carry-in handling
- [x] Truth-table tests
- [x] Edge-case tests

### Ripple Carry Adder

- [x] Connect full adders
- [x] 1-bit addition
- [x] 4-bit ripple carry adder
- [x] Carry propagation
- [x] Carry-out
- [x] Overflow behavior
- [x] Addition tests
- [x] Edge-case tests

### Goal

Create reliable arithmetic building blocks that can be reused by the ALU.

---

## Phase 6 — ALU

The ALU is the first major integration point of Astra.

### Logical Operations

- [x] 4-bit AND
- [x] 4-bit OR
- [x] 4-bit XOR
- [x] 4-bit NOT

### Arithmetic Operations

- [x] Addition
- [x] Subtraction
- [x] Carry handling
- [x] Signed arithmetic
- [x] Arithmetic edge cases

### Operation Selection

- [x] Define ALU operation codes
- [x] Calculate logical results
- [x] Calculate arithmetic results
- [x] Select operation using MUX
- [x] Produce final ALU result

### ALU Flags

- [x] Zero flag
- [x] Carry flag
- [x] Negative/sign flag
- [x] Overflow flag

### ALU Testing

- [x] Test every operation
- [x] Test zero inputs
- [x] Test maximum values
- [x] Test carry cases
- [x] Test signed values
- [x] Test overflow cases
- [x] Test invalid inputs
- [x] Integration tests

### Goal

Create the computational core of Astra.

---

## Phase 7 — Sequential Logic

Introduce state and memory into the system.

- [x] SR latch
- [x] D latch
- [x] Master-slave D flip-flop
- [x] Rising-edge behavior
- [x] Synchronous state updates
- [x] State-transition tests
- [ ] Unified reset abstraction

### Goal

Understand how sequential logic stores information and changes state on clock events.

---

## Phase 8 — Clock & Timing

Build the timing foundation of Astra.

- [x] Rising/falling edge behavior
- [x] Synchronous state updates
- [x] Clock-driven tests
- [ ] Standalone clock abstraction
- [ ] Unified reset cycle

### Current Status

Astra components already use explicit clock phases and demonstrate rising-edge/synchronous behavior. A separate system-wide clock abstraction is not required by V1.

### Goal

Provide a cleaner timing model for future versions.

---

## Phase 9 — Registers & Register File

Build storage components used by the processor.

### Registers

- [x] 1-bit register
- [x] 4-bit register
- [x] Register load control
- [x] Register tests
- [ ] Generic register-enable abstraction
- [ ] Generic register-reset abstraction

### Register File

- [x] 4 registers
- [x] 2-bit register addressing
- [x] Two independent read ports
- [x] Single write port
- [x] Write enable
- [x] Register file tests

### Goal

Provide fast temporary storage for the CPU.

---

## Phase 10 — Counters & Program Counter

Build components that allow the processor to track execution.

- [x] 4-bit incrementer
- [x] 4-bit counter
- [x] 4-bit Program Counter
- [x] PC increment
- [x] PC load
- [x] PC reset
- [x] Jump support
- [x] PC wraparound
- [x] PC tests
- [ ] Conditional branch support

### Goal

Create the mechanism that determines which instruction executes next.

---

## Phase 11 — Memory

Build the storage system used by Astra.

### Data Memory

- [x] Basic memory cells
- [x] Address selection
- [x] Read operation
- [x] Write operation
- [x] Write enable
- [x] 16 × 4-bit data memory
- [x] RAM tests
- [x] Boundary tests

### Instruction Memory

- [x] 16 × 8-bit instruction memory
- [x] Program storage
- [x] Instruction fetching
- [x] Program counter integration
- [x] Instruction memory tests

### Goal

Allow Astra to store both program instructions and data.

---

## Phase 12 — Datapath

Connect the major hardware components together.

- [x] Register file integration
- [x] ALU integration
- [x] Register → ALU path
- [x] ALU → register path
- [x] Memory → register path
- [x] Register → memory path
- [x] Program counter integration
- [x] Instruction fetch path
- [x] Datapath tests

### Goal

Create the physical/logical paths through which information moves inside Astra.

---

## Phase 13 — Instruction Set Architecture

Define Astra's machine language.

### Instruction Format

- [x] 8-bit instruction width
- [x] 4-bit opcode
- [x] 2-bit register fields
- [x] 4-bit address fields
- [x] R-type format
- [x] N-type format
- [x] M-type two-word format
- [x] J-type format
- [x] H-type format

### Instruction Set

- [x] ADD
- [x] SUB
- [x] AND
- [x] OR
- [x] XOR
- [x] NOT
- [x] LOAD
- [x] STORE
- [x] JUMP
- [x] HALT

### Encoding & Decoding

- [x] Opcode table
- [x] Register encoding
- [x] Instruction encoding
- [x] Instruction decoder
- [x] Opcode decoding
- [x] Operand extraction
- [x] JUMP address decoding
- [x] LOAD/STORE address-word decoding
- [x] Invalid instruction detection
- [x] Encoder tests
- [x] Decoder tests

### Goal

Define exactly how Astra represents and understands instructions.

---

## Phase 14 — Control Unit

Build the logic responsible for controlling the processor.

### Control Signals

- [x] ALU control signals
- [x] Register control signals
- [x] Memory control signals
- [x] PC control signals
- [x] Halt control

### Instruction Cycle

- [x] Fetch
- [x] Decode
- [x] Execute
- [x] Memory access
- [x] Write-back
- [x] PC update

### Sequencing

- [x] Instruction sequencing
- [x] LOAD/STORE multi-word sequencing
- [x] Jump control
- [x] Halt control
- [x] Reset sequence

### Goal

Turn the datapath into a processor capable of executing instructions.

---

## Phase 15 — Complete CPU

Integrate all major hardware components.

```text
             ┌─────────────────┐
             │  Control Unit   │
             └────────┬────────┘
                      │
                      ▼
        ┌───────────────────────────┐
        │          Datapath         │
        │                           │
        │ Register File → ALU       │
        │       ↑           ↓       │
        │       └── Memory ─┘       │
        └─────────────┬─────────────┘
                      │
                      ▼
                Instruction
                  Memory
```

### Integration

- [x] Integrate ALU
- [x] Integrate register file
- [x] Integrate program counter
- [x] Integrate instruction decoder
- [x] Integrate control unit
- [x] Integrate data memory
- [x] Integrate instruction memory
- [x] Integrate fetch/decode logic
- [x] Integrate CPU cycle

### CPU Execution

- [x] Fetch instruction
- [x] Decode instruction
- [x] Execute instruction
- [x] Access memory
- [x] Write result
- [x] Update PC
- [x] HALT execution
- [x] CPU reset

### CPU Tests

- [x] Individual instruction tests
- [x] Multi-instruction tests
- [x] Memory tests
- [x] Full CPU integration tests
- [x] CPU reset tests
- [x] End-to-end execution tests

### Goal

Create a functioning programmable processor.

---

## Phase 16 — CPU Simulator & Debugger

Build tools that make Astra observable and easy to debug.

### CPU Simulator

- [x] Execute one instruction
- [x] Execute multiple instructions
- [x] Run until HALT
- [x] Reset CPU
- [ ] Dedicated clock abstraction

### Debug Information

- [ ] Display PC
- [ ] Display registers
- [ ] Display ALU result
- [ ] Display flags
- [ ] Display current instruction
- [ ] Display memory state
- [ ] Display clock cycle

### Debugger

- [x] Step instruction API
- [ ] Run / pause UI
- [ ] Set breakpoints
- [ ] Inspect registers interactively
- [ ] Inspect memory interactively
- [ ] Trace instructions

### Goal

Make it possible to see exactly what Astra is doing internally while a program executes.

---

## Phase 17 — Assembler

Create a way to write Astra programs using assembly language.

### Assembly Language

- [x] Assembly syntax
- [x] Registers
- [x] Instructions
- [x] Operands
- [x] Numeric addresses
- [x] Labels
- [x] Comments
- [x] Case-insensitive syntax

### Assembler Implementation

- [x] Two-pass assembler
- [x] Instruction validation
- [x] Instruction encoding
- [x] Register encoding
- [x] Label handling
- [x] Address resolution
- [x] Assembly → instruction objects
- [x] Assembler error messages
- [x] Assembler tests
- [x] Label tests
- [x] Assembler execution tests

### Goal

Allow humans to program Astra without writing raw machine code.

---

## Phase 18 — Astra Programs

Run real programs on the Astra CPU.

### V1 Examples

- [x] Arithmetic program
- [x] Subtraction program
- [x] Memory program
- [x] Jump program
- [x] Label program
- [x] Example integration tests

### Future Programs

- [ ] Loop program
- [ ] Conditional program
- [ ] Fibonacci program
- [ ] Array manipulation
- [ ] Searching
- [ ] Sorting
- [ ] Function/subroutine program

### Goal

Demonstrate that Astra is not merely a collection of circuits, but a programmable computer.

---

## Phase 19 — I/O

Give Astra a way to communicate with the outside world.

- [ ] Input abstraction
- [ ] Output abstraction
- [ ] Output device
- [ ] Input device
- [ ] Memory-mapped I/O
- [ ] I/O address range
- [ ] CPU → device communication
- [ ] Device → CPU communication
- [ ] Basic text output
- [ ] Display abstraction
- [ ] I/O tests

### Goal

Allow Astra programs to interact with external devices.

---

## Phase 20 — Astra Runtime / Tiny Operating Environment

Build a minimal software layer on top of the CPU.

### Runtime

- [ ] Program loading
- [ ] Basic system calls
- [ ] Basic I/O interface
- [ ] Program termination
- [ ] Simple memory management

### Optional Kernel Features

- [ ] Basic process abstraction
- [ ] Simple scheduler
- [ ] Stack support
- [ ] Interrupt mechanism

### Goal

Create a small software environment that runs on Astra hardware.

---

## Phase 21 — End-to-End System

Integrate the entire project.

```text
Assembly Source
      ↓
   Assembler
      ↓
Instruction Objects
      ↓
Program Loader
      ↓
Instruction Memory
      ↓
     CPU
      ↓
Datapath / ALU / Registers
      ↓
Data Memory / I/O
      ↓
Program Result
```

### End-to-End Tests

- [x] Assembly → instruction objects
- [x] Instruction objects → memory
- [x] CPU fetches program
- [x] CPU executes program
- [x] Program accesses memory
- [x] Program uses ALU
- [x] Program uses jumps
- [x] Program halts correctly
- [x] CPU reset and re-execution
- [x] Example programs

### Goal

Run a complete program from source code through the simulated hardware.

---

## Phase 22 — Testing & Validation

Ensure every layer is reliable.

### Unit Tests

- [x] Gate tests
- [x] MUX tests
- [x] Decoder tests
- [x] Encoder tests
- [x] Adder tests
- [x] ALU tests
- [x] Flip-flop tests
- [x] Register tests
- [x] Counter tests
- [x] Memory tests
- [x] ISA tests
- [x] CPU tests
- [x] Assembler tests
- [x] Example tests

### Integration Tests

- [x] ALU + registers
- [x] Registers + datapath
- [x] Datapath + control unit
- [x] CPU + memory
- [x] CPU + assembler
- [x] End-to-end programs

### Edge Cases

- [x] Zero values
- [x] Maximum values
- [x] Carry
- [x] Signed values
- [x] Overflow
- [x] Invalid instructions
- [x] Invalid operands
- [x] Memory boundaries
- [x] Jump boundaries
- [x] Reset behavior

### Current Verification

```text
415 tests passed
```

### Goal

Make Astra predictable, reliable, and easy to verify.

---

## Phase 23 — Cleanup & Documentation

Turn the project into a polished engineering project.

### Code Quality

- [x] Clean project structure
- [x] Type hints
- [x] Useful docstrings
- [x] Remove unnecessary complexity
- [x] Consistent validation
- [x] Value-based instruction equality

### Documentation

- [x] README
- [x] Architecture documentation
- [x] ISA documentation
- [x] Assembler documentation
- [x] Getting-started documentation
- [x] Example programs

### V1 Release

- [x] Full test suite passes
- [x] Example integration passes
- [x] Documentation complete
- [ ] Git tag `v1.0.0`
- [ ] GitHub release

### Goal

Make Astra understandable to someone who has never seen the project before.

---

# 📍 Current Progress

## Astra V1 — Complete

The core Astra V1 computer is implemented and tested.

### Completed Hardware

- [x] Basic logic gates
- [x] Multiplexers / demultiplexers
- [x] Encoders / decoders
- [x] Multi-bit logic
- [x] Half adder
- [x] Full adder
- [x] 4-bit ripple-carry adder
- [x] 4-bit ALU
- [x] Sequential logic
- [x] 1-bit register
- [x] 4-bit register
- [x] 4-register dual-read/single-write register file
- [x] 4-bit RAM
- [x] 16 × 4-bit data memory
- [x] 4-bit incrementer
- [x] 4-bit counter
- [x] 4-bit program counter
- [x] 16 × 8-bit instruction memory

### Completed ISA

- [x] 8-bit instruction width
- [x] 4-bit opcode
- [x] 2-bit register fields
- [x] 4-bit address fields
- [x] R-type format
- [x] N-type format
- [x] M-type two-word format
- [x] J-type format
- [x] H-type format
- [x] ADD
- [x] SUB
- [x] AND
- [x] OR
- [x] XOR
- [x] NOT
- [x] LOAD
- [x] STORE
- [x] JUMP
- [x] HALT

### Completed CPU

- [x] Instruction decoder
- [x] ALU control
- [x] Datapath
- [x] Control unit
- [x] Fetch unit
- [x] Fetch/decode
- [x] CPU cycle
- [x] CPU
- [x] CPU reset
- [x] Program loader

### Completed Software Layer

- [x] Two-pass assembler
- [x] Labels
- [x] Forward label references
- [x] Backward label references
- [x] Assembly validation
- [x] Example programs
- [x] End-to-end execution

### Verification

```text
415 / 415 tests passing
```

---

# 🚀 Astra V2 — Planned

V1 is now a stable baseline. V2 can extend the ISA and CPU capabilities without changing the fundamental V1 architecture unnecessarily.

## Phase 24 — Conditional Branching

First planned ISA extension.

- [ ] Define branch instruction format
- [ ] Define branch opcode(s)
- [ ] BEQ
- [ ] BNE
- [ ] Branch target handling
- [ ] Branch control signals
- [ ] Branch tests
- [ ] Assembler support
- [ ] Conditional program examples

### Goal

Allow Astra programs to make decisions and implement real conditional loops.

---

## Phase 25 — Immediate Instructions

- [ ] Define immediate encoding
- [ ] ADDI
- [ ] ANDI
- [ ] ORI
- [ ] XORI
- [ ] Immediate decoding
- [ ] Immediate tests
- [ ] Assembler support

### Goal

Allow programs to operate directly on constants without first loading values from memory.

---

## Phase 26 — Stack & Subroutines

- [ ] Stack design
- [ ] Stack pointer
- [ ] PUSH
- [ ] POP
- [ ] CALL
- [ ] RET
- [ ] Subroutine examples
- [ ] Stack tests

### Goal

Support reusable functions and structured programs.

---

## Phase 27 — I/O

- [ ] Memory-mapped I/O
- [ ] Input device
- [ ] Output device
- [ ] Text output
- [ ] I/O tests

### Goal

Allow Astra programs to communicate with the outside world.

---

## Phase 28 — Larger Architecture

Possible future extensions:

- [ ] Wider datapath
- [ ] More registers
- [ ] Larger instruction memory
- [ ] Larger data memory
- [ ] More instruction formats
- [ ] Better branch support

---

## Phase 29 — Advanced CPU Architecture

Possible later research directions:

- [ ] Multi-cycle execution
- [ ] Pipeline
- [ ] Pipeline hazards
- [ ] Forwarding
- [ ] Branch prediction
- [ ] Cache
- [ ] Interrupts
- [ ] Memory management

These are deliberately deferred until the simpler architecture is stable.

---

## Phase 30 — Debugger & Visualization

- [ ] Interactive register viewer
- [ ] Interactive memory viewer
- [ ] Instruction trace
- [ ] Breakpoints
- [ ] Clock-cycle visualization
- [ ] Datapath visualization
- [ ] Hardware diagram generation
- [ ] Web-based simulator

---

## Phase 31 — FPGA / Physical Astra

Long-term possibilities:

- [ ] FPGA implementation
- [ ] Hardware synthesis
- [ ] Physical CPU prototype
- [ ] External I/O
- [ ] Physical Astra computer

---

# 🧭 Development Philosophy

Astra is built **from the bottom up**:

```text
Logic Gates
     ↓
MUX / Selectors
     ↓
Encoders / Decoders
     ↓
Multi-Bit Logic
     ↓
Adders
     ↓
ALU
     ↓
Sequential Logic
     ↓
Registers
     ↓
Program Counter
     ↓
Memory
     ↓
Datapath
     ↓
Instruction Set Architecture
     ↓
Control Unit
     ↓
CPU
     ↓
Assembler
     ↓
Programs
     ↓
I/O
     ↓
Runtime
     ↓
Complete Astra Computer
```

Each stage follows:

```text
Understand
    ↓
Design
    ↓
Implement
    ↓
Test
    ↓
Integrate
    ↓
Document
    ↓
Next Stage
```

---

# 🎯 Ultimate Goal

The ultimate goal of Astra is to build a:

> **complete, understandable, programmable computer from the ground up**

Starting with:

```text
0s and 1s
```

and progressing toward:

```text
Astra Assembly Program
        ↓
     Assembler
        ↓
    Machine Code
        ↓
      Memory
        ↓
       CPU
        ↓
   Control Unit
        ↓
       ALU
        ↓
    Registers
        ↓
      Memory
        ↓
      Output
```

The project should make it possible to answer:

> **How does a computer actually work, from individual logic gates all the way to executing a program?**

Astra is the attempt to build that answer.
