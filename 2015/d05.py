#!/bin/python
"""Advent of Code: Day 05."""

from lib import aoc

SAMPLE = """\
ugknbfddgicrmopn
aaa
jchzalrnumimnmhp
haegwjzuvuyypxyu
dvszwmarrgswjxmb
qjhvhtzxzqqjkmpb
xxyxx
uurcxstgmygtbstg
ieodomkazucvgmuy""".splitlines()

InputType = list[str]
VOWELS = set("aeiou")
BAD = {"ab", "cd", "pq", "xy"}


class Day05(aoc.Challenge):
    """Day 5: Doesn't He Have Intern-Elves For This?. Classify strings as naughty or nice."""

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=1),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=1),
        aoc.TestCase(inputs=SAMPLE[2], part=1, want=0),
        aoc.TestCase(inputs=SAMPLE[3], part=1, want=0),
        aoc.TestCase(inputs=SAMPLE[4], part=1, want=0),
        aoc.TestCase(inputs=SAMPLE[5], part=2, want=1),
        aoc.TestCase(inputs=SAMPLE[6], part=2, want=1),
        aoc.TestCase(inputs=SAMPLE[7], part=2, want=0),
        aoc.TestCase(inputs=SAMPLE[8], part=2, want=0),
    )

    def part1(self, puzzle_input: InputType) -> int:
        """Return how many lines follow rules 1."""
        total = 0
        for line in puzzle_input:
            if (
                sum(True for i in line if i in VOWELS) >= 3
                and all(b not in line for b in BAD)
                and any(a == b for a, b in zip(line, line[1:]))
            ):
                total += 1
        return total

    def part2(self, puzzle_input: InputType) -> int:
        """Return how many lines follow rules 2."""
        total = 0
        for line in puzzle_input:
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
