#!/bin/python
"""Advent of Code: Day 11. Count the flashing octopuses."""

import typing
from lib import aoc


def do_step(octopuses: dict[tuple[int, int], int]) -> tuple[dict[tuple[int, int], int], int]:
    """Apply one clock step to the octopuses."""
    # Add one energy to each octopus.
    new = {point: energy + 1 for point, energy in octopuses.items()}
    # Handle octopus flashing, updating neighbors as needed, until all
    # octopuses are done flashing.
    to_flash = set(point for point, energy in new.items() if energy == 10)
    flashed = set()
    while to_flash:
        point = to_flash.pop()
        flashed.add(point)
        for neighbor in aoc.t_neighbors8(point):
            if neighbor not in octopuses:
                continue
            new[neighbor] += 1
            if new[neighbor] == 10:
                to_flash.add(neighbor)
    # Reset flashed octopuses to 0.
    new.update({point: 0 for point in flashed})
    return new, len(flashed)


def solve(data: aoc.Map, part: int) -> int:
    """Count octopus flashes."""
    octopuses = typing.cast(dict[tuple[int, int], int], data.chars)
    num_octos = len(octopuses)
    flashes = 0

    for step in range(1, 5000):
        octopuses, flashed = do_step(octopuses)
        if part == 1:
            # Count total flashes after 100 steps.
            flashes += flashed
            if step == 100:
                return flashes
        elif flashed == num_octos:
            # Return step when all the octopuses flashed.
            return step
    raise RuntimeError("Could not solve in allocated steps.")


SAMPLE = """\
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""
TESTS = [(1, SAMPLE, 1656), (2, SAMPLE, 195)]
