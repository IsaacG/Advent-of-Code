#!/bin/python
"""Advent of Code, Day 17: Pyroclastic Flow. Compute the height of a Tetris-like rock pile after rocks have landed."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

import typer
from lib import aoc

ROCKS = [
    "####",
    """\
.#.
###
.#.""",
    """\
..#
..#
###""", """\
#
#
#
#""",
    """\
##
##"""
]
SAMPLE = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'


InputType = str


class Day17(aoc.Challenge):
    """Day 17: Pyroclastic Flow."""

    DEBUG = False
    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=3068),
        aoc.TestCase(inputs=SAMPLE, part=2, want=1514285714288),
    ]
    INPUT_PARSER = aoc.parse_one_str

    def solver(self, parsed_input: InputType, n) -> int:
        rocks = [
            {complex(0, 0), complex(1, 0), complex(2, 0), complex(3, 0)},
            {complex(1, 0), complex(0, 1), complex(1, 1), complex(2, 1), complex(1, 2)},
            {complex(0, 0), complex(1, 0), complex(2, 0), complex(2, 1), complex(2,2)},
            {complex(0, 0), complex(0, 1), complex(0, 2), complex(0, 3)},
            {complex(0, 0), complex(0, 1), complex(1, 0), complex(1, 1)},
        ]
        heights = [int(max(i.imag for i in r)) for r in rocks]
        stream_size = len(parsed_input)
        stream = parsed_input
        gravity = complex(0, -1)

        landed = set()
        height = 0
        seen = {}

        # SHOW = 20
        cycle_detection = None
        height_deltas = collections.deque([0] * 40)

        wind_idx = -1
        rock_cnt = -1

        while rock_cnt + 1 < n:
            rock_cnt += 1
            if rock_cnt and rock_cnt % 1000000 == 0:
                print(f"Step {rock_cnt}")
            rock_shape = rocks[rock_cnt % 5]
            bottom_left_corner = complex(2, height + 4)

            while True:
                wind_idx = (wind_idx + 1) % stream_size
                wind = -1 if stream[wind_idx] == "<" else +1
                o2 = wind + bottom_left_corner
                r2 = {r + o2 for r in rock_shape}
                if all(0 <= r.real < 7 for r in r2) and landed.isdisjoint(r2):
                    bottom_left_corner = o2

                o2 = gravity + bottom_left_corner
                r2 = {r + o2 for r in rock_shape}
                if all(0 < r.imag for r in r2) and landed.isdisjoint(r2):
                    bottom_left_corner = o2
                else:
                    break

            landed.update({bottom_left_corner + r for r in rock_shape})
            new_height = max(height, int(bottom_left_corner.imag) + heights[rock_cnt%5])
            height_deltas.append(new_height - height)
            height_deltas.popleft()
            height = new_height

            if all(complex(x, height) in landed for x in range(7)):
                t = ((((wind_idx) << 4) | (rock_cnt % 5)), tuple(height_deltas))
                if t not in seen:
                    seen[t] = (rock_cnt, height)
                else:
                    prior_rock_cnt, prior_height = seen[t]
                    self.debug(f"Cycle found {prior_rock_cnt, prior_height} -> {rock_cnt, height}.")

                    if True:
                        cycle_size = rock_cnt - prior_rock_cnt
                        height_diff = height - prior_height

                        cycle_count = (n - rock_cnt) // cycle_size
                        rock_cnt += cycle_count * cycle_size
                        height += cycle_count * height_diff
                        landed.update(complex(x, height) for x in range(7))


        return height

    def part1(self, parsed_input: InputType) -> int:
        return self.solver(parsed_input, 2022)

    def part2(self, parsed_input: InputType) -> int:
        return self.solver(parsed_input, 1000000000000)


if __name__ == "__main__":
    typer.run(Day17().run)

# vim:expandtab:sw=4:ts=4
