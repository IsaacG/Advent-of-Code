#!/bin/python
"""Advent of Code, Day 19: Tractor Beam."""

import collections

import intcode
from lib import aoc


class Day19(aoc.Challenge):
    """Day 19: Tractor Beam."""

    TESTS = [
        aoc.TestCase(part=1, inputs="", want=aoc.TEST_SKIP),
        aoc.TestCase(part=2, inputs="", want=aoc.TEST_SKIP),
    ]
    INPUT_PARSER = aoc.parse_one_str

    def is_on(self, computer, x: int, y: int) -> bool:
        """Return if a given coordinate is on."""
        computer.reset()
        computer.input.extend([x, y])
        computer.run()
        return computer.output.pop() == 1

    def part1(self, puzzle_input: str) -> int:
        computer = intcode.Computer(puzzle_input, debug=self.DEBUG)
        total = 0
        left, right, last_y = 0, 0, 0
        for y in range(50):
            # s = sum(self.is_on(puzzle_input, x, y) for x in range(50))
            first = next(
                (
                    x
                    for x in range(left, min(50, left + 3 + y - last_y))
                    if self.is_on(computer, x, y)
                ), None
            )
            if first is None:
                continue
            last_y = y
            left = first
            right = max(right, left)
            right = next(
                (
                    x for x in range(right, min(50, right + 5))
                    if not self.is_on(computer, x, y)
                ),
                50,
            ) - 1
            count = right - left + 1
            # assert s == count, f"{s=}, {count=}, {y=}"
            total += count
        return total

    def part2(self, puzzle_input: str) -> int:
        computer = intcode.Computer(puzzle_input, debug=self.DEBUG)
        left, right = 10, 10
        prior: collections.deque[tuple[int, int]] = collections.deque()
        for y in range(10, 100000):
            left = next(x for x in range(left, left + 3) if self.is_on(computer, x, y))
            right = max(right, left)
            right = next(x for x in range(right, right + 5) if not self.is_on(computer, x, y))
            prior.append((y, right))
            if len(prior) == 100:
                prior_y, prior_right = prior.popleft()
                if left + 100 <= prior_right:
                    return left * 10000 + prior_y
        raise RuntimeError("No solution found.")

# vim:expandtab:sw=4:ts=4
