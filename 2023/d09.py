#!/bin/python
"""Advent of Code, Day 9: Mirage Maintenance."""

from lib import aoc

SAMPLE = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

InputType = list[list[int]]


class Day09(aoc.Challenge):
    """Day 9: Mirage Maintenance."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=114),
        aoc.TestCase(inputs=SAMPLE, part=2, want=2),
    ]
    INPUT_PARSER = aoc.parse_multi_int_per_line

    def get_prior_and_following(self, line) -> tuple[int, int]:
        """Return the prior and following value of a line using recursive first differences."""
        diffs = [b - a for a, b in zip(line, line[1:])]
        if all(i == 0 for i in diffs):
            prior = following = 0
        else:
            prior, following = self.get_prior_and_following(diffs)
        return line[0] - prior, line[-1] + following

    def solver(self, puzzle_input: InputType, part_one: bool) -> int:
        """Compute the next value in a series using repeated first differences."""
        # Sum up the prior or following value from each line.
        return sum(
            self.get_prior_and_following(line)[1 if part_one else 0]
            for line in puzzle_input
        )

# vim:expandtab:sw=4:ts=4
