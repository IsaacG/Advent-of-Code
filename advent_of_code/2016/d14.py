#!/bin/python
"""Advent of Code, Day 14: One-Time Pad."""

import collections
import hashlib
import itertools
import re
from collections import abc


def hash_gen(name: str, stretch: bool) -> abc.Generator[tuple[int, str, str], None, None]:
    """Generate MD5 digests which start with triplets.

    >>> r = 'RE.match(s)'
    >>> z = 'any(a == b == c for a, b, c in zip(s, s[1:], s[2:]))'
    >>> timeit.timeit(
            r,
            setup='
                s = "asdfd3fewafewewerrrsddasfdas";
                import re; RE = re.compile(r"(?P<a>)(?P=a)(?P=a)")'
        )
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
        if found := triplets.search(digest):
            yield i, found.group(1), digest


def solve(data: str, part: int) -> int:
    """Return the 64th key."""
    gen = hash_gen(data, part == 2)
    queue = collections.deque((next(gen) for _ in range(1001)), maxlen=1001)

    found = 0
    idx = 0
    while found < 64:
        idx, char, _ = queue.popleft()
        queue.append(next(gen))
        quints = char * 5
        if any(
            quints in digest
            for _, _, digest in itertools.takewhile(lambda x: x[0] <= idx + 1000, queue)
        ):
            found += 1

    return idx


TESTS = [(1, "abc", 22728), (2, "abc", 22551)]
