#!/bin/python
"""Advent of Code, Day 14: Restroom Redoubt."""

import dataclasses
import itertools
import math
import operator


@dataclasses.dataclass
class Robot:

    pos_x: int
    pos_y: int
    vel_x: int
    vel_y: int
    wrap_x: int
    wrap_y: int

    def step(self, steps: int) -> None:
        self.pos_x = (self.pos_x + steps * self.vel_x) % self.wrap_x
        self.pos_y = (self.pos_y + steps * self.vel_y) % self.wrap_y


def solve(data: list[list[int]], part: int, testing: bool) -> int:
    """Simulate robots moving around."""
    width, height = (11, 7) if testing else (101, 103)
    robots = [
        Robot(pos_x=px, pos_y=py, vel_x=vx, vel_y=vy, wrap_x=width, wrap_y=height)
        for px, py, vx, vy in data
    ]

    if part == 1:
        for robot in robots:
            robot.step(100)
        half_width = (width - 1) // 2
        half_height = (height - 1) // 2
        counts = [
            sum(op_a(robot.pos_x, half_width) and op_b(robot.pos_y, half_height) for robot in robots)
            for op_a, op_b in itertools.product([operator.gt, operator.lt], repeat=2)
        ]
        return math.prod(counts)

    for step in range(10000):
        centered_x = sum(33 < robot.pos_x < 69 for robot in robots)
        centered_y = sum(40 < robot.pos_y < 80 for robot in robots)
        if centered_x > 175 and centered_y > 225:
            break
        for robot in robots:
            robot.step(1)
    for step in range(step, 10000, height):
        centered_y = sum(44 < robot.pos_y < 78 for robot in robots)
        centered_x = sum(35 < robot.pos_x < 67 for robot in robots)
        if centered_x > 300 and centered_y > 350:
            break
        for robot in robots:
            robot.step(height)

    return step


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
TESTS = [(1, SAMPLE, 12)]
# vim:expandtab:sw=4:ts=4
