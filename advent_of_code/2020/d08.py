#!/usr/bin/env python
"""AoC Day 8: Handheld Halting."""


def compute(lines: list[list[str]]) -> tuple[int, bool]:
    """Run the code, returning the accumulator and if the end was hit."""
    # Accumulator
    acc = 0
    # Instruction pointer. The next instruction to execute.
    ptr = 0
    # Track which instructions were previously executed for loop detection.
    seen = set()
    # max value for the ptr, ie the end of the instructions.
    max_ptr = len(lines) - 1

    while True:
        seen.add(ptr)
        op, sval = lines[ptr]
        val = int(sval)
        if op == 'nop':
            ptr += 1
        elif op == 'jmp':
            ptr += val
        elif op == 'acc':
            ptr += 1
            acc += val
        else:
            raise ValueError(f'Invalid op {op}')

        # Got to the end.
        if ptr > max_ptr:
            return acc, True
        # Loop detection.
        if ptr in seen:
            return acc, False


def solve(data, part: int) -> int:
    """Run a program to get the accumulator value."""
    if part == 1:
        # Run the code until a loop is detected.
        acc, end = compute(data)
        return acc

    # Swap jmp<>nop until the code can run to the end.
    for i, (op, val) in enumerate(data.copy()):
        op, val = data[i]
        line = data[i]
        if op == 'acc':
            continue
        if op == 'nop':
            data[i] = ['jmp', val]
        elif op == 'jmp':
            data[i] = ['nop', val]
        acc, end = compute(data)
        if end:
            return acc
        data[i] = line
    raise RuntimeError


SAMPLE = ["""\
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
""", """\
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
"""]
TESTS = [
    (1, SAMPLE[0], 5),
    (2, SAMPLE[1], 8),
]
