#!/bin/python
"""Advent of Code, Day 21: Keypad Conundrum."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
029A
980A
179A
456A
379A""",  # 37
]

LineType = int
InputType = list[LineType]


class Day21(aoc.Challenge):
    """Day 21: Keypad Conundrum."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=126384),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=None),
    ]

    def part1(self, puzzle_input: InputType) -> int:
        NUMPAD_LAYOUT = "789\n456\n123\nX0A"
        ARRPAD_LAYOUT = "X^A\n<v>"
        NUMPAD = {
            char: complex(x, y)
            for y, line in enumerate(NUMPAD_LAYOUT.splitlines())
            for x, char in enumerate(line)
        }
        ARRPAD = {
            char: complex(x, y)
            for y, line in enumerate(ARRPAD_LAYOUT.splitlines())
            for x, char in enumerate(line)
        }

        def pushpad(pad, src, dst):
            offset = pad[dst] - pad[src]
            parts = []
            if offset.real > 0:
                parts.append( ">" * int(offset.real))
            else:
                parts.append( "<" * -int(offset.real))
            if offset.imag > 0:
                parts.append( "v" * int(offset.imag))
            else:
                parts.append( "^" * -int(offset.imag))
            return parts[0] + parts[1] + "A"
            return [parts[0] + parts[1] + "A", parts[1] + parts[0] + "A"]

        total = 0
        if False:
            for line in puzzle_input:
                options = {""}
                for src, dst in zip("A" + line, line):
                    n = set()
                    for opt_a in pushpad(NUMPAD, src, dst):
                        for opt_b in options:
                            n.add(opt_a + opt_b)
                    options = n

                inputs = options
                outputs = set()
                for one_input in inputs:
                    options = {"",}
                    for src, dst in zip("A" + one_input, one_input):
                        n = set()
                        for opt_a in pushpad(ARRPAD, src, dst):
                            for opt_b in options:
                                n.add(opt_a + opt_b)
                        options = n
                    outputs.update(options)

                inputs = outputs
                outputs = set()
                for one_input in inputs:
                    options = {""}
                    for src, dst in zip("A" + one_input, one_input):
                        n = set()
                        for opt_a in pushpad(ARRPAD, src, dst):
                            for opt_b in options:
                                n.add(opt_a + opt_b)
                        options = n
                    outputs.update(options)

                size = min(len(i) for i in outputs)
                complexity = size * int(line.removesuffix("A"))
                print(f"{line}: complexity = {size} * {int(line.removesuffix("A"))} = {complexity}")
                total += complexity



        if True:
            for line in puzzle_input:
                print(line)
                pushes = "".join(pushpad(NUMPAD, src, dst) for src, dst in zip("A" + line, line))
                if line == "179A":
                    print(pushes)
                pushes = "".join(pushpad(ARRPAD, src, dst) for src, dst in zip("A" + pushes, pushes))
                if line == "179A":
                    print(pushes)
                pushes = "".join(pushpad(ARRPAD, src, dst) for src, dst in zip("A" + pushes, pushes))
                if line == "179A":
                    print(pushes)
                complexity = len(pushes) * int(line.removesuffix("A"))
                print(f"{line}: complexity = {len(pushes)} * {int(line.removesuffix("A"))} = {complexity}")
                total += complexity
                        

        if not self.testing:
            assert total != 155462
        return total

    # def part2(self, puzzle_input: InputType) -> int:

    # def solver(self, puzzle_input: InputType, part_one: bool) -> int | str:

# vim:expandtab:sw=4:ts=4
