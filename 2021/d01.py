#!/bin/python

"""Advent of Code: Day 01."""


from lib import aoc


SAMPLE = ["""\
199
200
208
210
200
207
240
269
260
263
"""]


class Day01(aoc.Challenge):
    """Examine the sea floor depth to determine how many values are increases."""

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=7),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=5),
    )

    def part1(self, puzzle_input: list[int]) -> int:
        """Return the number of "steps" with an increase.

        Given a list of numbers, count how many of those elements are increases
        (greater than) the prior element.
        """
        return sum(b > a for a, b in zip(puzzle_input, puzzle_input[1:]))

    def part2(self, puzzle_input: list[int]) -> int:
        """Use a rolling window (summed) for steps.

        Same as part1 but use a rolling sum of three elements for each step.
        """
        groups = [a + b + c for a, b, c in zip(puzzle_input, puzzle_input[1:], puzzle_input[2:])]
        return self.part1(groups)
