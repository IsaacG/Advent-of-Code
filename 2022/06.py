#!/bin/python
"""Advent of Code: Day 06."""

import typer
from lib import aoc

SAMPLE = [
    "bvwbjplbgvbhsrlpgdmjqwftvncz",
    "nppdvjthqldpwncqszvftbrmjlhg",
    "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
    "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw",
    "mjqjpqmgbljsphdztnvjfqwrcgsmlb",
]

InputType = str


class Day06(aoc.Challenge):
    """Day 6: Tuning Trouble. Parse data streams to find the start of messages."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=5),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=6),
        aoc.TestCase(inputs=SAMPLE[2], part=1, want=10),
        aoc.TestCase(inputs=SAMPLE[3], part=1, want=11),
        aoc.TestCase(inputs=SAMPLE[4], part=2, want=19),
    ]
    INPUT_PARSER = aoc.parse_one_str
    PARAMETERIZED_INPUTS = [4, 14]

    def solver(self, line: str, num: int) -> int:
        """Return the offset *after* a series of n different chars."""
        parts = (line[i:] for i in range(num))
        return next(
            offset + num
            for offset, chars in enumerate(zip(*parts))
            if len(set(chars)) == num
        )


if __name__ == "__main__":
    typer.run(Day06().run)

# vim:expandtab:sw=4:ts=4
