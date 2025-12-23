#!/bin/python
"""Advent of Code, Day 11: Plutonian Pebbles."""
import functools


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


def solve(data: list[int], part: int) -> int:
    steps = 25 if part == 1 else 75
    return sum(count_stone(stone, steps) for stone in data)


TESTS = [(1, "125 17", 55312), (2, "125 17", 65601038650482)]
# vim:expandtab:sw=4:ts=4
