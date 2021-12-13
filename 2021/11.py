#!/bin/python
"""Advent of Code: Day 11."""

import collections
import functools
import math
import re

import typer

from lib import aoc

InputType = dict[complex, int]
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

    DEBUG = True

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=1656),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=195),
    )


    @staticmethod
    def neighbors(octos: dict[complex, int], p: complex) -> list[complex]:
        points = [p + x + y * 1j for x in range(-1, 2) for y in range(-1, 2) if x or y]
        return [p for p in points if p in octos]
                
    def part1(self, lines: InputType) -> int:
        octos = lines
        flashes = 0
        for i in range(100):
            new = {p: v + 1 for p, v in octos.items()}
            to_flash = set(p for p, v in new.items() if v > 9)
            while to_flash:
                flashing = to_flash.pop()
                for n in self.neighbors(octos, flashing):
                    new[n] += 1
                    if new[n] == 10:
                        to_flash.add(n)
            octos = {p: v if v < 10 else 0 for p, v in new.items()}
            flashes += sum(1 for v in octos.values() if v == 0)
        return flashes

    def part2(self, lines: InputType) -> int:
        octos = lines
        for step in range(1, 500):
            new = {p: v + 1 for p, v in octos.items()}
            to_flash = set(p for p, v in new.items() if v > 9)
            while to_flash:
                flashing = to_flash.pop()
                for n in self.neighbors(octos, flashing):
                    new[n] += 1
                    if new[n] == 10:
                        to_flash.add(n)
            octos = {p: v if v < 10 else 0 for p, v in new.items()}
            if all(v == 0 for v in octos.values()):
                return step
        raise RuntimeError("Not found")

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        grid = [[int(e) for e in line] for line in puzzle_input.splitlines()]
        energy = {x + y * 1j: val for x, line in enumerate(grid) for y, val in enumerate(line)}
        return energy


if __name__ == "__main__":
    typer.run(Day11().run)

# vim:expandtab:sw=4:ts=4
