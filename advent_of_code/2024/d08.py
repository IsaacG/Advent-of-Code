#!/bin/python
"""Advent of Code, Title."""

import collections
import itertools
from lib import aoc
PARSER = aoc.CoordinatesParserC()

def solve(data: aoc.Map, part: int) -> int:
    all_locations = data.all_coords
    antinodes = set()
    for freq in data.non_blank_chars:
        for a, b in itertools.combinations(data.coords[freq], 2):
            sequences: tuple[collections.abc.Iterable[int], collections.abc.Iterable[int]]
            if part == 1:
                sequences = ([2], [-1])
            else:
                sequences = (itertools.count(), itertools.count(step=-1))

            delta = b - a
            for steps in sequences:
                for i in steps:
                    if (node := a + i * delta) in all_locations:
                        antinodes.add(node)
                    else:
                        break

    return len(antinodes)


SAMPLE = """\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""
TESTS = [(1, SAMPLE, 14), (2, SAMPLE, 34)]
# vim:expandtab:sw=4:ts=4
