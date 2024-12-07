#!/bin/python
"""Advent of Code, Bridge Repair."""

from lib import aoc

SAMPLE = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""


class Day07(aoc.Challenge):
    """Bridge Repair."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=3749),
        aoc.TestCase(part=2, inputs=SAMPLE, want=11387),
    ]
    INPUT_PARSER = aoc.parse_ints

    def solver(self, puzzle_input: list[list[int]], part_one: bool) -> int | str:
        """Return the results of the valid equations."""

        def valid(result: int, numbers: list[int]) -> bool:
            """Return if the numbers can give the result."""
            if len(numbers) == 1:
                return result == numbers[0]
            # Small optimization. Numbers never decrease. If the first number is too big, abort.
            if result < numbers[0]:
                return False
            return (
                valid(result, [numbers[0] + numbers[1]] + numbers[2:])
                or valid(result, [numbers[0] * numbers[1]] + numbers[2:]) 
                or (not part_one and valid(result, [int(str(numbers[0]) + str(numbers[1]))] + numbers[2:]))
            )

        return sum(
            result
            for result, *numbers in puzzle_input
            if valid(result, numbers)
        )

# vim:expandtab:sw=4:ts=4
