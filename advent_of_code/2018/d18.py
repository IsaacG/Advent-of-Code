#!/bin/python
"""Advent of Code, Day 18: Settlers of The North Pole."""

import math
import typing

from lib import aoc
import frozendict

SAMPLE = """\
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|."""


class Day18(aoc.Challenge):
    """Day 18: Settlers of The North Pole."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=1147),
        aoc.TestCase(part=2, inputs=SAMPLE, want=aoc.TEST_SKIP),
    ]
    INPUT_PARSER = aoc.CoordinatesParser(chars=None, origin_top_left=True)

    def solver(self, puzzle_input: aoc.Map, part_one: bool) -> int:
        area = typing.cast(frozendict.frozendict[complex, str], frozendict.frozendict(puzzle_input.chars))

        def transform(coord: complex) -> str:
            """Return the next value for a cell."""
            match area[coord]:
                case ".":
                    return "|" if sum(area.get(coord + d, ".") == "|" for d in aoc.EIGHT_DIRECTIONS) >= 3 else "."
                case "|":
                    return "#" if sum(area.get(coord + d, ".") == "#" for d in aoc.EIGHT_DIRECTIONS) >= 3 else "|"
                case _:  # "#"
                    adjacent = {area.get(coord + d, ".") for d in aoc.EIGHT_DIRECTIONS}
                    return "#" if "#" in adjacent and "|" in adjacent else "."

        steps = 10 if part_one else 1000000000
        # Cycle tracking. A set for effiecient existence check. A list for ordered states.
        seen = set()
        states: list[frozendict.frozendict[complex, str]] = []
        for step in range(steps):
            area = frozendict.frozendict((coord, transform(coord)) for coord in area)
            # Cycle detection logic.
            if area in seen:
                last_seen = states.index(area)
                cycle_length = step - states.index(area)
                remaining_steps = (steps - step - 1) % cycle_length
                area = states[last_seen + remaining_steps]
                break
            seen.add(area)
            states.append(area)
        return math.prod(sum(i == char for i in area.values()) for char in "|#")

# vim:expandtab:sw=4:ts=4
