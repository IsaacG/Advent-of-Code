#!/bin/python
"""Advent of Code, Day 5: How About a Nice Game of Chess?."""

import functools
import hashlib
import itertools
from collections import abc

from lib import aoc

InputType = str


class Day05(aoc.Challenge):
    """Day 5: How About a Nice Game of Chess?."""

    TESTS = [
        aoc.TestCase(inputs="abc", part=1, want="18f47a30"),
        aoc.TestCase(inputs="abc", part=2, want="05ace8e3"),
    ]
    TIMEOUT = 60

    def hash_gen(self, name: str) -> abc.Generator[str, None, None]:
        """Generate MD5 digests which start with 00000."""
        base = hashlib.md5(name.encode())
        for i in itertools.count():
            md5 = base.copy()
            md5.update(str(i).encode())
            digest = md5.hexdigest()
            if digest.startswith("00000"):
                yield digest

    @functools.cache
    def digest_gen(self, name: str) -> aoc.CachedIterable:
        """Return a CachedIterable which generates digests."""
        return aoc.CachedIterable(self.hash_gen(name))

    def part1(self, parsed_input: InputType) -> str:
        """Return a door code using the first 8 digests."""
        gen = iter(self.digest_gen(parsed_input))
        return "".join(next(gen)[5] for _ in range(8))

    def part2(self, parsed_input: InputType) -> str:
        """Return a door code using position-aware digests."""
        gen = iter(self.digest_gen(parsed_input))
        out: dict[int, str] = {}
        while len(out) < 8:
            digest = next(gen)
            pos, char = digest[5:7]
            if pos.isdigit() and int(pos) < 8 and int(pos) not in out:
                out[int(pos)] = char
        return "".join(out[i] for i in range(8))
