#!/bin/python
"""Advent of Code, Day 1: Secret Entrance."""
from lib import aoc

SAMPLE = "L68 L30 R48 L5 R60 L55 L1 L99 R14 L82".replace(" ", "\n")


class Day01(aoc.Challenge):
    """Day 1: Secret Entrance."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=3),
        aoc.TestCase(part=2, inputs=SAMPLE, want=6),
    ]
    INPUT_PARSER = aoc.parse_re_group_mixed(r"([LR])(\d+)")

    def part1(self, puzzle_input: list[tuple[str, int]]) -> int:
        """Return how many times the dial stops at 0."""
        position = 50
        count = 0
        for direction, distance in puzzle_input:
            if direction == "L":
                distance *= -1
            position += distance
            position %= 100
            if position == 0:
                count += 1
        return count

    def part2(self, puzzle_input: list[tuple[str, int]]) -> int:
        """Return how many times the dial passes 0."""
        position = 50
        count = 0
        for direction, distance in puzzle_input:
            step = 1 if direction == "R" else -1
            for _ in range(distance):
                position += step
                if position % 100 == 0:
                    count += 1
        return count

# vim:expandtab:sw=4:ts=4
