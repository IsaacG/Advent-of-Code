#!/bin/python
"""Advent of Code, Day 10: Hoof It."""
from lib import aoc


def solve(data: aoc.Map, part: int) -> int:
    """Score and rate trails by computing how to walk the trail to a 9."""
    total = 0
    maps = data.coords
    for trailhead in maps[0]:
        trails: set[tuple[tuple[int, int], tuple[tuple[int, int], ...]]] = {(trailhead, (trailhead,))}
        for elevation in range(1, 10):
            new_trails = set()
            for last_pos, path in trails:
                coords = maps[elevation]
                for dx, dy in aoc.FOUR_DIRECTIONS_T:
                    if (new_pos := (last_pos[0] + dx, last_pos[1] + dy)) in coords:
                        new_trails.add((new_pos, path + (new_pos,)))
            trails = new_trails
        total += len({trail[0 if part == 1 else 1] for trail in trails})
    return total


SAMPLE = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""
TESTS = [(1, SAMPLE, 36), (2, SAMPLE, 81)]
# vim:expandtab:sw=4:ts=4
