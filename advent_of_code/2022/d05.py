#!/bin/python
"""Advent of Code: Day 05. Supply Stacks. Move crates from stack to stack."""

from lib import aoc
PARSER = aoc.ParseBlocks([aoc.parse_one_str_per_line, aoc.parse_re_findall_int(r"\d+")])


def build_stacks(setup: list[str]) -> list[list[str]]:
    """Build the initial stacks from input."""
    stack_count = len(setup[-1].split())
    width = stack_count * 4
    stack: list[list[str]] = [[] for _ in range(stack_count)]
    for line in setup[-2::-1]:
        line = line.ljust(width)
        for i in range(stack_count):
            crate = line[1 + i * 4]
            if crate != " ":
                stack[i].append(crate)
    return stack


def solve(data: tuple[list[str], list[tuple[int, int, int]]], part: int) -> str:
    """Return crates after moving them with a CrateMover."""
    setup_block, moves = data
    stack = build_stacks(setup_block)

    for move_count, src, dst in moves:
        if part == 1:
            for _ in range(move_count):
                stack[dst - 1].append(stack[src - 1].pop())
        else:
            stack[dst - 1].extend(stack[src - 1][-move_count:])
            del stack[src - 1][-move_count:]
    return "".join(s.pop() for s in stack)


SAMPLE = """\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""
TESTS = [(1, SAMPLE, "CMZ"), (2, SAMPLE, "MCD")]
