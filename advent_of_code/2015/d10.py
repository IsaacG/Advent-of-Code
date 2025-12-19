#!/bin/python
"""Advent of Code: Day 10, Day 10: Elves Look, Elves Say. Run a look-say algorithm."""

import functools

from lib import aoc


@functools.cache
def look_say(string: str) -> str:
    """Return a look-say version of a string."""
    str_len = len(string)
    # Reduce large inputs to take advantage of caching.
    # Find a split point between differing chars.
    if str_len > 15:
        split = str_len // 2
        while split > 3:
            if string[split - 1] == string[split]:
                split -= 1
            else:
                return look_say(string[:split]) + look_say(string[split:])

    out: list[str] = []
    count = 0
    prior = string[0]
    for char in string:
        if char == prior:
            count += 1
        else:
            out.extend((str(count), prior))
            prior = char
            count = 1
    out.extend((str(count), prior))
    return "".join(out)


def solve(data: str, part: int, *, testing: bool) -> int:
    """Return look-say length after looping."""
    steps = 40 if part == 1 else 50
    for _ in range(5 if testing else steps):
        data = look_say(data)
        # data = "".join(f"{len(list(b))}{a}" for a, b in itertools.groupby(data))
    return len(data)


PARSER = aoc.parse_one_str
TESTS = [(1, "1", 6), (2, "1", 6)]
