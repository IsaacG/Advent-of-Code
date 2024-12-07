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
            options = {numbers[0]}
            for number in numbers[1:]:
                next_options = {option + number for option in options}
                next_options |= {option * number for option in options}
                if not part_one:
                    next_options |= {int(str(option) + str(number)) for option in options}
                options = {o for o in next_options if o <= result}
            return result in options

        return sum(
            result
            for result, *numbers in puzzle_input
            if valid(result, numbers)
        )

# vim:expandtab:sw=4:ts=4
