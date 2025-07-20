#!/bin/python
"""Advent of Code, Day 17: Reservoir Research."""
from __future__ import annotations

import functools
import sys
import typing

from lib import aoc

SAMPLE = """\
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504"""


class Day17(aoc.Challenge):
    """Day 17: Reservoir Research."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=57),
        aoc.TestCase(part=2, inputs=SAMPLE, want=29),
    ]
    INPUT_PARSER = aoc.parse_re_group_mixed(r"([xy])=(\d+), [xy]=(\d+)..(\d+)")

    def solver(self, puzzle_input: list[list[int | str]], part_one: bool) -> int:
        clay: set[tuple[int, int]] = set()
        for fixed, pos, start, end in typing.cast(list[tuple[str, int, int, int]], puzzle_input):
            if fixed == "x":
                clay.update((pos, i) for i in range(start, end + 1))
            else:
                clay.update((i, pos) for i in range(start, end + 1))
        min_y = min(y for _, y in clay)
        max_y = max(y for _, y in clay)
        min_x = min(x for x, _ in clay)
        max_x = max(x for x, _ in clay)
        filled = clay.copy()

        source = (500, min_y - 1)
        wet = set()

        def show():  # pylint: disable=W0612
            for y in range(min_y, max_y + 1):
                self.debug(
                    "".join(
                        "#" if (x,y) in clay else
                        "~" if (x,y) in filled else
                        "|" if (x,y) in wet else
                        " "
                        for x in range(min_x - 1, max_x + 2
                    )
                )
            )
            print()

        @functools.cache
        def has_leaks(x, y):
            # If we got to the bottom, there is nothing more to do.
            if y == max_y:
                return True
            # Check if we can flow downwards.
            new_pos = (x, y + 1)
            if new_pos not in filled:
                wet.add(new_pos)
                if has_leaks(*new_pos):
                    return True
            # Water does not escape downwards. Flow sideways: left then right.
            expanded = {(x, y)}
            leaks = False
            for dx in [-1, 1]:
                new_x = x
                while True:
                    new_x += dx
                    # Stop going sideways when we hit a wall.
                    if (new_x, y) in filled:
                        break
                    expanded.add((new_x, y))
                    # Try to flow downwards.
                    if (new_x, y + 1) not in filled:
                        wet.add((new_x, y + 1))
                        if has_leaks(new_x, y + 1):
                            leaks = True
                            break
            wet.update(expanded)
            if not leaks:
                filled.update(expanded)
            return leaks

        sys.setrecursionlimit(5000)
        has_leaks(*source)

        # Wet soil.
        if part_one:
            return len(wet)
        # Standing water.
        return len(filled - clay)

# vim:expandtab:sw=4:ts=4
