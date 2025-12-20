#!/bin/python
"""Advent of Code, Day 5: A Maze of Twisty Trampolines, All Alike."""


def solve(data: list[int], part: int) -> int:
    """Count how many steps of jumps it takes to exit the memory."""
    mem = data
    size = len(mem)
    ptr = 0

    step = 0
    while 0 <= ptr < size:
        offset = mem[ptr]
        mem[ptr] += -1 if part == 2 and offset >= 3 else 1
        ptr += offset
        step += 1
    return step


TESTS = [(1, "0\n3\n0\n1\n-3", 5), (2, "0\n3\n0\n1\n-3", 10)]
# vim:expandtab:sw=4:ts=4
