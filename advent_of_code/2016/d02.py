#!/bin/python
"""Advent of Code, Day 2: Bathroom Security. Follow directions to compute keypad code."""

from lib import aoc


def solve(data: list[str], part: int) -> str:
    """Walk a keypad following directions to compute a code."""
    pad_layout = "123\n456\n789" if part == 1 else "1\n234\n56789\nABC\nD"
    pad_rows = pad_layout.splitlines()
    size = max(len(row) for row in pad_rows)
    pad = {
        complex(x, y): key
        for y, row in enumerate(pad_rows)
        for x, key in enumerate(row.center(size))
        if key != " "
    }
    cur = next(pos for pos, key in pad.items() if key == "5")
    directions = aoc.LETTER_DIRECTIONS

    out = []
    for line in data:
        for val in line:
            if cur + directions[val] in pad:
                cur += directions[val]
        out.append(pad[cur])
    return "".join(out)


SAMPLE = "ULL\nRRDDD\nLURDL\nUUUUD"
TESTS = [(1, SAMPLE, "1985"), (2, SAMPLE, "5DB3")]

# vim:expandtab:sw=4:ts=4
