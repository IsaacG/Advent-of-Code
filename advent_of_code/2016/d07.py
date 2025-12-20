#!/bin/python
"""Advent of Code, Day 7: Internet Protocol Version 7. Detect line patterns."""

import re
import more_itertools

LineType = tuple[list[str], list[str]]
InputType = list[LineType]


def tls(string: str) -> bool:
    """Return if a string segment has a pattern ABBA."""
    it = more_itertools.sliding_window(string, 4)
    return any(a == d != b == c for a, b, c, d in it)


def ssl(outer: list[str], inner: list[str]) -> bool:
    """Return if inner and outer have a matching ABA, BAB."""
    patterns = [
        (chars[1] + chars[0] + chars[1])
        for chunk in inner
        for chars in more_itertools.sliding_window(chunk, 3)
        if chars[0] == chars[2] != chars[1]
    ]
    return any(pattern in chunk for chunk in outer for pattern in patterns)


def solve(data: InputType, part: int) -> int:
    """Return the number of lines with TLS/SSL patterns."""
    if part == 1:
        return sum(
            not any(tls(i) for i in inner)
            and any(tls(i) for i in outer)
            for outer, inner in data
        )
    return sum(ssl(*line) for line in data)


def input_parser(puzzle_input: str) -> InputType:
    """Parse the input data."""
    lines = []
    for line in puzzle_input.splitlines():
        parts = re.split(r"[][]", line)
        lines.append((parts[::2], parts[1::2]))
    return lines


SAMPLE = [
    """\
abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn""",
    "aba[bab]xyz\naba[bab]xyz",
    "aba[bab]xyz\naaa[kek]eke",
    "aba[bab]xyz\nzazbz[bzb]cdb",
    "aba[bab]xyz\nxyx[xyx]xyx",
]
TESTS = [
    (1, SAMPLE[0], 2),
    (2, SAMPLE[1], 2),
    (2, SAMPLE[2], 2),
    (2, SAMPLE[3], 2),
    (2, SAMPLE[4], 1),
]
