#!/bin/python
"""Advent of Code, Day 14: Regolith Reservoir."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

import typer
from lib import aoc

SAMPLE = [
    """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9""",
]

LineType = int
InputType = list[LineType]


class Day14(aoc.Challenge):
    """Day 14: Regolith Reservoir."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=24),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=93),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    def part1(self, parsed_input: InputType) -> int:
        rocks = set()
        max_y = 0
        for line in parsed_input:
            for point in line:
                max_y = max(max_y, point.imag)

        for line in parsed_input:
            for start, end in zip(line, line[1:]):
                if start.real == end.real:
                    direction = complex(0, 1)
                    if start.imag > end.imag:
                        end, start = start, end
                else:
                    direction = complex(1, 0)
                    if start.real > end.real:
                        end, start = start, end
                cur = start
                while cur != end:
                    rocks.add(cur)
                    cur += direction
                rocks.add(end)

        directions = (complex(0, 1), complex(-1, 1), complex(1, 1))
        for grain in range(26000):
            cur = complex(500, 0)
            can_move = True
            while can_move and cur.imag < max_y:
                for d in directions:
                    if cur + d not in rocks:
                        cur += d
                        break
                else:
                    can_move = False
                if grain == 4:
                    for d in directions:
                        # print(f"{cur=} {cur+d=} {cur+d in rocks}")
                        pass
            if cur.imag >= max_y:
                return grain
            # print(f"{grain=} landed at {cur}")
            rocks.add(cur)

    def part2(self, parsed_input: InputType) -> int:
        rocks = set()
        max_y = 0
        for line in parsed_input:
            for point in line:
                max_y = max(max_y, point.imag)
        max_y += 2

        for line in parsed_input:
            for start, end in zip(line, line[1:]):
                if start.real == end.real:
                    direction = complex(0, 1)
                    if start.imag > end.imag:
                        end, start = start, end
                else:
                    direction = complex(1, 0)
                    if start.real > end.real:
                        end, start = start, end
                cur = start
                while cur != end:
                    rocks.add(cur)
                    cur += direction
                rocks.add(end)

        directions = (complex(0, 1), complex(-1, 1), complex(1, 1))
        for grain in range(2600000):
            cur = complex(500, 0)
            can_move = True
            while can_move and cur.imag < max_y:
                for d in directions:
                    if cur + d not in rocks and (cur + d).imag < max_y:
                        cur += d
                        break
                else:
                    can_move = False
                if grain == 4:
                    for d in directions:
                        # print(f"{cur=} {cur+d=} {cur+d in rocks}")
                        pass
            if cur == complex(500, 0):
                return grain + 1
            # print(f"{grain=} landed at {cur}")
            rocks.add(cur)

    def line_parser(self, line: str):
        out = []
        for pair in line.split(" -> "):
            x, y = pair.split(",")
            out.append(complex(int(x), int(y)))
        return out



if __name__ == "__main__":
    typer.run(Day14().run)

# vim:expandtab:sw=4:ts=4
