#!/bin/python
"""Advent of Code, Day 1: Trebuchet?!."""

from lib import aoc

SAMPLE = [
    """\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet""",
    """\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen""",
]

NUMBER_WORDS = "one two three four five six seven eight nine"
WORDS = {
    word: str(index)
    for index, word in enumerate(NUMBER_WORDS.split(), start=1)
}


class Day01(aoc.Challenge):
    """Day 1: Trebuchet?!. Find numbers in a string."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=142),
        aoc.TestCase(inputs=SAMPLE[1], part=2, want=281),
        aoc.TestCase(inputs="eightwo", part=2, want=82),
        aoc.TestCase(inputs="hczrldvxffninemzbhsv2two5eightwozfh", part=2, want=92),
    ]

    def solver(self, puzzle_input: list[str], part_one: bool) -> int:
        """Walk a string and extract numbers."""
        total = 0
        for line in puzzle_input:
            numbers = []
            for i in range(len(line)):
                if line[i:i + 1].isdigit():
                    numbers.append(line[i:i + 1])
                elif not part_one:  # Part 2
                    for word, value in WORDS.items():
                        if line[i:].startswith(word):
                            numbers.append(value)
            first_last = f"{numbers[0]}{numbers[-1]}"
            total += int(first_last)
        return total

# vim:expandtab:sw=4:ts=4
