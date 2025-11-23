#!/bin/python
"""Advent of Code, Day 10: Hoof It."""

from lib import aoc

SAMPLE = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""


class Day10(aoc.Challenge):
    """Day 10: Hoof It."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=36),
        aoc.TestCase(part=2, inputs=SAMPLE, want=81),
    ]
    INPUT_PARSER = aoc.CoordinatesParserC()

    def solver(self, puzzle_input: aoc.Map, part_one: bool) -> int:
        """Score and rate trails by computing how to walk the trail to a 9."""
        total = 0
        maps = puzzle_input.coords
        for trailhead in maps[0]:
            trails: set[tuple[complex, tuple[complex, ...]]] = {(trailhead, (trailhead,))}
            for elevation in range(1, 10):
                new_trails = set()
                for last_pos, path in trails:
                    coords = maps[elevation]
                    for neighbor in aoc.FOUR_DIRECTIONS:
                        if (new_pos := last_pos + neighbor) in coords:
                            new_trails.add((new_pos, path + (new_pos,)))
                trails = new_trails
            total += len({trail[0 if part_one else 1] for trail in trails})
        return total

# vim:expandtab:sw=4:ts=4
