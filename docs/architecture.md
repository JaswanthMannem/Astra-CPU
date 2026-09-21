# Astra Architecture

## Overview

Astra is a small 4-bit CPU implemented from the bottom up in Python. It models digital logic, combinational circuits, sequential circuits, memory, an instruction set, CPU datapath, control logic, an assembler, and end-to-end execution.

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

## Word Sizes

- Datapath: 4 bits
- Registers: 4 bits
- Data memory word: 4 bits
- Data-memory address: 4 bits
- Instruction word: 8 bits
- Instruction-memory address: 4 bits
- Number of registers: 4

## Logic Layer

Primitive gates:

- NOT
- AND
- OR
- XOR
- NAND
- NOR
- XNOR

## Combinational Components

Astra includes multiplexers, demultiplexers, decoders, encoders, adders, bitwise operations, a 4-bit ALU, and an incrementer.

The ALU supports ADD, SUB, AND, OR, XOR, and NOT.

Subtraction uses:

```text
A - B = A + NOT(B) + 1
```

## Sequential Components

Astra models state using:

- SR latch
- D latch
- Master-slave D flip-flop
- 1-bit register
- 4-bit register
- Register file
- RAM
- Program counter

## Register File

The V1 register file contains:

```text
R0 = 00
R1 = 01
R2 = 10
R3 = 11
```

It has two read ports and one write port.

## Data Memory

Astra V1 provides 16 words of 4-bit data memory, addressed by 4 bits.

## Instruction Memory

Instruction memory contains 16 words of 8 bits each and uses a 4-bit address.

## Program Counter

The PC is 4 bits wide and supports:

- Hold
- Increment
- Load
- Reset

Priority:

```text
RESET > LOAD > INCREMENT > HOLD
```

The counter wraps from `1111` to `0000`.

## CPU Cycle

The CPU follows:

```text
Fetch
  -> Decode
  -> Control
  -> Read operands
  -> Execute
  -> Write result
  -> Update PC
```

`LOAD` and `STORE` occupy two instruction-memory words.

## Reset

CPU reset clears:

- Program counter
- Register file
- Data memory
- Halt state

Instruction memory is preserved.

## V1 Scope

Astra V1 includes:

- 4-bit datapath
- Four registers
- 16x4 data memory
- 16x8 instruction memory
- ADD, SUB, AND, OR, XOR, NOT
- LOAD, STORE, JUMP, HALT
- CPU reset
- Two-pass assembler
- Labels
- End-to-end program execution

Conditional branches, interrupts, stacks, pipelining, and larger word sizes are outside V1.
