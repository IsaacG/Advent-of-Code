#!/bin/python
"""Advent of Code, Day 8: Treetop Tree House."""

import collections
import functools
import math
import re

import typer
from lib import aoc

SAMPLE = [
    """\
30373
25512
65332
33549
35390""",  # 0
]

LineType = int
InputType = list[LineType]


class Day08(aoc.Challenge):
    """Day 8: Treetop Tree House."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=21),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=8),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    # Convert lines to type:
    INPUT_TYPES = LineType
    # Split on whitespace and coerce types:
    # INPUT_TYPES = [str, int]
    # Apply a transform function
    # TRANSFORM = lambda _, l: (l[0], int(l[1:]))

    def part1(self, parsed_input: InputType) -> int:
        b = parsed_input
        all_points = set(b)
        visible = set()
        for i in range(b.height):
            visible.add(complex(0, i))
            visible.add(complex(b.width - 1, i))
        for i in range(b.width):
            visible.add(complex(i, 0))
            visible.add(complex(i, b.height - 1))

        directions = [complex(0, 1), complex(1, 0), complex(0, -1), complex(-1, 0)]

        todo = all_points - visible
        prior = len(visible)
        tocheck = set(visible)
        changed = True
        while tocheck and changed:
            to_add = set()
            changed = False
            for i in tocheck:
                for d in directions:
                    if i + d in visible or i + d in to_add:
                        continue
                    if i + d not in b:
                        continue
                    if b[i] >= b[i + d]:
                        continue
                    new_vis = True
                    cur = i
                    while cur in b:
                        if b[cur] >=  b[i + d]:
                            new_vis = False
                            break
                        cur -= d
                    if new_vis:
                        to_add.add(i + d)
                        changed = True
            tocheck = (all_points - visible) | to_add
            visible.update(to_add)


        return len(visible)

    def part2(self, parsed_input: InputType) -> int:
        b = parsed_input
        scores = []
        directions = [complex(0, 1), complex(1, 0), complex(0, -1), complex(-1, 0)]
        for i in b:
            s = []
            for d in directions:
                cur = i + d
                num = 0
                while cur in b:
                    num += 1
                    if b[cur] >= b[i]:
                        break
                    cur += d
                s.append(num)
            scores.append(self.mult(s))
        return max(scores)




    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return aoc.Board.from_int_block(puzzle_input)
        return puzzle_input.splitlines()
        return puzzle_input
        return [int(i) for i in puzzle_input.splitlines()]
        mutate = lambda x: (x[0], int(x[1])) 
        return [mutate(line.split()) for line in puzzle_input.splitlines()]
        patt = re.compile(r"(.*) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.")
        return [
            tuple(
                int(i) if i.isdigit() else i
                for i in patt.match(line).groups()
            )
            for line in puzzle_input.splitlines()
        ]


if __name__ == "__main__":
    typer.run(Day08().run)

# vim:expandtab:sw=4:ts=4
