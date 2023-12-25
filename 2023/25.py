#!/bin/python
"""Advent of Code, Day 25: Snowverload."""
from __future__ import annotations

import collections
import copy
import functools
import itertools
import math
import random
import re

from lib import aoc

SAMPLE = """\
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""

InputType = dict[int, set[int]]


class Day25(aoc.Challenge):
    """Day 25: Snowverload."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=54),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    def part1(self, parsed_input: InputType) -> int:
        graph = parsed_input
        graph_list = {src: list(dsts) for src, dsts in graph.items()}
        nodes = list(graph)
        node_count = len(nodes)
        counts = collections.Counter()

        for j in range(200):
            for i in range(50):
                # Randomly wander the graph from start until we find end. Record edges traversed.
                start = random.choice(nodes)
                end = random.choice(nodes)
                cur = start
                edges = set()
                while cur != end:
                    neighbor = random.choice(graph_list[cur])
                    edges.add(tuple(sorted([cur, neighbor])))
                    cur = neighbor
                counts.update(edges)

            # See if removing the most commonly traversed three edges results in a split graph.
            candidates = [i for i, _ in counts.most_common(3)]
            for a, b in candidates:
                graph[a].remove(b)
                graph[b].remove(a)

            todo = {nodes[0]}
            group = set()
            while todo:
                cur = todo.pop()
                group.add(cur)
                for neighbor in graph[cur]:
                    if neighbor not in group:
                        todo.add(neighbor)
            if len(group) != node_count:
                return len(group) * (node_count - len(group))
            for a, b in candidates:
                graph[a].add(b)
                graph[b].add(a)

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        connected = collections.defaultdict(set)
        for line in puzzle_input.splitlines():
            src, dsts = line.split(": ")
            for dst in dsts.split():
                connected[src].add(dst)
                connected[dst].add(src)
        labels = {val: idx for idx, val in enumerate(connected)}
        # Relabel the nodes using index numbers vs strings.
        return {labels[src]: {labels[dst] for dst in dsts} for src, dsts in connected.items()}

# vim:expandtab:sw=4:ts=4
