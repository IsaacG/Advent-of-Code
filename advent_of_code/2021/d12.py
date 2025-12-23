#!/bin/python
"""Advent of Code: Day 12. Find all the paths through a maze/graph."""

import collections
import functools


def solve(data: dict[str, list[str]], part: int) -> int:
    """Count the number of paths from "start" to "end".

    Do not revisit small caves... excepting maybe one small cave.
    """
    twice = "start" if part == 1 else None

    @functools.cache
    def paths(start: str, seen: frozenset[str], twice: str | None) -> int:
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
        for node in data[start]:
            # The start node should not be visited twice.
            if node == "start":
                continue
            # If the node is not a small cave we already visited, visit it.
            if node not in seen:
                subpaths += paths(node, seen, twice)
            # If we already visited it once, maybe visit it a second time.
            elif twice is None:
                subpaths += paths(node, seen, node)
        return subpaths

    return paths("start", frozenset(), twice)


def input_parser(data: str) -> dict[str, list[str]]:
    """Parse the input data."""
    graph = collections.defaultdict(list)
    # Form nodes of a non-directional graph.
    for line in data.splitlines():
        start, end = line.split("-")
        graph[start].append(end)
        graph[end].append(start)
    return dict(graph)


SAMPLE = ["""\
start-A
start-b
A-c
A-b
b-d
A-end
b-end
""", """\
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
""", """\
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
TESTS = (
    (1, SAMPLE[0], 10),
    (1, SAMPLE[1], 19),
    (1, SAMPLE[2], 226),
    (2, SAMPLE[0], 36),
    (2, SAMPLE[1], 103),
    (2, SAMPLE[2], 3509),
)
