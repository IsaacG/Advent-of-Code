#!/bin/python
"""Advent of Code, Day 13: Claw Contraption."""
import math

from lib import aoc
PARSER = aoc.ParseBlocks([aoc.parse_ints])

def solve(data: list[list[int]], part: int) -> int:
    """Solved by linear algebra and a system of two equations with two unknowns.

    presses_a * a_x + presses_b * b_x = target_x  (1)
    presses_a * a_y + presses_b * b_y = target_y  (2)

    from (1)
    presses_b = (target_x - presses_a * a_x) / b_x  (3)
    from (2), substituting (3)
    presses_a * a_y + presses_b * b_y = target_y
    presses_a * a_y + ((target_x - presses_a * a_x) / b_x) * b_y = target_y
    presses_a = (target_y - (b_y * target_x / b_x)) / (a_y - (b_y * a_x / b_x))  (4)
    """
    tokens = 0
    for chunks in data:
        if part == 2:
            chunks[2] = [i + 10000000000000 for i in chunks[2]]
        a_x, a_y = chunks[0]
        b_x, b_y = chunks[1]
        target_x, target_y = chunks[2]

        presses_a = (target_y - (b_y * target_x / b_x)) / (a_y - (b_y * a_x / b_x))
        presses_b = (target_x - presses_a * a_x ) / b_x
        # Check the numbers are round integers ... or close enough.
        rounded_a = round(presses_a)
        rounded_b = round(presses_b)
        if abs(rounded_a - presses_a) > 0.001 or abs(rounded_b - presses_b) > 0.001:
            continue

        # assert rounded_a * a_x + rounded_b * b_x == target_x and rounded_a * a_y + rounded_b * b_y == target_y
        tokens += 3 * rounded_a + rounded_b
    return tokens


SAMPLE = """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""
TESTS = [(1, SAMPLE, 480)]
# vim:expandtab:sw=4:ts=4
