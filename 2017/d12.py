#!/bin/python
"""Advent of Code, Day 12: Digital Plumber."""

import collections
from lib import aoc

SAMPLE = """\
0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""


class Day12(aoc.Challenge):
    """Day 12: Digital Plumber."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=6),
        aoc.TestCase(part=2, inputs=SAMPLE, want=2),
    ]
    INPUT_PARSER = aoc.parse_ints

    def solver(self, puzzle_input: list[list[int]], part_one: bool) -> int:
        pipes = collections.defaultdict(set)
        for one, *others in puzzle_input:
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
        return group_sizes[0] if part_one else len(group_sizes)


# vim:expandtab:sw=4:ts=4
