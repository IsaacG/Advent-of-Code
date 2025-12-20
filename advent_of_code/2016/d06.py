#!/bin/python
"""Advent of Code, Day 6: Signals and Noise.

Extract the most and least common value from each column.
"""
import collections
from lib import aoc


def solve(data: list[str], part: int) -> str:
    """Return the most/least common character from data."""
    idx = 0 if part == 1 else -1
    return "".join(
        collections.Counter(col).most_common()[idx][0]
        for col in zip(*data)
    )


PARSER = aoc.parse_one_str_per_line
SAMPLE = """\
eedadn\ndrvtee\neandsr\nraavrd\n\
atevrs\ntsrnev\nsdttsa\nrasrtv\n\
nssdts\nntnada\nsvetve\ntesnvt\n\
vntsnd\nvrdear\ndvrsen\nenarar"""
TESTS = [(1, SAMPLE, "easter"), (2, SAMPLE, "advent")]
