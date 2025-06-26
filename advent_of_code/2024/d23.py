#!/bin/python
"""Advent of Code, Day 23: LAN Party."""

import collections
import itertools
from lib import aoc

SAMPLE = """\
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""


class Day23(aoc.Challenge):
    """Day 23: LAN Party."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=7),
        aoc.TestCase(part=2, inputs=SAMPLE, want="co,de,ka,ta"),
    ]
    INPUT_PARSER = aoc.BaseParseMultiPerLine(word_separator="-")

    def part1(self, puzzle_input: list[list[str]]) -> int:
        """Count the number of three interconnected nodes."""
        connections = collections.defaultdict(set)
        for a, b in puzzle_input:
            connections[a].add(b)
            connections[b].add(a)

        triples = set()
        for a, bs in connections.items():
            if not a.startswith("t"):
                continue
            for b, c in itertools.combinations(bs, 2):
                if c in connections[b]:
                    triples.add(frozenset({a, b, c}))
        return len(triples)

    def part2(self, puzzle_input: list[list[str]]) -> str:
        """Return the largest clique."""
        connections = collections.defaultdict(set)
        for a, b in puzzle_input:
            connections[a].add(b)
            connections[b].add(a)

        for a, bs in connections.items():
            bs.add(a)

        longest = max(len(i) for i in connections.values())

        for length in range(longest, 1, -1):
            for party in connections.values():
                if len(party) < length:
                    continue
                for candidates in itertools.combinations(party, length):
                    if all(i in connections[j] for i, j in itertools.combinations(candidates, 2)):
                        return ",".join(sorted(candidates))
        raise RuntimeError("No solution found")

# vim:expandtab:sw=4:ts=4
