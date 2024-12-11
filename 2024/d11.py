#!/bin/python
"""Advent of Code, Day 11: Plutonian Pebbles."""
from __future__ import annotations

import functools
from lib import aoc

SAMPLE = "125 17"


@functools.cache
def count_stone(stone: int, steps: int) -> int:
    """Count how many stones one stone turns into after steps."""
    if steps == 0:
        return 1
    if stone == 0:
        return count_stone(1, steps - 1)
    stone_str = str(stone)
    stone_len = len(stone_str)
    if stone_len % 2:
        return count_stone(stone * 2024, steps - 1)
    div = 10 ** (stone_len // 2)
    return count_stone(stone // div, steps - 1) + count_stone(stone % div, steps - 1)


class Day11(aoc.Challenge):
    """Day 11: Plutonian Pebbles."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=55312),
        aoc.TestCase(part=2, inputs=SAMPLE, want=aoc.TEST_SKIP),
    ]

    def solver(self, puzzle_input: list[int], part_one: bool) -> int:
        steps = 25 if part_one else 75
        return sum(count_stone(stone, steps) for stone in puzzle_input)

# vim:expandtab:sw=4:ts=4
