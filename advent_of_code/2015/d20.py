#!/bin/python
"""Advent of Code, Day 20: Infinite Elves and Infinite Houses."""
TESTS = [(1, "70", 4), (1, "130", 8)]


def solve(data: int, part: int) -> int:
    target = data // (10 if part == 1 else 11)

    limit = 1000000
    houses = [1] * limit
    for i in range(2, limit):
        stop = limit if part == 1 else min(limit, i * 51)
        for house in range(i, stop, i):
            houses[house] += i

    for i, num in enumerate(houses):
        if num >= target:
            return i

    raise RuntimeError
