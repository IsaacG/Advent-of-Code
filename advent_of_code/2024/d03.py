#!/bin/python
"""Advent of Code, Day 3: Mull It Over."""

import re
PARSER = str


def solve(data: str, part: int) -> int:
    """Return the sum of all the multiplications."""
    data = data.replace("\n", " ")
    if part == 2:
        # Remove any don't()-do() pairs and any trailing don't().
        data = re.sub(r"don't\(\).*?(do\(\)|$)", "", data)
    return sum(
        int(a) * int(b)
        for a, b in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", data)
    )

SAMPLE = [
    'xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))',
    "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))",
]
TESTS = [(1, SAMPLE[0], 161), (2, SAMPLE[1], 48)]
# vim:expandtab:sw=4:ts=4
