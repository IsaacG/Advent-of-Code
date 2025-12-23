#!/bin/python
"""Advent of Code, Guard Gallivant. Simulate a guard walking a floor."""

from lib import aoc

def walk(
    all_spots: set[complex], blocked: set[complex], pos: complex, direction: complex
) -> tuple[set[complex], bool]:
    """Walk the map until hitting the edge or entering a loop."""
    spots: set[complex] = set()
    seen: set[complex] = set()
    while pos in all_spots:
        spots.add(pos)
        if (pos[0] + direction[0], pos[1] + direction[1]) in blocked:
            if pos in seen:
                return spots, True
            seen.add(pos)
            while (pos[0] + direction[0], pos[1] + direction[1]) in blocked:
                direction = aoc.rotate_counterclockwise(*direction)
        pos = pos[0] + direction[0], pos[1] + direction[1]
    return spots, False

def solve(data: aoc.Map, part: int) -> int:
    all_spots = data.all_coords
    blocked = data.coords["#"]
    start_pos, start_dir = next(
        (data.coords[arrow].copy().pop(), aoc.ARROW_DIRECTIONS_T[arrow])
        for arrow in "<>v^"
        if arrow in data.coords
    )

    spots, _ = walk(all_spots, blocked, start_pos, start_dir)
    # Part one: return the length of the path until the edge.
    if part == 1:
        return len(spots)

    # Part two: count how many loops can be made by adding one obstable.
    return sum(
        walk(all_spots, blocked | {option}, start_pos, start_dir)[1]
        for option in spots - {start_pos}
    )


SAMPLE = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""
TESTS = [(1, SAMPLE, 41), (2, SAMPLE, 6)]
# vim:expandtab:sw=4:ts=4
