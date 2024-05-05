#!/bin/python
"""Advent of Code, Day 14: Reindeer Olympics."""

import re

from lib import aoc

SAMPLE = """\
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds."""

InputType = list[tuple[str, int, int, int]]
PARSE_RE = r"(.*) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds."


class Day14(aoc.Challenge):
    """Day 14: Score a reindeer race."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=1120),
        aoc.TestCase(inputs=SAMPLE, part=2, want=689),
    ]
    INPUT_PARSER = aoc.parse_re_group_mixed(PARSE_RE)

    def distance(self, seconds, speed, fly, rest):
        """Return distance ran after a duration time."""
        rounds, extra = divmod(seconds, fly + rest)
        return speed * (rounds * fly + min(extra, fly))

    def part1(self, parsed_input: InputType) -> int:
        """Return the longest distance at the end of the race."""
        race_len = 1000 if self.testing else 2503
        return max(
            self.distance(race_len, *data)
            for _, *data in parsed_input
        )

    def part2(self, parsed_input: InputType) -> int:
        """Return the biggest score at the end of the race."""
        race_len = 1000 if self.testing else 2503
        points = {name: 0 for name, *_ in parsed_input}

        for i in range(1, race_len + 1):
            positions = {
                name: self.distance(i, speed, fly, rest)
                for name, speed, fly, rest in parsed_input
            }
            max_position = max(positions.values())
            for name, position in positions.items():
                if position == max_position:
                    points[name] += 1
        return max(points.values())
