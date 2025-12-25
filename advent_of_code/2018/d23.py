#!/bin/python
"""Advent of Code, Day 23: Experimental Emergency Teleportation."""
import collections.abc
import typing
from lib import aoc

SOLVE_WITH_ASSUMPTIONS = False


def solve(data: list[tuple[int, int, int, int]], part: int) -> int:
    """Determine fields of overlapping nanobot signals."""

    if part == 1:
        # Sort on radius. Pick largest.
        rxyz = sorted(((r, x, y, z) for x, y, z, r in data), reverse=True)
        sr, sx, sy, sz = rxyz[0]
        # Count bots within this radius.
        return sum(
            abs(sx - x) + abs(sy - y) + abs(sz - z) <= sr
            for r, x, y, z in rxyz
        )

    # Part two: fast with assumptions.
    # Assume all bots are in a line. Line scan to count overlapping fields.
    points_of_interest = []
    for x, y, z, r in data:
        distance = abs(x) + abs(y) + abs(z)
        points_of_interest.append((max(0, distance - r), 1))
        points_of_interest.append((distance + r + 1, -1))
    points_of_interest.sort()

    most_count, most_distance = 0, 0
    count = 0

    for distance, delta in points_of_interest:
        count += delta
        if count > most_count:
            most_count = count
            most_distance = distance
    if SOLVE_WITH_ASSUMPTIONS:
        return most_distance

    # Part two: slower with less assumptions. Bisect the space.
    # Map sections of space to the bots they contain.
    # Discard smaller sections. Bisect the remaining sections. Repeat until sections are 1 unit large.
    mins = [min(line[i] for line in data) for i in range(3)]
    maxs = [max(line[i] for line in data) for i in range(3)]
    contains = {
        tuple(typing.cast(tuple[int, int], tuple(i)) for i in zip(mins, maxs)): {
            (tuple(bot), r) for *bot, r in data
        }
    }

    def overlaps(cube: collections.abc.Sequence[tuple[int, int]], bot: tuple[int, ...], r: int) -> bool:
        """Return if a nanobot signal overlaps a space segment."""
        distance = sum(
            max(cube[i][0] - bot[i], 0, bot[i] - cube[i][1])
            for i in range(3)
        )
        return distance <= r

    # plane controls which plane we use to bisect. Rotate through planes.
    # Stop when all segments are 1 unit large.
    plane = 0
    while any(a != b for cube in contains for a, b in cube):
        plane = (plane + 1) % 3
        if all(cube[plane][1] == cube[plane][0] for cube in contains):
            continue
        new_contains = {}
        for cube in sorted(contains, key=lambda x: len(contains[x]), reverse=True)[:8]:
            if cube[plane][0] == cube[plane][1]:
                new_contains[cube] = contains[cube]
            else:
                # Divide the segment into two parts.
                segments = [list(cube), list(cube)]
                mid_up = (cube[plane][1] + cube[plane][0] + 1) // 2
                mid_down = (cube[plane][1] + cube[plane][0]) // 2
                segments[0][plane] = (cube[plane][0], mid_down)
                segments[1][plane] = (mid_up, cube[plane][1])
                for segment in segments:
                    new_contains[tuple(segment)] = {
                        (bot, r)
                        for bot, r in contains[cube]
                        if overlaps(segment, bot, r)
                    }
        contains = new_contains

    biggest = sorted(contains, key=lambda x: len(contains[x]), reverse=True)[0]
    distance = sum(abs(i[0]) for i in biggest)
    assert distance == most_distance
    return distance


PARSER = aoc.parse_ints
SAMPLE = [
    """\
pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1""",
    """\
pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5""",
]
TESTS = [(1, SAMPLE[0], 7), (2, SAMPLE[1], 36)]
# vim:expandtab:sw=4:ts=4
