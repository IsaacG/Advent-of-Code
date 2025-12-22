#!/usr/bin/env python
"""AoC Day 2: Password Philosophy."""

import re
RE = re.compile('^([0-9]+)-([0-9]+) (.): (.*)$')


def input_parser(text: str) -> list[tuple[int, int, str, str]]:
    """Parse the puzzle input."""
    data = []
    for line in text.splitlines():
        r = RE.match(line)
        assert r
        mn, mx, char, passwd = r.groups()
        data.append((int(mn), int(mx), char, passwd))
    return data


def solve(data: list[tuple[int, int, str, str]], part: int) -> int:
    """Count valid passwords."""
    if part == 1:
        return sum(
            mn <= len([1 for i in passwd if i == char]) <= mx
            for (mn, mx, char, passwd) in data
        )
    return sum(
        (passwd[mn - 1] == char) ^ (passwd[mx - 1] == char)
        for (mn, mx, char, passwd) in data
    )


SAMPLE = """\
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
"""
TESTS = [(1, SAMPLE, 2), (2, SAMPLE, 1)]
