#!/bin/python
"""Advent of Code, Day 13: Distress Signal. Sort packets of types int and nested lists."""

import functools
import json
import math
from typing import Any

from lib import aoc


# cmp for integers.
int_cmp = aoc.cmp


def cmp(first: Any, second: Any) -> int:
    """Compare two values and return -1|0|1.

    if first  < second: -1
    if first == second:  0
    if first  > second: +0
    """
    match [first, second]:
        case [int(), int()]:
            return int_cmp(first, second)
        case [list(), list()]:
            for i, j in zip(first, second):
                result = cmp(i, j)
                if result:
                    return result
            return int_cmp(len(first), len(second))
        case [list(), int()]:
            return cmp(first, [second])
        case [int(), list()]:
            return cmp([first], second)
    raise ValueError(f"Umatched {first} {second}")


PARSER = aoc.ParseBlocks([aoc.ParseOneWordPerLine(json.loads)])

def solve(data: list[list[Any]], part: int) -> int:
    """Return the number of pairs which are in order."""
    pairs = data
    if part == 1:
        return sum(
            idx
            for idx, (fst, snd) in enumerate(pairs, start=1)
            if cmp(fst, snd) == -1
        )

    pairs = data
    dividers = ([[2]], [[6]])
    vals = list(dividers)
    for pair in pairs:
        vals.extend(pair)
    vals.sort(key=functools.cmp_to_key(cmp))
    return math.prod(vals.index(divider) + 1 for divider in dividers)


SAMPLE = """\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""
TESTS = [(1, SAMPLE, 13), (2, SAMPLE, 140)]
