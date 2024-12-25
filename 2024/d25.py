#!/bin/python
"""Advent of Code, Day 25: Code Chronicle."""

from lib import aoc

SAMPLE = """\
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""


class Day25(aoc.Challenge):
    """Day 25: Code Chronicle."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=3),
        aoc.TestCase(part=2, inputs=SAMPLE, want=aoc.TEST_SKIP),
    ]
    INPUT_PARSER = aoc.ParseBlocks([aoc.parse_one_str_per_line])

    def part1(self, puzzle_input: list[list[str]]) -> int:
        """Count how many keys (loosely) fit locks."""
        size = len(next(zip(*puzzle_input[0])))
        keys: list[list[int]] = []
        locks: list[list[int]] = []
        for block in puzzle_input:
            obj_type = locks if block[0][0] == "#" else keys
            obj_type.append([i.count("#") for i in zip(*block)])

        return sum(
            all(a + b <= size for a, b in zip(key, lock))
            for key in keys for lock in locks
        )

# vim:expandtab:sw=4:ts=4
