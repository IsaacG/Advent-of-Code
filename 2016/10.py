#!/bin/python
"""Advent of Code, Day 10: Balance Bots."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = """\
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2"""

LineType = int
InputType = list[LineType]


class Day10(aoc.Challenge):
    """Day 10: Balance Bots."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=2),
        aoc.TestCase(inputs=SAMPLE, part=2, want=2 * 3 * 5),
    ]

    INPUT_PARSER = aoc.parse_multi_mixed_per_line

    def part1(self, parsed_input: InputType) -> int:
        want = [2, 5] if self.testing else [17, 61]
        bots = collections.defaultdict(list)
        outputs = collections.defaultdict(list)
        instructions = {}
        for line in parsed_input:
            match line:
                case ["value", value, "goes", "to", "bot", bot]:
                    bots[bot].append(value)
                case ["bot", bot, "gives", "low", "to", low_type, low, "and", "high", "to", high_type, high]:
                    instructions[bot] = ((low_type, low), (high_type, high))
                case _:
                    raise ValueError(f"Invalid line {line}")

        self.debug(f"Starting bots: {bots}")

        changed = True
        while changed:
            changed = False
            full = [(bot, values) for bot, values in bots.items() if len(values) == 2]
            for bot, values in full:
                # Check if the output is full, ie this bot cannot hand off pieces.
                if any(
                    out_type == "bot" and len(bots[out]) == 2
                    for out_type, out in instructions[bot]
                ):
                    continue

                changed = True
                ordered = sorted(values)
                values.clear()
                if ordered == want:
                    return bot

                for value, (out_type, out) in zip(ordered, instructions[bot]):
                    sink = bots if out_type == "bot" else outputs
                    sink[out].append(value)

        raise RuntimeError("Ran out of full bots!")


    def part2(self, parsed_input: InputType) -> int:
        want = [2, 5] if self.testing else [17, 61]
        bots = collections.defaultdict(list)
        outputs = collections.defaultdict(list)
        instructions = {}
        for line in parsed_input:
            match line:
                case ["value", value, "goes", "to", "bot", bot]:
                    bots[bot].append(value)
                case ["bot", bot, "gives", "low", "to", low_type, low, "and", "high", "to", high_type, high]:
                    instructions[bot] = ((low_type, low), (high_type, high))
                case _:
                    raise ValueError(f"Invalid line {line}")

        self.debug(f"Starting bots: {bots}")

        changed = True
        while changed:
            changed = False
            full = [(bot, values) for bot, values in bots.items() if len(values) == 2]
            for bot, values in full:
                # Check if the output is full, ie this bot cannot hand off pieces.
                if any(
                    out_type == "bot" and len(bots[out]) == 2
                    for out_type, out in instructions[bot]
                ):
                    continue

                changed = True
                ordered = sorted(values)
                values.clear()

                for value, (out_type, out) in zip(ordered, instructions[bot]):
                    sink = bots if out_type == "bot" else outputs
                    sink[out].append(value)

        stacks = [outputs[i] for i in range(3)]
        assert all(len(stack) == 1 for stack in stacks)
        return math.prod(stack[0] for stack in stacks)

    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        raise NotImplementedError

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return super().input_parser(puzzle_input)
        return puzzle_input.splitlines()
        return puzzle_input
        return [int(i) for i in puzzle_input.splitlines()]
        mutate = lambda x: (x[0], int(x[1])) 
        return [mutate(line.split()) for line in puzzle_input.splitlines()]
        # Words: mixed str and int
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

# vim:expandtab:sw=4:ts=4
