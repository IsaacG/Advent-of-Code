#!/bin/python
"""Advent of Code, Day 24: Electromagnetic Moat."""


def strongest(start: int, options: set[tuple[int, ...]]) -> tuple[int, int, int]:
    """Return the strongest combination."""
    strength = 0
    longest_length = 0
    longest_strength = 0

    for option in options:
        if start not in option:
            continue
        cur = option[0] + option[1]
        next_start = cur - start
        n_str, n_len, n_long_str = strongest(next_start, options - {option})
        strength = max(strength, n_str + cur)
        n_long_str += cur
        if n_len > longest_length:
            longest_length = n_len
            longest_strength = n_long_str
        elif n_len == longest_length and n_long_str > longest_strength:
            longest_strength = n_long_str
    return strength, longest_length + 1, longest_strength


def solve(data: list[list[int]], part: int) -> int:
    """Compute the strongest (longest) magnetic bridge which can be built."""
    bridges = {tuple(i) for i in data}
    return strongest(0, bridges)[0 if part == 1 else 2]


SAMPLE = """\
0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10"""
TESTS = [(1, SAMPLE, 31), (2, SAMPLE, 19)]
# vim:expandtab:sw=4:ts=4
