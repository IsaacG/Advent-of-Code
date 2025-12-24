#!/bin/python
"""Advent of Code, Day 1: Secret Entrance."""
from lib import aoc
PARSER = aoc.parse_re_group_mixed(r"([LR])(\d+)")


def solve(data: list[tuple[str, int]], part: int) -> int:
    """Return how many times the dial hits 0."""
    position = 50
    count = 0
    for direction, distance in data:
        step = 1 if direction == "R" else -1
        if part == 1:
            position += distance * step
            if position % 100 == 0:
                count += 1
        else:
            for _ in range(distance):
                position += step
                if position % 100 == 0:
                    count += 1
    return count


SAMPLE = "L68 L30 R48 L5 R60 L55 L1 L99 R14 L82".replace(" ", "\n")
TESTS = [(1, SAMPLE, 3), (2, SAMPLE, 6)]
# vim:expandtab:sw=4:ts=4
