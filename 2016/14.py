#!/bin/python
"""Advent of Code, Day 14: One-Time Pad."""
from __future__ import annotations

import collections
import functools
import hashlib
import itertools
import math
import re

from lib import aoc


class Day14(aoc.Challenge):
    """Day 14: One-Time Pad."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs="abc", part=1, want=22728),
        aoc.TestCase(inputs="abc", part=2, want=22551),
    ]

    def hash_gen(self, name: str, stretch: bool) -> abc.Generator[str, None, None]:
        """Generate MD5 digests which start with triplets.

        >>> r = 'RE.match(s)'
        >>> z = 'any(a == b == c for a, b, c in zip(s, s[1:], s[2:]))'
        >>> timeit.timeit(r, setup='s = "asdfd3fewafewewerrrsddasfdas"; import re; RE = re.compile(r"(?P<a>)(?P=a)(?P=a)")')
        0.3939150311052799
        >>> timeit.timeit(z, setup='s = "asdfd3fewafewewerrrsddasfdas"')
        5.473389117047191
        """
        triplets = re.compile(r"(?P<a>.)(?P=a)(?P=a)")
        base = hashlib.md5(name.encode())
        for i in itertools.count():
            md5 = base.copy()
            md5.update(str(i).encode())
            digest = md5.hexdigest()
            if stretch:
                for _ in range(2016):
                    digest = hashlib.md5(digest.encode()).hexdigest()
            if m := triplets.search(digest):
                yield i, m.group(1), digest

    def solver(self, parsed_input: InputType, param: bool) -> int:
        triplets = re.compile(r"(?P<a>.)(?P=a)(?P=a)")
        gen = self.hash_gen(parsed_input, param)
        queue = collections.deque((next(gen) for _ in range(1001)), maxlen=1001)

        found = 0
        fi = False
        first = False
        for step in range(1_000_000):
            idx, char, candidate = queue.popleft()
            if not fi:
                fi = True
                print(idx, char, candidate)
            quints = char * 5
            # print(f"{char=}, {quints=}")
            queue.append(next(gen))
            if any(
                quints in digest
                for _, _, digest in itertools.takewhile(lambda x: x[0] <= idx + 1000, queue)
            ):
                found += 1
                if found == 64:
                    return idx
                if not first:
                    first = True
                    print("First", idx, candidate)

        return 0

    def part2(self, parsed_input: InputType) -> int:
        raise NotImplementedError

