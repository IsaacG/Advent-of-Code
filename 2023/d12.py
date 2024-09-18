#!/bin/python
"""Advent of Code, Day 12: Hot Springs."""

import functools
from lib import aoc

SAMPLE = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""


class Day12(aoc.Challenge):
    """Day 12: Hot Springs."""

    INPUT_PARSER = aoc.parse_one_str_per_line
    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=21),
        aoc.TestCase(inputs=SAMPLE, part=2, want=525152),
    ]

    @functools.cache
    def ways_to_fit(self, springs: tuple[str, ...], numbers: tuple[int, ...]) -> int:
        """Return the ways springs can fit."""
        if not numbers:
            # If we are out of numbers, check for known springs.
            # If there are known springs, this is not a match.
            # If there are only "?" then this is one match.
            return 0 if any("#" in group for group in springs) else 1

        # Remove any leading ??? groups which are too small to match.
        while springs and len(springs[0]) < numbers[0] and "#" not in springs[0]:
            springs = springs[1:]

        if not springs:
            # Ran out of spring groups but have more numbers. Cannot match.
            return 0
        if "#" in springs[0] and len(springs[0]) < numbers[0]:
            # The first group is too small but must match. This is not a match.
            return 0

        first_group = springs[0]
        first_num = numbers[0]
        count = 0
        # Count possible matches with the first ? being a .
        if springs[0].startswith("?"):
            skip_start = (springs[0][1:],) + springs[1:]
            count += self.ways_to_fit(skip_start, numbers)

        # Count possible matches with the first ? being a #
        if len(first_group) == first_num:
            count += self.ways_to_fit(springs[1:], numbers[1:])
        elif len(first_group) > first_num and first_group[first_num] == "?":
            at_start = (first_group[first_num + 1:],) + springs[1:]
            count += self.ways_to_fit(at_start, numbers[1:])

        return count

    def solver(self, puzzle_input: str, part_one: bool) -> int:
        """Return the total number of possible fits."""
        count = 0
        for line in puzzle_input:
            springs_str, numbers_str = line.split()
            if not part_one:
                springs_str = "?".join([springs_str] * 5)
                numbers_str = ",".join([numbers_str] * 5)
            springs = tuple(i for i in springs_str.split(".") if i)
            numbers = tuple(int(i) for i in numbers_str.split(","))
            count += self.ways_to_fit(springs, numbers)
        return count


# vim:expandtab:sw=4:ts=4
