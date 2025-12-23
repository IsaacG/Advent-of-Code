#!/bin/python
"""Advent of Code: Day 02. Track the location of the submarine as it moves about."""


def solve(data: list[tuple[str, int]], part: int) -> int:
    """Compute the submarine's horizontal position, depth and aim."""
    horiz, depth, aim = 0, 0, 0
    for direction, num in data:
        if direction == "forward":
            horiz += num
            if part == 2:
                depth += aim * num
        else:
            if direction == "up":
                num = -num
            if part == 1:
                depth += num
            else:
                aim += num

    return depth * horiz


SAMPLE = """\
forward 5
down 5
forward 8
up 3
down 8
forward 2
"""
TESTS = [(1, SAMPLE, 150), (2, SAMPLE, 900)]
