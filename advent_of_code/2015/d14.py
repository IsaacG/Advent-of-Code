#!/bin/python
"""Advent of Code, Day 14: Reindeer Olympics. 14: Score a reindeer race."""

from lib import aoc


def distance(seconds, speed, fly, rest):
    """Return distance ran after a duration time."""
    rounds, extra = divmod(seconds, fly + rest)
    return speed * (rounds * fly + min(extra, fly))


def solve(data: list[tuple[str, int, int, int]], part: int, testing: bool) -> int:
    """Return the longest distance/biggest score at the end of the race."""
    race_len = 1000 if testing else 2503
    if part == 1:
        return max(distance(race_len, *data) for _, *data in data)

    points = {name: 0 for name, *_ in data}
    for i in range(1, race_len + 1):
        positions = {
            name: distance(i, speed, fly, rest)
            for name, speed, fly, rest in data
        }
        max_position = max(positions.values())
        for name, position in positions.items():
            if position == max_position:
                points[name] += 1
    return max(points.values())


PARSE_RE = r"(.*) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds."
PARSER = aoc.parse_re_group_mixed(PARSE_RE)
SAMPLE = """\
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds."""
TESTS = [
    (1, SAMPLE, 1120),
    (2, SAMPLE, 689),
]
