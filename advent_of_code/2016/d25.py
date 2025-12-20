#!/bin/python
"""Advent of Code, Day 25: Clock Signal. Find the starting value which generates a clock signal."""
import itertools
import assembunny
TESTS = list[tuple[int, int, int]]()


def solve(data: list[list[str | int]]) -> int:
    """Find the starting value which generates a clock signal."""
    computer = assembunny.Assembunny(data)
    return next(
        i for i in itertools.count(start=0)
        if computer.run(register_a=i)[1]
    )
