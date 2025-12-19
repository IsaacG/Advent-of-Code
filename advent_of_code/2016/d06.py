#!/bin/python
"""Advent of Code, Day 6: Signals and Noise.

Extract the most and least common value from each column.
"""

import collections

from lib import aoc

SAMPLE = """\
eedadn\ndrvtee\neandsr\nraavrd\n\
atevrs\ntsrnev\nsdttsa\nrasrtv\n\
nssdts\nntnada\nsvetve\ntesnvt\n\
vntsnd\nvrdear\ndvrsen\nenarar"""

InputType = list[str]


class Day06(aoc.Challenge):
    """Day 6: Signals and Noise."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want="easter"),
        aoc.TestCase(inputs=SAMPLE, part=2, want="advent"),
    ]
    INPUT_PARSER = aoc.parse_one_str_per_line

    def solver(self, puzzle_input: InputType, part_one: bool) -> str:
        idx = 0 if part_one else -1
        return "".join(
            collections.Counter(col).most_common()[idx][0]
            for col in zip(*puzzle_input)
        )
