#!/bin/python
"""Advent of Code, Day 19: Medicine for Rudolph."""

import re


def part1(puzzle_input: tuple[list[list[str]], str]) -> int:
    mappings, start = puzzle_input
    found = set()
    length = len(start)
    for a, _, b in mappings:
        for x in range(length):
            if start[x:].startswith(a):
                found.add(start[:x] + b + start[x + len(a):])
    return len(found)


def part2(puzzle_input: tuple[list[list[str]], str]) -> int:
    _, start = puzzle_input
    elements = re.findall(r"[A-Z][a-z]*", start)
    num_elements = len(elements)
    parens = elements.count("Rn") + elements.count("Ar")
    commas = elements.count("Y")
    # https://www.reddit.com/r/adventofcode/comments/3xflz8/comment/cy4etju/
    return num_elements - parens - 2 * commas - 1


def solve(data, part: int) -> int:
    return part1(data) if part == 1 else part2(data)


SAMPLE = [
    """\
H => HO
H => OH
O => HH

HOH""",
    """\
H => HO
H => OH
O => HH

HOHOHO""", """\
e => H
e => O
H => HO
H => OH
O => HH

HOH""", """\
e => H
e => O
H => HO
H => OH
O => HH

HOHOHO"""
]


TESTS = [
    (1, SAMPLE[0], 4),
    (1, SAMPLE[1], 7),
    # (2, SAMPLE[2], 3),
    # (2, SAMPLE[3], 6),
]
