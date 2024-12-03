#!/bin/python
"""Advent of Code, Day 10: The Stars Align. Read a message in the sky."""

from typing import Sequence
from lib import aoc

SAMPLE = """\
position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>"""

LineType = Sequence[int]
InputType = list[LineType]


class Day10(aoc.Challenge):
    """Day 10: The Stars Align."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want="HI"),
        aoc.TestCase(inputs=SAMPLE, part=2, want=3),
    ]

    def solver(self, puzzle_input: InputType, part_one: bool) -> int | str:
        """Return the message in the moving stars."""
        height = 8 if self.testing else 10
        points = puzzle_input
        for i in range(12000):
            points = [(x + dx, y + dy, dx, dy) for x, y, dx, dy in points]
            ymin = min(y for _, y, _, _ in points)
            ymax = max(y for _, y, _, _ in points)
            if ymax - ymin + 1 != height:
                continue
            ocr = aoc.OCR.from_point_set({complex(x, y) for x, y, _, _ in points})
            if ocr.is_valid():
                return [ocr.as_string(), i + 1][0 if part_one else 1]
        raise RuntimeError("Unreachable.")
