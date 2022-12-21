#!/bin/python
"""Advent of Code, Day 21: Monkey Math."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

import typer
from lib import aoc

SAMPLE = [
    """\
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32""",  # 1
]

LineType = int
InputType = list[LineType]


class Day21(aoc.Challenge):
    """Day 21: Monkey Math."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=152),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=301),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    def part1(self, parsed_input: InputType) -> int:
        solved = {}
        for monkey, job in parsed_input.items():
            if job.isdigit():
                solved[monkey] = int(job)
        unsolved = set(parsed_input) - set(solved)
        print(f"{len(parsed_input)=} {len(solved)=} {len(unsolved)=}")
        while unsolved:
            new_solved = set()
            for monkey in unsolved:
                a, op, b = parsed_input[monkey].split()
                if a in solved and b in solved:
                    match op:
                        case "+":
                            solved[monkey] = solved[a] + solved[b]
                        case "-":
                            solved[monkey] = solved[a] - solved[b]
                        case "/":
                            solved[monkey] = solved[a] // solved[b]
                        case "*":
                            solved[monkey] = solved[a] * solved[b]
                    new_solved.add(monkey)
                    if monkey == "root":
                        return solved[monkey]
            unsolved -= new_solved
        raise RuntimeError
        

    def part2(self, parsed_input: InputType) -> int:
        solved = {}
        for monkey, job in parsed_input.items():
            if job.isdigit():
                solved[monkey] = int(job)
        solved["humn"] = "humn"
        unsolved = set(parsed_input) - set(solved)
        print(f"{len(parsed_input)=} {len(solved)=} {len(unsolved)=}")
        while unsolved:
            new_solved = set()
            for monkey in unsolved:
                a, op, b = parsed_input[monkey].split()
                if a in solved and b in solved:
                    match solved[a], op, solved[b]:
                        case [int(x), "+", int(y)]:
                            solved[monkey] = x + y
                        case [int(x), "-", int(y)]:
                            solved[monkey] = x - y
                        case [int(x), "*", int(y)]:
                            solved[monkey] = x * y
                        case [int(x), "/", int(y)]:
                            solved[monkey] = x // y
                        case [_, "+", _]:
                            solved[monkey] = f"({solved[a]})+({solved[b]})"
                        case [_, "-", _]:
                            solved[monkey] = f"({solved[a]})-({solved[b]})"
                        case [_, "*", _]:
                            solved[monkey] = f"({solved[a]})*({solved[b]})"
                        case [_, "/", _]:
                            solved[monkey] = f"({solved[a]})//({solved[b]})"
                    new_solved.add(monkey)
                    if monkey == "root":
                        solved[monkey] = f"({solved[a]}) == ({solved[b]})"
                        print(solved[monkey])
            unsolved -= new_solved
        raise RuntimeError
        

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        out = {}
        for line in puzzle_input.splitlines():
            monkey, job = line.split(": ")
            out[monkey] = job
        return out



if __name__ == "__main__":
    typer.run(Day21().run)

# vim:expandtab:sw=4:ts=4
