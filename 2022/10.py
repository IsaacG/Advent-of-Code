#!/bin/python
"""Advent of Code, Day 10: Cathode-Ray Tube."""

import collections
import functools
import math
import re

import typer
from lib import aoc

SAMPLE = [
    """\
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop""",  # 30
]

LineType = int
InputType = list[LineType]


class Day10(aoc.Challenge):
    """Day 10: Cathode-Ray Tube."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=13140),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=0),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    # Convert lines to type:
    INPUT_TYPES = LineType
    # Split on whitespace and coerce types:
    # INPUT_TYPES = [str, int]
    # Apply a transform function
    # TRANSFORM = lambda _, l: (l[0], int(l[1:]))

    def part1(self, parsed_input: InputType) -> int:
        inst = []
        for parts in parsed_input:
            match parts:
                case ["noop"]:
                    inst.append(parts)
                case ["addx", _]:
                    inst.append(["noop"])
                    inst.append(parts)
        cycle = 0
        regx = 1
        out = 0
        for parts in inst:
            cycle += 1
            if (cycle + 20) % 40 == 0:
                out += regx * cycle
            match parts:
                case ["noop"]:
                    pass
                case ["addx", _]:
                    regx += int(parts[1])
            if cycle > 220:
                break
        return out


    def part2(self, parsed_input: InputType) -> int:
        inst = []
        for parts in parsed_input:
            match parts:
                case ["noop"]:
                    inst.append(parts)
                case ["addx", _]:
                    inst.append(["noop"])
                    inst.append(parts)
        cycle = 0
        regx = 1
        out = 0
        pixels = []
        for parts in inst:
            cycle += 1
            pos = (cycle - 1) % 40
            if (cycle + 20) % 40 == 0:
                out += regx * cycle
            pixels.append(abs(pos - regx) > 1)
            match parts:
                case ["noop"]:
                    pass
                case ["addx", _]:
                    regx += int(parts[1])
            if cycle > 320:
                break
        rows = [pixels[i*40:(i+1)*40] for i in range(6)]
        return aoc.OCR(rows).as_string()

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return [
            tuple(
                int(i) if i.isdigit() else i
                for i in line.split()
            )
            for line in puzzle_input.splitlines()
        ]
        # Regex splitting
        patt = re.compile(r"(.*) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.")
        return [
            tuple(
                int(i) if i.isdigit() else i
                for i in patt.match(line).groups()
            )
            for line in puzzle_input.splitlines()
        ]

    # def line_parser(self, line: str):
    #     pass


if __name__ == "__main__":
    typer.run(Day10().run)

# vim:expandtab:sw=4:ts=4
