#!/bin/python
"""Advent of Code, Day 7: Recursive Circus."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)""",  # 0
]

LineType = int
InputType = list[LineType]


class Day07(aoc.Challenge):
    """Day 7: Recursive Circus."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [False, True]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want="tknk"),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=60),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_re_findall_mixed(r"\d+|[a-z]+")

    def part1(self, parsed_input: InputType) -> str:
        candidates: set[str] = set()
        invalid: set[str] = set()
        for (node, weight, *children) in parsed_input:
            candidates.add(node)
            invalid.update(children)
        root = candidates - invalid
        return root.pop()

    def part2(self, parsed_input: InputType) -> int:
        node_weight: dict[str, int] = {}
        node_children: dict[str, set[str]] = collections.defaultdict(set)
        invalid: set[str] = set()
        for (node, weight, *children) in parsed_input:
            node_weight[node] = weight
            node_children[node].update(children)
            invalid.update(children)
        root = (set(node_weight) - invalid).pop()

        tower_weights: dict[str, int] = {}
        def sum_weights(node: str) -> int:
            if node not in tower_weights:
                tower_weights[node] = node_weight[node] + sum(sum_weights(child) for child in node_children[node])
            return tower_weights[node]

        to_check = set(node_weight)
        while to_check:
            node = next(
                node
                for node in to_check
                if all(child not in to_check for child in node_children[node])
            )
            to_check.remove(node)
            weights = collections.Counter(sum_weights(child) for child in node_children[node]).most_common()
            if len(weights) <= 1:
                continue
            (common, _), (outlier, _) = weights
            tower = next(child for child in node_children[node] if sum_weights(child) == outlier)
            print(node, weights, node_weight[node])
            return node_weight[tower] + (common - outlier)

    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        raise NotImplementedError

# vim:expandtab:sw=4:ts=4
