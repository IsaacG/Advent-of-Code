#!/bin/python
"""Advent of Code: Day 12."""

import collections
import functools
from typing import Optional

import typer

from lib import aoc

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
"""]
# Node edges.
InputType = dict[str, list[str]]


class Day12(aoc.Challenge):
    """Find all the paths through a maze/graph."""

    DEBUG = True

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=10),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=19),
        aoc.TestCase(inputs=SAMPLE[2], part=1, want=226),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=36),
        aoc.TestCase(inputs=SAMPLE[1], part=2, want=103),
        aoc.TestCase(inputs=SAMPLE[2], part=2, want=3509),
    )

    @functools.cache
    def paths(self, start: str, seen: frozenset[str], twice: Optional[str]) -> int:
        """Count all the paths from `start` to "end" without revisiting `seen`.

        Allow a single small cave to be visited twice.
        """
        # If we are at the end, there are no further options.
        if start == "end":
            return 1
        # The start node should not appear in the seen nodes.
        assert start not in seen or start == twice
        # Update the list of nodes we cannot revisit.
        if start.islower():
            seen = frozenset(seen | set([start]))
        # Count paths from every neighbor to the end.
        subpaths = 0
        for node in self.graph[start]:
            # The start node should not be visited twice.
            if node == "start":
                continue
            # If the node is not a small cave we already visited, visit it.
            if node not in seen:
                subpaths += self.paths(node, seen, twice)
            # If we already visited it once, maybe visit it a second time.
            elif twice is None:
                subpaths += self.paths(node, seen, node)
        return subpaths

    def part1(self, parsed_input: InputType) -> int:
        """Count the number of paths from "start" to "end".

        Do not revisit small caves.
        """
        return self.solve(parsed_input, "start")

    def part2(self, parsed_input: InputType) -> int:
        """Count the number of paths from "start" to "end".

        Do not revisit small caves... excepting one small cave.
        """
        return self.solve(parsed_input, None)

    def solve(self, graph: InputType, twice: Optional[str]) -> int:
        """Solve the problem for either day."""
        self.paths.cache_clear()  # pylint:disable=E1101
        # Set self.graph to avoid having it be part of the cache keys.
        self.graph = graph  # pylint:disable=W0201
        return self.paths("start", frozenset(), twice)

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        graph = collections.defaultdict(list)
        # Form nodes of a non-directional graph.
        for line in puzzle_input.splitlines():
            start, end = line.split("-")
            graph[start].append(end)
            graph[end].append(start)
        return dict(graph)


if __name__ == "__main__":
    typer.run(Day12().run)

# vim:expandtab:sw=4:ts=4
