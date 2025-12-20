#!/bin/python
"""Advent of Code, Day 12: Digital Plumber."""

import collections
from lib import aoc


def solve(data: list[list[int]], part: int) -> int:
    """Return details of a specific group."""
    pipes = collections.defaultdict(set)
    for one, *others in data:
        for other in others:
            pipes[one].add(other)
            pipes[other].add(one)

    group_sizes = {}
    unseen = set(pipes)
    while unseen:
        seed = min(unseen)
        todo = {seed}
        seen = set()
        while todo:
            cur = todo.pop()
            unseen.remove(cur)
            seen.add(cur)
            for other in pipes[cur]:
                if other not in seen:
                    todo.add(other)
        group_sizes[seed] = len(seen)
    return group_sizes[0] if part == 1 else len(group_sizes)


PARSER = aoc.parse_ints
SAMPLE = """\
0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""
TESTS = [(1, SAMPLE, 6), (2, SAMPLE, 2)]
# vim:expandtab:sw=4:ts=4
