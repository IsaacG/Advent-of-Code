#!/bin/python
"""Advent of Code, Day 16: Aunt Sue. Find the aunt who matches the criteria."""

import operator
import collections.abc

from lib import aoc

InputType = list[dict[str, int]]
WANT_NUM = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}
OPS = {k: operator.eq for k in WANT_NUM}


@staticmethod
def matches(ops: dict[str, collections.abc.Callable], aunts: list[dict[str, int]]) -> int:
    """Return the aunt who matches the comparisons."""
    for i, aunt in enumerate(aunts, start=1):
        if all(ops[k](v, WANT_NUM[k]) for k, v in aunt.items()):
            return i
    raise RuntimeError("Not found.")


def solve(data: InputType, part: int) -> int:
    """Find the aunt who matches optionally with fuzzy rules."""
    ops = OPS
    if part == 2:
        ops |= {
            "cats": operator.gt,
            "trees": operator.gt,
            "goldfish": operator.lt,
            "pomeranians": operator.lt,
        }
    return matches(ops, data)


def input_parser(puzzle_input: str) -> InputType:
    """Parse the input data."""
    return [
        dict(
            (prop.split(": ")[0], int(prop.split(": ")[1]))
            for prop in line.split(": ", 1)[1].split(", ")
        )
        for line in puzzle_input.splitlines()
    ]


PARSER = aoc.ParseCustom(input_parser)
TESTS = []
