#!/bin/python
"""Advent of Code, Day 23: LAN Party."""

import collections
import itertools
from lib import aoc
PARSER = aoc.BaseParseMultiPerLine(word_separator="-")


def solve(data: list[list[str]], part: int) -> str:
    """Return the largest clique."""
    connections = collections.defaultdict(set)
    for a, b in data:
        connections[a].add(b)
        connections[b].add(a)

    if part == 1:
        triples = set()
        for a, bs in connections.items():
            if not a.startswith("t"):
                continue
            for b, c in itertools.combinations(bs, 2):
                if c in connections[b]:
                    triples.add(frozenset({a, b, c}))
        return len(triples)

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
TESTS = [(1, SAMPLE, 7), (2, SAMPLE, "co,de,ka,ta")]
# vim:expandtab:sw=4:ts=4
