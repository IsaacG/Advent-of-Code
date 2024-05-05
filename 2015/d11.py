#!/bin/python
"""Advent of Code: Day 11. Corporate Policy. Rotate passwords. Find next password which satisfies contraints."""

import string

from lib import aoc

SAMPLE = ["abcdefgh", "ghijklmn"]

InputType = str
NOT_ALLOWED = {
    string.ascii_lowercase.index(i) for i in "iol"
}


def parts(num: int) -> list[int]:
    """Return 8 places of base-26 values for a number."""
    num_parts = []
    for _ in range(8):
        num, remainder = divmod(num, 26)
        num_parts.append(remainder)
    num_parts.reverse()
    return num_parts


def valid(password: list[int]) -> bool:
    """Return if a password is valid."""
    # Invalid chars.
    if any(i in password for i in NOT_ALLOWED):
        return False
    # Three incremental numbers.
    if not any(
        password[i] + 2 == password[i + 1] + 1 == password[i + 2]
        for i in range(6)
    ):
        return False

    # Two non-overlapping pairs.
    pairs = 0
    i = 0
    while i < 7:
        if password[i] == password[i + 1]:
            i += 1
            pairs += 1
        i += 1
    return pairs > 1


class Day11(aoc.Challenge):
    """Day 11: Corporate Policy. Rotate passwords."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want="abcdffaa"),
        #aoc.TestCase(inputs=SAMPLE[1], part=1, want="ghjaabcc"),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want="abcdffbb"),
    ]

    def next_password(self, password: str) -> str:
        """Generate the next password."""
        # String to int
        num = 0
        for char in password:
            num *= 26
            num += string.ascii_lowercase.index(char)

        # Increment until valid.
        num += 1
        while not valid(parts(num)):
            num += 1

        # Int to string.
        password = "".join(string.ascii_lowercase[i] for i in parts(num))
        return password

    def part1(self, parsed_input: InputType) -> int:
        """Rotate once."""
        assert valid(parts(334140716))  # abcdffaa
        assert valid(parts(50460204602))  # ghjaabcc

        return self.next_password(parsed_input)

    def part2(self, parsed_input: InputType) -> int:
        """Rotate twice."""
        password = self.next_password(parsed_input)
        return self.next_password(password)
