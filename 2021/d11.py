#!/bin/python
"""Advent of Code: Day 11."""

from lib import aoc

SAMPLE = ["""\
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
"""]


class Day11(aoc.Challenge):
    """Count the flashing octopuses."""

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=1656),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=195),
    )

    def step(self, octopuses: dict[complex, int]) -> dict[complex, int]:
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
            for neighbor in aoc.neighbors(point, directions=aoc.EIGHT_DIRECTIONS):
                if neighbor not in octopuses:
                    continue
                new[neighbor] += 1
                if new[neighbor] == 10:
                    to_flash.add(neighbor)
        # Reset flashed octopuses to 0.
        new.update({point: 0 for point in flashed})
        return new

    def part1(self, puzzle_input: aoc.Map) -> int:
        """Count how many octopuses flash after 100 steps."""
        octopuses = puzzle_input.chars
        flashes = 0
        for _ in range(100):
            octopuses = self.step(octopuses)
            flashes += sum(1 for v in octopuses.values() if v == 0)
        return flashes

    def part2(self, puzzle_input: aoc.Map) -> int:
        """Count how many steps until all the octopuses flashed in the same step."""
        octopuses = puzzle_input.chars
        # Stop after a bunch of steps, just in case this isn't working.
        for step in range(1, 5000):
            octopuses = self.step(octopuses)
            if all(v == 0 for v in octopuses.values()):
                return step
        raise RuntimeError("Could not solve in allocated steps.")
