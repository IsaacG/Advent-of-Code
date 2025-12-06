#!/bin/python
"""Advent of Code, Day 6: Trash Compactor."""
from lib import aoc

SAMPLE = """\
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +"""


class Day06(aoc.Challenge):
    """Day 6: Trash Compactor."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=4277556),
        aoc.TestCase(part=2, inputs=SAMPLE, want=3263827),
    ]
    INPUT_PARSER = aoc.parse_one_str

    def part1(self, puzzle_input: str) -> int:
        """Return the answer for the math homework."""
        *lines, operators = [line.split() for line in puzzle_input.splitlines()]
        numbers = [[int(i) for i in line] for line in lines]
        transposed = zip(*numbers)
        return sum(
            aoc.LIST_OPS[op](nums)
            for nums, op in zip(transposed, operators)
        )

    def part2(self, puzzle_input: str) -> int:
        """Return the answer for the math homework."""
        *nums, ops = puzzle_input.splitlines()
        longest_line = max(len(i) for i in puzzle_input.splitlines())
        starts = [idx for idx, char in enumerate(ops) if char != " "] + [longest_line + 1]
        operators = ops.split()

        total = 0
        for start, end, op in zip(starts, starts[1:], operators):
            # Collect all columns.
            numbers = [
                int(
                    # Collect all lines for one column.
                    "".join(
                        line[col] for line in nums if line[col] != " "
                    )
                )
                for col in range(start, end - 1)
            ]
            total += aoc.LIST_OPS[op](numbers)
        return total

# vim:expandtab:sw=4:ts=4
