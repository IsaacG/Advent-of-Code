#!/bin/python
"""Advent of Code, Day 7: Recursive Circus."""

import collections
from lib import aoc

SAMPLE = """\
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
cntj (57)"""


class Day07(aoc.Challenge):
    """Day 7: Recursive Circus."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want="tknk"),
        aoc.TestCase(inputs=SAMPLE, part=2, want=60),
    ]
    INPUT_PARSER = aoc.parse_re_findall_mixed(r"\d+|[a-z]+")

    def solver(self, puzzle_input: list[list[int | str]], part_one: bool) -> int | str:
        node_weight: dict[str, int] = {}
        node_children: dict[str, set[str]] = collections.defaultdict(set)
        not_root: set[str] = set()

        node: str
        weight: int
        children: list[str]
        for (node, weight, *children) in puzzle_input:  # type: ignore
            node_weight[node] = weight
            node_children[node].update(children)
            not_root.update(children)
        root = (set(node_weight) - not_root).pop()
        if part_one:
            return root

        tower_weights: dict[str, int] = {}

        def sum_weights(node: str) -> int:
            """Compute weight of a tower recursively with dynamic programming."""
            if node not in tower_weights:
                tower_weights[node] = node_weight[node] + sum(
                    sum_weights(child) for child in node_children[node]
                )
            return tower_weights[node]

        weight_offset, current = 0, root
        while True:
            # Weights of subprograms.
            weights = {child: sum_weights(child) for child in node_children[current]}
            # We expect there to be multiple counts as one node should be an outlier.
            # Until it is balanced, at which point we found the problem node.
            counts = collections.Counter(weights.values()).most_common()

            if len(counts) <= 1:
                # If the children are balanced, the current node needs adjusting.
                return node_weight[current] + weight_offset

            # Find the weight delta then repeat at the outlier child.
            (sibling_weight, _), (outlier_weight, _) = counts
            weight_offset = sibling_weight - outlier_weight
            current = next(
                child for child, weight in weights.items()
                if sum_weights(child) == outlier_weight
            )

        raise RuntimeError("No solution found.")

# vim:expandtab:sw=4:ts=4
