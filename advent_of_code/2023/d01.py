#!/bin/python
"""Advent of Code, Day 1: Trebuchet?! Find numbers in a string."""
NUMBER_WORDS = "one two three four five six seven eight nine"
WORDS = {
    word: str(index)
    for index, word in enumerate(NUMBER_WORDS.split(), start=1)
}


def solve(data: list[str], part: int) -> int:
    """Walk a string and extract numbers."""
    total = 0
    for line in data:
        numbers = []
        for i in range(len(line)):
            if line[i:i + 1].isdigit():
                numbers.append(line[i:i + 1])
            elif part == 2:  # Part 2
                for word, value in WORDS.items():
                    if line[i:].startswith(word):
                        numbers.append(value)
        first_last = f"{numbers[0]}{numbers[-1]}"
        total += int(first_last)
    return total


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
TESTS = [
    (1, SAMPLE[0], 142),
    (2, SAMPLE[1], 281),
    (2, "eightwo", 82),
    (2, "hczrldvxffninemzbhsv2two5eightwozfh", 92),
]
# vim:expandtab:sw=4:ts=4
