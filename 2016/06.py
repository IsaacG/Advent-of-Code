#!/bin/python
"""Advent of Code, Day 6: Signals and Noise. Extract the most and least common value from each column."""

import collections

from lib import aoc

SAMPLE = """\
eedadn\ndrvtee\neandsr\nraavrd\n
atevrs\ntsrnev\nsdttsa\nrasrtv\n
nssdts\nntnada\nsvetve\ntesnvt\n
vntsnd\nvrdear\ndvrsen\nenarar"""

InputType = list[str]


class Day06(aoc.Challenge):
    """Day 6: Signals and Noise."""

    PARAMETERIZED_INPUTS = [0, -1]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want="easter"),
        aoc.TestCase(inputs=SAMPLE, part=2, want="advent"),
    ]

    INPUT_PARSER = aoc.parse_one_str_per_line

    def solver(self, parsed_input: InputType, idx: int) -> str:
        return "".join(
            collections.Counter(col).most_common()[idx][0]
            for col in zip(*parsed_input)
        )
