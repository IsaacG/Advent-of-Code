#!/bin/python
"""Advent of Code: Day 05."""

import collections
import functools
import math
import re

import typer
from lib import aoc

SAMPLE = ["""\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""]

InputType = tuple[str, str]


class Day05(aoc.Challenge):
    """Day 5: Supply Stacks."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want="CMZ"),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want="MCD"),
    ]

    def part1(self, parsed_input: InputType) -> str:
        setup_block, moves = parsed_input.split("\n\n")
        setup = setup_block.splitlines()
        stack_count = len(setup[-1].split())
        width = stack_count * 4
        stack = [[] for _ in range(stack_count)]
        for line in setup[-2::-1]:
            line = line.ljust(width)
            for i in range(stack_count):
                crate = line[1 + i * 4]
                if crate != " ":
                    stack[i].append(crate)
        print(stack)
        for line in moves.splitlines():
            move_count, src, dst = [int(i) for i in line.split() if i.isdigit()]
            for i in range(move_count):
                stack[dst - 1].append(stack[src - 1].pop())
        return "".join(s.pop() for s in stack)

    def part2(self, parsed_input: InputType) -> str:
        setup_block, moves = parsed_input.split("\n\n")
        setup = setup_block.splitlines()
        stack_count = len(setup[-1].split())
        width = stack_count * 4
        stack = [[] for _ in range(stack_count)]
        for line in setup[-2::-1]:
            line = line.ljust(width)
            for i in range(stack_count):
                crate = line[1 + i * 4]
                if crate != " ":
                    stack[i].append(crate)

        for line in moves.splitlines():
            move_count, src, dst = [int(i) for i in line.split() if i.isdigit()]
            stack[dst - 1].extend(stack[src - 1][-move_count:])
            for i in range(move_count):
                stack[src - 1].pop()

        return "".join(s.pop() for s in stack)


    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return puzzle_input


if __name__ == "__main__":
    typer.run(Day05().run)

# vim:expandtab:sw=4:ts=4
