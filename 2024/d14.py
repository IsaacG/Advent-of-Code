#!/bin/python
"""Advent of Code, Day 14: Restroom Redoubt."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3""",  # 2
]

LineType = int
InputType = list[LineType]


class Day14(aoc.Challenge):
    """Day 14: Restroom Redoubt."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=12),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_ints_per_line

    def part1(self, puzzle_input: InputType) -> int:
        robots = []
        width, height = (11, 7) if self.testing else (101, 103)
        for px, py, vx, vy in puzzle_input:
            robots.append((complex(px, py), complex(vx, vy)))
        steps = 100
        half_width = (width - 1) // 2
        half_height = (height - 1) // 2
        final_pos = [pos + vel * steps for pos, vel in robots]
        final_pos = [complex(pos.real % width, pos.imag % height) for pos in final_pos]
        q = []
        q.append(sum(1 for robot in final_pos if robot.real < half_width and robot.imag < half_height))
        q.append(sum(1 for robot in final_pos if robot.real < half_width and robot.imag > half_height))
        q.append(sum(1 for robot in final_pos if robot.real > half_width and robot.imag < half_height))
        q.append(sum(1 for robot in final_pos if robot.real > half_width and robot.imag > half_height))
        res =  math.prod(q)
        print(q)
        if not self.testing:
            assert res != 224796000
        return res

    def part2(self, puzzle_input: InputType) -> int:
        pos = []
        vel = []
        width, height = (101, 103)
        for px, py, vx, vy in puzzle_input:
            pos.append(complex(px, py))
            vel.append(complex(vx, vy))
        dense_centers = []
        for step in range(10000):
            centered_y = sum(
                35 < p.real < 67
                for p in pos 
            )
            centered_x = sum(
                44 < p.imag < 78
                for p in pos 
            )
            if centered_x > 350 and centered_y > 300:
                dense_centers.append(step)
                print(step)
                print(aoc.render(set(pos)))
                print(step)
                print()
            pos = [p + v for p, v in zip(pos, vel)]
            pos = [complex(p.real % width, p.imag % height) for p in pos]

        if len(dense_centers) == 1:
            return dense_centers[0]
        raise RuntimeError("Did not solve")


    # def solver(self, puzzle_input: InputType, part_one: bool) -> int | str:

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return super().input_parser(puzzle_input)
        return puzzle_input.splitlines()
        return puzzle_input
        return [int(i) for i in puzzle_input.splitlines()]
        mutate = lambda x: (x[0], int(x[1])) 
        return [mutate(line.split()) for line in puzzle_input.splitlines()]
        # Words: mixed str and int
        return [
            tuple(
                int(i) if i.isdigit() else i
                for i in line.split()
            )
            for line in puzzle_input.splitlines()
        ]
        # Regex splitting
        patt = re.compile(r"(.*) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.")
        return [
            tuple(
                int(i) if i.isdigit() else i
                for i in patt.match(line).groups()
            )
            for line in puzzle_input.splitlines()
        ]

# vim:expandtab:sw=4:ts=4
