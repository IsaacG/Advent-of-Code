#!/bin/python
"""Advent of Code: Day 06."""

import typer
from lib import aoc

SAMPLE = [
    "mjqjpqmgbljsphdztnvjfqwrcgsmlb",  # 0
    "mjq",  # 1
    "mjqj",  # 2
    "j",  # 3
    "jpqm",  # 4
    "bvwbjplbgvbhsrlpgdmjqwftvncz",  # 5
    "nppdvjthqldpwncqszvftbrmjlhg",  # 6
    "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",  # 7
    "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw",  # 8
    "1598",  # 9
    "mjqjpqmgbljsphdztnvjfqwrcgsmlb",  # 10
    "bvwbjplbgvbhsrlpgdmjqwftvncz",  # 11
    "nppdvjthqldpwncqszvftbrmjlhg",  # 12
    "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",  # 13
    "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw",  # 14
    "2414",  # 15
]

InputType = str


class Day06(aoc.Challenge):
    """Day 6: Tuning Trouble. Parse data streams to find the start of messages."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[5], part=1, want=5),
        aoc.TestCase(inputs=SAMPLE[6], part=1, want=6),
        aoc.TestCase(inputs=SAMPLE[7], part=1, want=10),
        aoc.TestCase(inputs=SAMPLE[8], part=1, want=11),
        aoc.TestCase(inputs=SAMPLE[10], part=2, want=19),
    ]

    def find_unique_n_start(self, line: str, num: int) -> int:
        """Return the offset *after* a series of n different chars."""
        parts = [line[i:] for i in range(num)]
        for offset, chars in enumerate(zip(*parts)):
            if len(set(chars)) == num:
                return offset + num
        raise RuntimeError("Not found")

    def part1(self, parsed_input: InputType) -> int:
        """Return the start-of-packet marker index."""
        return self.find_unique_n_start(parsed_input, 4)

    def part2(self, parsed_input: InputType) -> int:
        """Return the start-of-message marker marker index."""
        return self.find_unique_n_start(parsed_input, 14)

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return puzzle_input


if __name__ == "__main__":
    typer.run(Day06().run)

# vim:expandtab:sw=4:ts=4
