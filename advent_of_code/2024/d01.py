#!/bin/python
"""Advent of Code, Day 1: Historian Hysteria."""


def solve(data: list[list[int]], part: int) -> int:
    """Return the similarity between two lists."""
    a, b = (sorted(line) for line in zip(*data))
    if part == 1:
        return sum(abs(i - j) for i, j in zip(a, b))
    return sum(i * b.count(i) for i in a)


SAMPLE = """\
3   4
4   3
2   5
1   3
3   9
3   3"""
TESTS = [(1, SAMPLE, 11), (2, SAMPLE, 31)]
# vim:expandtab:sw=4:ts=4
