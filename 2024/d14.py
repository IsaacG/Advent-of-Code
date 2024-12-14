#!/bin/python
"""Advent of Code, Day 14: Restroom Redoubt."""

import itertools
import math
import operator

from lib import aoc

SAMPLE = """\
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
p=9,5 v=-3,-3"""


class Day14(aoc.Challenge):
    """Day 14: Restroom Redoubt."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=12),
        aoc.TestCase(part=2, inputs=SAMPLE, want=aoc.TEST_SKIP),
    ]
    INPUT_PARSER = aoc.parse_ints_per_line

    def part1(self, puzzle_input: list[list[int]]) -> int:
        """Simulate robots for 100 steps."""
        robots = []
        width, height = (11, 7) if self.testing else (101, 103)
        for px, py, vx, vy in puzzle_input:
            robots.append((complex(px, py), complex(vx, vy)))
        steps = 100
        half_width = (width - 1) // 2
        half_height = (height - 1) // 2
        final_pos = [pos + vel * steps for pos, vel in robots]
        final_pos = [complex(pos.real % width, pos.imag % height) for pos in final_pos]
        counts = [
            sum(op_a(robot.real, half_width) and op_b(robot.imag, half_height) for robot in final_pos)
            for op_a, op_b in itertools.product([operator.gt, operator.lt], repeat=2)
        ]
        return math.prod(counts)

    def part2(self, puzzle_input: list[list[int]]) -> int:
        """Simulate robots until an image is drawn."""
        pos = []
        vel = []
        width, height = (101, 103)
        skip_steps = 7000
        for px, py, vx, vy in puzzle_input:
            pos.append(complex(px + skip_steps * vx, py + skip_steps * vy))
            vel.append(complex(vx, vy))
        dense_centers = []
        for step in range(skip_steps, 8000):
            centered_y = sum(35 < p.real < 67 for p in pos)
            centered_x = sum( 44 < p.imag < 78 for p in pos)
            if centered_x > 350 and centered_y > 300:
                dense_centers.append(step)
                self.debug(aoc.render(set(pos)) + "\n")
            pos = [p + v for p, v in zip(pos, vel)]
            pos = [complex(p.real % width, p.imag % height) for p in pos]

        if len(dense_centers) == 1:
            return dense_centers[0]
        raise RuntimeError("Did not solve")

# vim:expandtab:sw=4:ts=4
