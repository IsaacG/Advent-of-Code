#!/bin/python
"""Advent of Code: Day 06. Tuning Trouble. Parse data streams to find the start of messages."""


def solve(data: str, part: int) -> int:
    """Return the offset *after* a series of n different chars."""
    num = 4 if part == 1 else 14
    parts = (data[i:] for i in range(num))
    return next(
        offset + num
        for offset, chars in enumerate(zip(*parts))
        if len(set(chars)) == num
    )


TESTS = [
    (1, "bvwbjplbgvbhsrlpgdmjqwftvncz", 5),
    (1, "nppdvjthqldpwncqszvftbrmjlhg", 6),
    (1, "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10),
    (1, "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11),
    (2, "mjqjpqmgbljsphdztnvjfqwrcgsmlb", 19),
]
