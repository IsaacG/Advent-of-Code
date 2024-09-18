#!/bin/python
"""Advent of Code, Day 2: Bathroom Security. Follow directions to compute keypad code."""

from lib import aoc

SAMPLE = """\
ULL
RRDDD
LURDL
UUUUD"""

LineType = str
InputType = list[LineType]


class Day02(aoc.Challenge):
    """Day 2: Bathroom Security."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want="1985"),
        aoc.TestCase(inputs=SAMPLE, part=2, want="5DB3"),
    ]

    def solver(self, puzzle_input: InputType, part_one: bool) -> str:
        """Walk a keypad following directions to compute a code."""
        pad_layout = "123\n456\n789" if part_one else "1\n234\n56789\nABC\nD"
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
        for line in puzzle_input:
            for val in line:
                if cur + directions[val] in pad:
                    cur += directions[val]
            out.append(pad[cur])
        return "".join(out)

# vim:expandtab:sw=4:ts=4
