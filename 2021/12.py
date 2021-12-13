#!/bin/python
"""Advent of Code: Day 12."""

import collections
import functools
import math
import re

import typer

from lib import aoc

InputType = list[tuple[str, str]]
SAMPLE = ["""\
start-A
start-b
A-c
A-b
b-d
A-end
b-end
""","""\
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
""","""\
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
""","""\
start-A
start-B
A-c
c-B
A-end
B-end
"""]


class Day12(aoc.Challenge):

    DEBUG = True

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=10),
        # aoc.TestCase(inputs=SAMPLE[1], part=1, want=19),
        # aoc.TestCase(inputs=SAMPLE[2], part=1, want=226),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=36),
        # aoc.TestCase(inputs=SAMPLE[1], part=2, want=103),
        # aoc.TestCase(inputs=SAMPLE[2], part=2, want=3509),
    )

    @functools.cache
    def paths(self, start, seen):
        if start == "end":
            return 1
        assert start not in seen
        if start.islower():
            seen = frozenset(seen | set([start]))
        subpaths = []
        for node in self.graph[start]:
            if node in seen:
                continue
            subpaths.append(self.paths(node, seen))
        return sum(subpaths)

    def part1(self, lines: InputType) -> int:
        self.paths.cache_clear()
        self.graph = lines
        paths = self.paths("start", frozenset())
        return paths

    @functools.cache
    def paths2(self, start, seen, twice):
        if start == "end":
            return 1
        assert start not in seen or start == twice
        if start.islower():
            seen = frozenset(seen | set([start]))
        subpaths = []
        for node in self.graph[start]:
            if node == "start":
                continue
            if node not in seen:
                subpaths.append(self.paths2(node, seen, twice))
            elif twice is None:
                subpaths.append(self.paths2(node, seen, node))
        return sum(subpaths)

    def part2(self, lines: InputType) -> int:
        self.paths2.cache_clear()
        self.graph = lines
        paths = self.paths2("start", frozenset(), None)
        return paths

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        graph = collections.defaultdict(list)
        for line in puzzle_input.splitlines():
            start, end = line.split("-")
            graph[start].append(end)
            graph[end].append(start)
        return dict(graph)


if __name__ == "__main__":
    typer.run(Day12().run)

# vim:expandtab:sw=4:ts=4
