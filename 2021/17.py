#!/bin/python
"""Advent of Code: Day 17."""

import collections
import functools
import math
import re
import time

import typer
from lib import aoc

SAMPLE = "target area: x=20..30, y=-10..-5"
InputType = tuple[complex, complex]


class Day17(aoc.Challenge):

    DEBUG = True

    TESTS = (
        aoc.TestCase(inputs=SAMPLE, part=1, want=45),
        aoc.TestCase(inputs=SAMPLE, part=2, want=112),
    )

    def part1(self, parsed_input: InputType) -> int:
        x0, x1, y0, y1 = parsed_input
        seen = set()
        worked = []
        for x in range(300):
            for y in range(300):
                vel = x + y * 1j
                result, m = self.check_v(vel, x0, x1, y0, y1)
                if result == 0:
                    worked.append(m)

        return int(max(worked))


    def part2(self, parsed_input: InputType) -> int:
        x0, x1, y0, y1 = parsed_input
        seen = set()
        worked = []
        for x in range(x1 + 1):
            for y in range(y0, max(abs(y0), abs(y1)) + 1):
                vel = x + y * 1j
                result, m = self.check_v(vel, x0, x1, y0, y1)
                if result == 0:
                    worked.append(vel)

        return len(worked)


    def check_v(self,vel, x0, x1, y0, y1):
        pos = complex(0)
        step = 0
        ys = []
        while pos.real < x1:
            if step > 10000:
                break
            # time.sleep(0.0001)
            pos += vel
            ys.append(pos.imag)
            if vel.real > 0:
                vel -= 1
            elif vel.real < 0:
                vel += 1
            vel += -1j

            if x0 <= pos.real <= x1 and y0 <= pos.imag <= y1:
                return 0, max(ys)

            if vel.real == 0 and pos.imag < y0:
                break

            if vel.imag < 0 and pos.imag < y0:
                break

            step += 1
        if pos.real > x1:
            return -1, None
        if pos.real < x1:
            return 1, None
        return 1, None


    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        pattern = re.compile(r"target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)")
        match = pattern.match(puzzle_input)
        nums = [int(i) for i in match.groups()]
        return nums
        return complex(*nums[0:2]), complex(*nums[2:4])


if __name__ == "__main__":
    typer.run(Day17().run)

# vim:expandtab:sw=4:ts=4
