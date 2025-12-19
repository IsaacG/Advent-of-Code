#!/bin/python
"""Advent of Code, Day 5: Doesn't He Have Intern-Elves For This? Classify strings as naughty or nice."""

from lib import aoc

VOWELS = set("aeiou")
BAD = {"ab", "cd", "pq", "xy"}


def solve(data: list[str], part: int) -> int:
    """Return how many lines follow rules 1 or 2."""
    total = 0
    for line in data:
        if part == 1:
            if (
                sum(True for i in line if i in VOWELS) >= 3
                and all(b not in line for b in BAD)
                and any(a == b for a, b in zip(line, line[1:]))
            ):
                total += 1
        else:
            repeated = False
            doubled = False
            for i in range(len(line) - 2):
                if not repeated and line[i:i + 2] in line[i + 2:]:
                    repeated = True
                if not doubled and line[i] == line[i+2]:
                    doubled = True
                if repeated and doubled:
                    total += 1
                    break
    return total


PARSER = aoc.parse_one_str_per_line
TESTS = [
    (1, "ugknbfddgicrmopn", 1),
    (1, "aaa", 1),
    (1, "jchzalrnumimnmhp", 0),
    (1, "haegwjzuvuyypxyu", 0),
    (1, "dvszwmarrgswjxmb", 0),
    (2, "qjhvhtzxzqqjkmpb", 1),
    (2, "xxyxx", 1),
    (2, "uurcxstgmygtbstg", 0),
    (2, "ieodomkazucvgmuy", 0),
]

