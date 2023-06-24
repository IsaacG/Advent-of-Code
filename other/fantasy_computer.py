#!/bin/python
"""Implement an int code computer.

https://www.reddit.com/r/adventofcode/comments/128t3c6
"""

import typing


class Instruction(typing.NamedTuple):
    code: int
    size: int


MOVR = Instruction(10, 3)
MOVV = Instruction(11, 3)
ADD = Instruction(20, 3)
SUB = Instruction(21, 3)
PUSH = Instruction(30, 2)
POP = Instruction(31, 2)
JP = Instruction(40, 2)
JL = Instruction(41, 4)
CALL = Instruction(42, 2)
RET = Instruction(50, 1)
PRINT = Instruction(60, 2)
HALT = Instruction(255, 1)
INSTRUCTIONS = {
    i.code: i for i in [MOVR, MOVV, ADD, SUB, PUSH, POP, JP, JL, CALL, RET, PRINT, HALT]
}


def debug(message: str, verbose: bool) -> None:
    if verbose:
        print(message)


def run(program: list[int], verbose: bool) -> list[int]:
    """Run a program and return the output."""
    ptr = 0
    registers = [0] * 4
    stack = []
    output = []

    while True:
        instruction = INSTRUCTIONS[program[ptr]]
        size = instruction.size
        if instruction == MOVR:
            # Loads the value from regsrc into regdst. E.g. regdst = regsrc
            reg_dst, reg_src = program[ptr + 1:ptr + size]
            debug(f"{ptr=}: [MOVR, {reg_dst=}, {reg_src=}]", verbose)
            registers[reg_dst] = registers[reg_src]
            ptr += size
        elif instruction == MOVV:
            # Loads the numeric value into register regdst. E.g. regdst = value
            reg_dst, value = program[ptr + 1:ptr + size]
            debug(f"{ptr=}: [MOVV, {reg_dst=}, {value=}]", verbose)
            registers[reg_dst] = value
            ptr += size
        elif instruction == ADD:
            # Adds the value from regsrc to the value of regdst and store the result in reg_dst
            reg_dst, reg_src = program[ptr + 1:ptr + size]
            debug(f"{ptr=}: [ADD, {reg_dst=}, {reg_src=}]", verbose)
            registers[reg_dst] += registers[reg_src]
            ptr += size
        elif instruction == SUB:
            # Subtracts the value of regsrc from the value of regdst and store the result in reg_dst
            reg_dst, reg_src = program[ptr + 1:ptr + size]
            debug(f"{ptr=}: [SUB, {reg_dst=}, {reg_src=}]", verbose)
            registers[reg_dst] -= registers[reg_src]
            ptr += size
        elif instruction == PUSH:
            # Pushes the value of reg_src on the stack
            reg_src, = program[ptr + 1:ptr + size]
            debug(f"{ptr=}: [PUSH, {reg_src=}]", verbose)
            stack.append(registers[reg_src])
            ptr += size
        elif instruction == POP:
            # Pops the last value from stack and loads it into register reg_dst
            reg_dst, = program[ptr + 1:ptr + size]
            debug(f"{ptr=}: [POP, {reg_dst=}]", verbose)
            registers[reg_dst] = stack.pop()
            ptr += size
        elif instruction == JP:
            # Jumps the execution to address addr. Similar to a GOTO!
            addr, = program[ptr + 1:ptr + size]
            debug(f"{ptr=}: [JP, {addr=}]", verbose)
            ptr = addr
        elif instruction == JL:
            # Jump to the address addr only if the value from reg1 < reg2 (IF reg1 < reg2 THEN JP addr)
            reg_1, reg_2, addr = program[ptr + 1:ptr + size]
            debug(f"{ptr=}: [JL, {reg_1=}, {reg_2=}, {addr=}]", verbose)
            if registers[reg_1] < registers[reg_2]:
                ptr = addr
            else:
                ptr += size
        elif instruction == CALL:
            # Pushes onto the stack the address of instruction that follows CALL and then jumps to address addr
            addr, = program[ptr + 1:ptr + size]
            debug(f"{ptr=}: [CALL, {addr=}]", verbose)
            stack.append(ptr + 2)
            ptr = addr
        elif instruction == RET:
            # Pops from the stack the last number, assumes is an address and jump to that address
            debug(f"{ptr=}: [RET]", verbose)
            ptr = stack.pop()
        elif instruction == PRINT:
            # Print on the screen the value contained in the register reg
            reg, = program[ptr + 1:ptr + size]
            debug(f"{ptr=}: [PRINT, {reg=}]", verbose)
            output.append(registers[reg])
            ptr += size
        elif instruction == HALT:
            # Stops our VM. The virtual CPU doesn't execute instructions once HALT is encountered.
            debug(f"{ptr=}: [HALT]", verbose)
            return output


if __name__ == "__main__":
    data = (
        "11,0,10,42,6,255,30,0,11,0,0,11,1,1,11,3,1,60,1,10,2,0,20,2,"
        "1,60,2,10,0,1,10,1,2,11,2,1,20,3,2,31,2,30,2,41,3,2,19,31,0,50"
    )
    output = run([int(i) for i in data.split(",")], False)
    print("Program output: " + ", ".join(str(i) for i in output))

