#!/bin/python
"""Advent of Code, Day 23: Safe Cracking. Simulate a computer."""
import assembunny


def solve(data: list[list[str | int]], part: int) -> int:
    """Simulate a computer."""
    computer = assembunny.Assembunny(data)
    return computer.run(register_a=7 if part == 1 else 12)[0]


SAMPLE = """\
cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a"""
TESTS = [(1, SAMPLE, 3)]
