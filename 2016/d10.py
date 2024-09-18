#!/bin/python
"""Advent of Code, Day 10: Balance Bots. Simulate a bot factory."""

import collections
import math

from lib import aoc

SAMPLE = """\
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2"""


class Day10(aoc.Challenge):
    """Day 10: Balance Bots."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=2),
        aoc.TestCase(inputs=SAMPLE, part=2, want=2 * 3 * 5),
    ]

    def solver(self, puzzle_input: list[str], param: bool) -> int:
        """Simulate a bot factory."""
        want = [2, 5] if self.testing else [17, 61]
        bots = collections.defaultdict(list)
        outputs: dict[int, list[int]] = collections.defaultdict(list)
        instructions = {}

        # Parse the input, setting up initial bot states and instructions.
        for line in puzzle_input:
            match line.split():
                case ["value", value, "goes", "to", "bot", bot]:
                    bots[int(bot)].append(int(value))
                case [
                    "bot", bot, "gives", "low", "to",
                    low_type, low, "and", "high", "to", high_type, high,
                ]:
                    instructions[int(bot)] = ((low_type, int(low)), (high_type, int(high)))

        # Simulate bots until nothing is changing.
        # Note: we can exit earlier by waiting for the needed exit conditions.
        # These bots have two pieces and are ready to act.
        while full := [(bot, values) for bot, values in bots.items() if len(values) == 2]:
            for bot, values in full:
                # Check if the output bot is full, ie the acting bot cannot hand off pieces.
                # Note: this check doesn't seem strictly needed.
                if any(out_type == "bot" and len(bots[out]) == 2 for out_type, out in instructions[bot]):
                    continue

                ordered = sorted(values)
                values.clear()

                # Part one: return which bot handles the wanted pieces.
                if not param and ordered == want:
                    return bot

                for value, (out_type, out) in zip(ordered, instructions[bot]):
                    sink: dict[int, list[int]] = bots if out_type == "bot" else outputs
                    sink[out].append(value)

        # Part two: outputs 0, 1, 2 should have exactly one piece.
        assert param
        stacks = [outputs[i] for i in range(3)]
        assert all(len(stack) == 1 for stack in stacks)
        return math.prod(stack[0] for stack in stacks)
