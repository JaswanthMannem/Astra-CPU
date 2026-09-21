# Astra V1 Instruction Set Architecture

## Overview

Astra V1 uses 8-bit instruction words and a 4-bit datapath.

Registers:

```text
R0 = 00
R1 = 01
R2 = 10
R3 = 11
```

## Opcodes

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

## R-Type

Binary arithmetic and logical operations use:

```text
opcode | destination | source
  4    |      2      |   2
```

Example:

```asm
ADD R1, R2
```

Semantics:

```text
R1 <- R1 + R2
```

This format is used by ADD, SUB, AND, OR, and XOR.

## NOT

```text
opcode | destination | 00
  4    |      2      |  2
```

Example:

```asm
NOT R1
```

Semantics:

```text
R1 <- NOT(R1)
```

## LOAD

```asm
LOAD R1, 5
```

LOAD needs 10 bits: 4 opcode bits, 2 register bits, and 4 address bits. It therefore occupies two 8-bit instruction-memory words.

First word:

```text
opcode | register | 00
```

Second word:

```text
0000 | address
```

Semantics:

```text
Rdst <- MEM[address]
```

## STORE

```asm
STORE R1, 8
```

STORE also occupies two words.

Semantics:

```text
MEM[address] <- Rsrc
```

## JUMP

```text
opcode | address
  4    |   4
```

Example:

```asm
JUMP 6
```

Semantics:

```text
PC <- 6
```

## HALT

HALT is encoded as:

```text
opcode | 0000
```

It stops CPU execution.

## Program Counter

The PC is 4 bits wide, so addresses range from 0 through 15.

The PC advances by one word normally and by two words for LOAD and STORE.

## Labels

Labels refer to instruction-memory word addresses:

```asm
start:
    LOAD R0, 4
    JUMP start
```

Forward references are supported.

## Arithmetic

Register values are 4-bit unsigned values. Arithmetic wraps within four bits:

```text
1111 + 0001 = 0000
```

## V1 Limitations

V1 does not include conditional branches, CALL/RET, stack instructions, immediate arithmetic, I/O, interrupts, or floating-point operations.
