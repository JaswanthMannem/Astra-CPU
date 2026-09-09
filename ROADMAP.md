# Astra — Roadmap

Astra is a computer architecture project built from the ground up, starting with basic digital logic and gradually building toward a complete working computer.

The project is developed incrementally:

**small components → combinational logic → arithmetic → ALU → sequential logic → registers → memory → datapath → ISA → CPU → assembler → programs → complete computer**

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

Build reliable data-selection and routing components that will later be used throughout the CPU.

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

Astra should be built **one bit at a time**.

```text
A = A3 A2 A1 A0
B = B3 B2 B1 B0

A3, B3 → operation
A2, B2 → operation
A1, B1 → operation
A0, B0 → operation
```

The same 1-bit operation is reused for every bit.

### Goal

Learn how simple 1-bit components scale into wider digital operations.

---

## Phase 5 — Arithmetic

Build arithmetic components from the previously implemented logic.

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

The ALU is the first major integration point of Astra. It combines logical and arithmetic operations and selects which result should be produced.

### Logical Operations
- [x] 4-bit AND
- [x] 4-bit OR
- [x] 4-bit XOR
- [x] 4-bit NOT

*Logical operations operate one bit at a time.*

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

### ALU Design Principle

For logical operations:

```text
A3, B3 → logic operation
A2, B2 → logic operation
A1, B1 → logic operation
A0, B0 → logic operation
```

For addition:

```text
A0 ──┐
B0 ──┼→ Full Adder ─→ S0
     │       │
     │      Carry
     │        ↓
A1 ──┐
B1 ──┼→ Full Adder ─→ S1
     │       │
     │      Carry
     │        ↓
A2 ──┐
B2 ──┼→ Full Adder ─→ S2
     │       │
     │      Carry
     │        ↓
A3 ──┐
B3 ──┼→ Full Adder ─→ S3
```

### Goal

Create the computational core of Astra.

---

## Phase 7 — Sequential Logic

Introduce state and memory into the system.

### Storage Elements
- [x] SR latch
- [x] D latch
- [x] D flip-flop
- [ ] Clock input
- [ ] Reset behavior
- [x] State-transition tests

### Goal

Understand the difference between:

```text
Combinational Logic:
Input → Output
```

and:

```text
Sequential Logic:
Input + Previous State → Output + New State
```

This phase introduces the concept of a computer being able to **remember** information.

---

## Phase 8 — Clock & Timing

Build the timing foundation of Astra.

- [ ] Clock abstraction
- [ ] Clock cycles
- [x] Rising/falling edge behavior
- [x] Synchronous state updates
- [ ] Reset cycle
- [x] Clock-driven tests

### Goal

Synchronize state changes so that Astra's components can operate together.

---

## Phase 9 — Registers

Build storage components used by the processor.

### Registers
- [x] 1-bit register
- [x] 4-bit register
- [x] Register load control
- [ ] Register enable
- [ ] Register reset
- [x] Register tests

### Register File
- [ ] Define register count
- [ ] Register addressing
- [ ] Read operation
- [ ] Write operation
- [ ] Write enable
- [ ] Register file tests

### Goal

Provide the CPU with fast temporary storage.

---

## Phase 10 — Counters & Program Counter

Build components that allow the processor to track execution.

- [ ] Incrementer
- [x] Counter
- [ ] Program Counter (PC)
- [ ] PC increment
- [ ] PC load
- [ ] PC reset
- [ ] Jump support
- [ ] Branch support
- [ ] PC tests

### Goal

Create the mechanism that determines which instruction the CPU executes next.

---

## Phase 11 — Memory

Build the storage system used by Astra.

### RAM
- [ ] Basic memory cell
- [ ] Address selection
- [ ] Read operation
- [ ] Write operation
- [ ] Write enable
- [ ] Multi-word RAM
- [ ] RAM tests
- [ ] Boundary tests

### Program / Instruction Memory
- [ ] Program storage
- [ ] Instruction fetching
- [ ] Program counter integration
- [ ] Instruction memory tests

### Goal

Allow Astra to store both program instructions and data.

---

## Phase 12 — Bus & Datapath

Connect the major hardware components together.

### Bus
- [ ] Define internal data bus
- [ ] Data routing
- [ ] Bus selection
- [ ] Bus control

### Datapath
- [ ] Connect registers
- [ ] Connect ALU
- [ ] Connect program counter
- [ ] Connect instruction register
- [ ] Register → ALU path
- [ ] ALU → register path
- [ ] Memory → register path
- [ ] Register → memory path
- [ ] PC → instruction memory path

### Goal

Create the physical/logical paths through which information moves inside Astra.

---

## Phase 13 — Instruction Set Architecture (ISA)

Define Astra's machine language before the final CPU control logic is implemented.

### Instruction Format
- [ ] Define instruction width
- [ ] Define opcode size
- [ ] Define register fields
- [ ] Define immediate fields
- [ ] Define address fields
- [ ] Define instruction types

### Instruction Categories

#### Data Movement
- [ ] LOAD
- [ ] STORE
- [ ] MOV

#### Arithmetic
- [ ] ADD
- [ ] SUB

#### Logic
- [ ] AND
- [ ] OR
- [ ] XOR
- [ ] NOT

#### Comparison
- [ ] CMP
- [ ] Equality comparison
- [ ] Greater/less comparison

#### Control Flow
- [ ] JMP
- [ ] Conditional branch
- [ ] CALL
- [ ] RETURN
- [ ] HALT

### Encoding
- [ ] Define machine-code encoding
- [ ] Define opcode table
- [ ] Define register encoding
- [ ] Define immediate encoding
- [ ] Define branch encoding

### Decoder
- [ ] Instruction decoder
- [ ] Opcode decoding
- [ ] Operand extraction
- [ ] Invalid instruction detection

### Goal

Define exactly how Astra represents and understands instructions.

---

## Phase 14 — Control Unit

Build the logic responsible for controlling the processor.

### Control Signals
- [ ] ALU control signals
- [ ] Register control signals
- [ ] Memory control signals
- [ ] PC control signals
- [ ] Instruction register control

### Instruction Cycle
- [ ] Fetch
- [ ] Decode
- [ ] Execute
- [ ] Memory access
- [ ] Write-back

### Sequencing
- [ ] Instruction sequencing
- [ ] Multi-cycle instructions where necessary
- [ ] Branch control
- [ ] Jump control
- [ ] Reset sequence

### Goal

Turn the datapath into a processor capable of executing instructions.

---

## Phase 15 — Complete CPU

Integrate all major hardware components.

```text
                 ┌─────────────────────┐
                 │     Control Unit    │
                 └──────────┬──────────┘
                            │
                            ▼
       ┌─────────────────────────────────────┐
       │              Datapath               │
       │                                     │
       │ Registers → ALU → Registers         │
       │     ↑           ↓                   │
       │     └───── BUS ─┘                   │
       └──────────────────┬──────────────────┘
                          │
                          ▼
                       Memory
```

### Integration
- [ ] Integrate ALU
- [ ] Integrate register file
- [ ] Integrate program counter
- [ ] Integrate instruction register
- [ ] Integrate instruction decoder
- [ ] Integrate control unit
- [ ] Integrate memory
- [ ] Integrate buses

### CPU Execution
- [ ] Fetch instruction
- [ ] Decode instruction
- [ ] Execute instruction
- [ ] Access memory
- [ ] Write result
- [ ] Update PC

### CPU Tests
- [ ] Individual instruction tests
- [ ] Multi-instruction tests
- [ ] Branch tests
- [ ] Memory tests
- [x] Register tests
- [ ] Full CPU integration tests

### Goal

Create a functioning programmable processor.

---

## Phase 16 — CPU Simulator & Debugger

Build tools that make Astra observable and easy to debug.

### CPU Simulator
- [ ] Clock the CPU
- [ ] Execute one instruction
- [ ] Execute multiple instructions
- [ ] Run until HALT
- [ ] Reset CPU

### Debug Information
- [ ] Display PC
- [ ] Display registers
- [ ] Display ALU result
- [ ] Display flags
- [ ] Display current instruction
- [ ] Display memory state
- [ ] Display clock cycle

### Debugger
- [ ] Step instruction
- [ ] Run / pause
- [ ] Set breakpoints
- [ ] Inspect registers
- [ ] Inspect memory
- [ ] Trace instructions

### Goal

Make it possible to see **exactly what Astra is doing internally** while a program executes.

---

## Phase 17 — Assembler

Create a way to write Astra programs using assembly language.

### Assembly Language
- [ ] Define assembly syntax
- [ ] Define registers
- [ ] Define instructions
- [ ] Define operands
- [ ] Define immediate values
- [ ] Define labels

Example:

```asm
LOAD R1, 10
LOAD R2, 20
ADD  R3, R1, R2
HALT
```

### Assembler Implementation
- [ ] Tokenizer
- [ ] Parser
- [ ] Instruction validation
- [ ] Instruction encoding
- [ ] Register encoding
- [ ] Immediate encoding
- [ ] Label handling
- [ ] Address resolution
- [ ] Assembly → machine code
- [ ] Assembler error messages
- [ ] Assembler tests

### Goal

Allow humans to program Astra without writing raw machine code.

---

## Phase 18 — Astra Programs

Run real programs on the Astra CPU.

### Basic Programs
- [ ] Arithmetic program
- [ ] Memory program
- [ ] Loop program
- [ ] Conditional program
- [x] Counter program
- [ ] Fibonacci program

### Advanced Programs
- [ ] Function/subroutine program
- [ ] Array manipulation
- [ ] Searching
- [ ] Sorting
- [ ] Larger multi-function program

### Goal

Demonstrate that Astra is not merely a collection of circuits, but a programmable computer.

---

## Phase 19 — I/O

Give Astra a way to communicate with the outside world.

### Basic I/O
- [ ] Input abstraction
- [ ] Output abstraction
- [ ] Output device
- [ ] Input device

### Memory-Mapped I/O
- [ ] Define I/O address range
- [ ] Map devices to addresses
- [ ] CPU → device communication
- [ ] Device → CPU communication

### Display
- [ ] Basic text output
- [ ] Simple display abstraction
- [ ] Display tests

### Goal

Allow Astra programs to interact with external devices.

---

## Phase 20 — Astra Runtime / Tiny Operating Environment

Build a minimal software layer on top of the CPU. This does **not** need to become a full modern operating system.

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
                 ASTRA COMPUTER
                       │
              ┌────────┴────────┐
              │                 │
             CPU              Memory
              │                 │
              ├────── BUS ──────┤
              │
         ┌────┴────┐
         │   ALU   │
         └────┬────┘
              │
        ┌─────┴─────┐
        │ Registers │
        └─────┬─────┘
              │
         Control Unit
              │
              ▼
        Astra Program
              │
              ▼
          Assembler
```

### End-to-End Tests
- [ ] Assembly → machine code
- [ ] Machine code → memory
- [ ] CPU fetches program
- [ ] CPU executes program
- [ ] Program accesses memory
- [ ] Program uses ALU
- [ ] Program uses branches
- [ ] Program performs I/O
- [ ] Program completes correctly

### Goal

Run a complete program from source code all the way through the simulated hardware.

---

## Phase 22 — Testing & Validation

Ensure every layer is reliable.

### Unit Tests
- [ ] Gate tests
- [ ] MUX tests
- [ ] Decoder tests
- [ ] Encoder tests
- [ ] Adder tests
- [ ] ALU tests
- [ ] Flip-flop tests
- [x] Register tests
- [x] Counter tests
- [ ] Memory tests
- [ ] CPU tests
- [ ] Assembler tests

### Integration Tests
- [ ] ALU + registers
- [ ] Registers + datapath
- [ ] Datapath + control unit
- [ ] CPU + memory
- [ ] CPU + assembler
- [ ] CPU + I/O
- [ ] End-to-end programs

### Edge Cases
- [ ] Zero values
- [ ] Maximum values
- [ ] Carry
- [ ] Signed values
- [ ] Overflow
- [ ] Invalid instructions
- [ ] Invalid operands
- [ ] Memory boundaries
- [ ] Branch boundaries
- [ ] Reset behavior

### Goal

Make Astra predictable, reliable, and easy to verify.

---

## Phase 23 — Cleanup & Documentation

Turn the project into a polished engineering project.

### Code Quality
- [ ] Clean project structure
- [ ] Refactor duplicated code
- [ ] Improve naming
- [ ] Add type hints
- [ ] Add useful docstrings
- [ ] Remove unnecessary complexity

### Documentation
- [ ] Update README
- [ ] Document architecture
- [ ] Document components
- [ ] Document ALU
- [ ] Document registers
- [ ] Document memory
- [ ] Document datapath
- [ ] Document control unit
- [ ] Document ISA
- [ ] Document assembly syntax
- [ ] Add example programs

### Final Documentation Architecture
```text
Logic
  ↓
Arithmetic
  ↓
ALU
  ↓
Sequential Logic
  ↓
Registers
  ↓
Memory
  ↓
Datapath
  ↓
ISA
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
```

### Goal

Make Astra understandable to someone who has never seen the project before.

---

## Phase 24 — Future Extensions

These are **not required for the core Astra project** and can be added after the complete computer works:

- [ ] Wider word size
- [ ] More CPU instructions
- [ ] Better branch support
- [ ] Stack-based execution
- [ ] Interrupts
- [ ] Pipelining
- [ ] Cache
- [ ] Virtual memory
- [ ] Better debugger
- [ ] Graphical hardware visualization
- [ ] Web-based Astra simulator
- [ ] FPGA implementation
- [ ] Physical Astra computer

---

# 📍 Current Progress

## Completed So Far

### Phase 1 — Basic Logic Gates
- [x] AND gate
- [x] OR gate
- [x] XOR gate
- [x] NOT gate
- [x] NAND gate
- [x] NOR gate
- [x] XNOR gate
- [x] Input validation
- [x] Unit tests

### Phase 2 — Multiplexers & Selectors
- [x] 2-to-1 MUX
- [x] 4-to-1 MUX
- [x] 8-to-1 MUX
- [x] 1-to-2 DEMUX
- [x] 1-to-4 DEMUX
- [x] Unit tests
- [x] Invalid-input tests

### Phase 3 — Encoders & Decoders
- [x] 2-to-4 Decoder
- [x] 4-to-2 Encoder
- [x] Input validation
- [x] Invalid-state handling
- [x] Unit tests

### Phase 4 — Multi-Bit Logic
- [x] 4-bit AND
- [x] 4-bit OR
- [x] 4-bit XOR
- [x] 4-bit NOT
- [x] 4-bit MUX
- [x] Multi-bit input validation
- [x] Unit tests

### Phase 5 — Arithmetic
- [x] Half Adder
- [x] Full Adder
- [x] 4-bit Ripple Carry Adder
- [x] Carry propagation
- [x] Carry-out
- [x] Overflow behavior
- [x] Addition and edge-case tests

### Phase 6 — ALU
- [x] Define ALU operation codes
- [x] Logical operations
- [x] Addition
- [x] Subtraction
- [x] Carry handling
- [x] Signed arithmetic
- [x] ALU operation selection
- [x] Zero flag
- [x] Carry flag
- [x] Negative/sign flag
- [x] Overflow flag
- [x] ALU tests and edge cases
- [x] Integration tests

### Phase 7 — Sequential Logic
- [x] SR latch
- [x] D latch
- [x] D flip-flop
- [x] State-transition tests
- [ ] Clock input abstraction
- [ ] Reset behavior

### Phase 8 — Clock & Timing
- [ ] Clock abstraction
- [ ] Clock cycles
- [x] Rising/falling edge behavior
- [x] Synchronous state updates
- [ ] Reset cycle
- [x] Clock-driven tests

### Phase 9 — Registers
- [x] 1-bit register
- [x] 4-bit register
- [x] Register load control
- [ ] Register enable
- [ ] Register reset
- [x] Register tests

### Phase 10 — Counters & Program Counter
- [ ] Incrementer component
- [x] Counter
- [ ] Program Counter (PC)
- [ ] PC increment
- [ ] PC load
- [ ] PC reset
- [ ] Jump support
- [ ] Branch support
- [ ] PC tests

## Current Stage Summary

**Sequential storage and basic state components are actively progressing.**

Components ready:
- Basic logic through 4-bit ALU
- SR latch, D latch, and D flip-flop
- 1-bit and 4-bit registers with load control
- 4-bit MUX
- 4-bit counter with enable and wraparound

**Next major component:** Register File.

> **Note:** The master-slave D flip-flop already demonstrates rising-edge and synchronous behavior. A standalone clock abstraction and unified reset system have not yet been built.

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
Clock
     ↓
Registers
     ↓
Counters / Program Counter
     ↓
Memory
     ↓
Bus / Datapath
     ↓
Instruction Set Architecture
     ↓
Control Unit
     ↓
CPU
     ↓
Simulator / Debugger
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

Each stage follows an explicit progression:

```text
Understand → Design → Implement → Test → Integrate → Document → Next Stage
```

---

# 🎯 Ultimate Goal

The ultimate goal of Astra is to build a **complete, understandable, programmable computer from the ground up**.

Starting with:

```text
0s and 1s
```

and ending with:

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
      Output
```

The project should make it possible to answer:

> *"How does a computer actually work, from individual logic gates all the way to executing a program?"*

Astra is the attempt to build that answer.