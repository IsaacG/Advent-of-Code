#!/bin/python
"""Advent of Code, Day 5: A Maze of Twisty Trampolines, All Alike."""

from lib import aoc

SAMPLE = "0\n3\n0\n1\n-3"


class Day05(aoc.Challenge):
    """Day 5: A Maze of Twisty Trampolines, All Alike."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=5),
        aoc.TestCase(inputs=SAMPLE, part=2, want=10),
    ]

    def solver(self, puzzle_input: list[int], part_one: bool) -> int:
        """Count how many steps of jumps it takes to exit the memory."""
        mem = puzzle_input
        size = len(mem)
        ptr = 0

        step = 0
        while 0 <= ptr < size:
            offset = mem[ptr]
            mem[ptr] += -1 if not part_one and offset >= 3 else 1
            ptr += offset
            step += 1
        return step

# vim:expandtab:sw=4:ts=4
