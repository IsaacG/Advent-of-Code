#!/bin/python
"""Advent of Code, Day 5: How About a Nice Game of Chess?."""
from __future__ import annotations

import collections
import functools
import hashlib
import itertools
import math
import re

from lib import aoc

InputType = str


class Day05(aoc.Challenge):
    """Day 5: How About a Nice Game of Chess?."""

    TESTS = [
        aoc.TestCase(inputs="abc", part=1, want="18f47a30"),
        aoc.TestCase(inputs="abc", part=2, want="05ace8e3"),
    ]

    INPUT_PARSER = aoc.parse_one_str

    def hash_gen(self, name: str) -> Generator[str, None, None]:
        base = hashlib.md5(name.encode())
        for i in itertools.count():
            md5 = base.copy()
            md5.update(str(i).encode())
            digest = md5.hexdigest()
            if digest.startswith("00000"):
                yield digest

    def part1(self, parsed_input: InputType) -> int:
        gen = self.hash_gen(parsed_input)
        return "".join(next(gen)[5] for _ in range(8))

    def part2(self, parsed_input: InputType) -> int:
        gen = self.hash_gen(parsed_input)
        out = {}
        while len(out) < 8:
            digest = next(gen)
            pos, char = digest[5:7]
            if pos.isdigit() and int(pos) < 8 and int(pos) not in out:
                out[int(pos)] = char
        return "".join(out[i] for i in range(8))
