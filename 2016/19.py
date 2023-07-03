#!/bin/python
"""Advent of Code, Day 19: An Elephant Named Joseph. Compute the winner of the Josephus problem."""

from lib import aoc


class Day19(aoc.Challenge):
    """Day 19: An Elephant Named Joseph."""

    TESTS = [
        aoc.TestCase(inputs="5", part=1, want=3),
        aoc.TestCase(inputs="5", part=2, want=2),
    ]

    def part1(self, parsed_input: int) -> int:
        """Solve the Josephus problem."""
        circle = list(range(parsed_input))
        while len(circle) > 1:
            odd = len(circle) % 2
            circle = circle[::2]
            if odd:
                circle = circle[1:]
        return circle[0] + 1

    def part2(self, parsed_input: int) -> int:
        """Solve a variation on the Josephus problem."""
        stop = parsed_input - 1

        size = 1
        while True:
            counter = 1
            while counter <= size // 2:
                if size == stop:
                    return counter
                size += 1
                counter += 1
            while counter <= size + 1:
                if size == stop:
                    return counter
                size += 1
                counter += 2
