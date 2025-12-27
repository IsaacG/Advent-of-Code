#!/bin/python
"""Advent of Code, ${title}."""
from __future__ import annotations

import collections
import functools
import itertools
import logging
import math
import re

from lib import aoc

InputType = list[list[str]]
log = logging.info

DEBUG = True
# Default is True. On live solve, submit one tests pass.
# SUBMIT = {1: False, 2: False}
# PARSER = aoc.parse_ints
# PARSER = str
# PARSER = str.splitlines
# PARSER = aoc.parse_multi_str_per_line
# PARSER = int
# PARSER = aoc.parse_one_int_per_line
# PARSER = aoc.parse_ints_one_line
# PARSER = aoc.parse_ints_per_line
# PARSER = aoc.parse_re_group_str(r"(a) .* (b) .* (c)")
# PARSER = aoc.parse_re_findall_str(r"(a|b|c)")
# PARSER = aoc.parse_multi_mixed_per_line
# PARSER = aoc.parse_re_group_mixed(r"(foo) .* (\d+)")
# PARSER = aoc.parse_re_findall_mixed(r"\d+|foo|bar")
# PARSER = aoc.ParseBlocks([aoc.parse_one_str_per_line, aoc.parse_re_findall_int(r"\d+")])
# PARSER = aoc.ParseOneWord(aoc.Board.from_int_block)
# PARSER = aoc.CoordinatesParser(chars=None, origin_top_left=True)
# max_x, max_y = width - 1, height - 1


def solve(data: InputType, part: int) -> int:
    print("\n".join(["==="] + [f"{k}={v!r}" for k, v in locals().items()] + ["==="]))
    # return (part1 if part == 1 else part2)(data)
    return None


# def part1(data: InputType) -> int:
# def part2(data: InputType) -> int:


def xinput_parser(self, data: str) -> InputType:
    """Parse the input data."""
    return data.splitlines()
    return data
    return [int(i) for i in data.splitlines()]
    mutate = lambda x: (x[0], int(x[1])) 
    return [mutate(line.split()) for line in data.splitlines()]
    # Words: mixed str and int
    return [
        tuple(
            int(i) if i.isdigit() else i
            for i in line.split()
        )
        for line in data.splitlines()
    ]
    # Regex splitting
    patt = re.compile(r"(.*) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.")
    return [
        tuple(
            int(i) if i.isdigit() else i
            for i in patt.match(line).groups()
        )
        for line in data.splitlines()
    ]

SAMPLE = """\
"""
TESTS = [
    (1, SAMPLE[0], None),
    (2, SAMPLE[0], None),
]
# vim:expandtab:sw=4:ts=4
