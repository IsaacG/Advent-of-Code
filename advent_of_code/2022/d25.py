#!/bin/python
"""Advent of Code, Day 25: Full of Hot Air. Convert from base 4 to 10 and back again!"""

from lib import aoc

LineType = str
InputType = list[LineType]
DECODER = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
ENCODER = {v: k for k, v in DECODER.items()}


def encode(dec: int) -> str:
    """Return the SNAFU encoding of a number."""
    out = []
    while dec:
        dec, rem = divmod(dec, 5)
        if rem > 2:
            dec += 1
            rem -= 5
        out.append(ENCODER[rem])
    return "".join(reversed(out))


def decode(snafu: str) -> int:
    """Return the integer value of a SNAFU encoded number."""
    total = 0
    for char in snafu:
        total = total * 5 + DECODER[char]
    return total


def solve(data: InputType, part: int) -> str:
    """Return the SNAFU-encoded sum of SNAFU values."""
    del part
    return encode(sum(decode(line) for line in data))


SAMPLE = """\
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""
TESTS = [(1, SAMPLE, "2=-1=0")]
