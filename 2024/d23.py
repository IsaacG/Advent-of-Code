#!/bin/python
"""Advent of Code, Day 23: LAN Party."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
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
td-yn""",  # 0
    'kh-tc',  # 1
    'kh',  # 2
    'tc',  # 3
    'tc-kh',  # 4
    '12',  # 5
    """\
aq,cg,yn
aq,vc,wq
co,de,ka
co,de,ta
co,ka,ta
de,ka,ta
kh,qp,ub
qp,td,wh
tb,vc,wq
tc,td,wh
td,wh,yn
ub,vc,wq""",  # 6
    't',  # 7
    't',  # 8
    'co,de,',  # 9
    'co,ka,',  # 10
    'de,ka,',  # 11
    'qp,',  # 12
    ',wh',  # 13
    ',vc,wq',  # 14
    ',',  # 15
    ',wh',  # 16
    ',wh,yn',  # 17
    't',  # 18
]

LineType = int
InputType = list[LineType]


class Day23(aoc.Challenge):
    """Day 23: LAN Party."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=7),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want="co,de,ka,ta"),
        # aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    # INPUT_PARSER = aoc.parse_one_str
    # INPUT_PARSER = aoc.parse_one_str_per_line
    # INPUT_PARSER = aoc.parse_multi_str_per_line
    # INPUT_PARSER = aoc.parse_one_int
    # INPUT_PARSER = aoc.parse_one_int_per_line
    # INPUT_PARSER = aoc.parse_ints_one_line
    # INPUT_PARSER = aoc.parse_ints_per_line
    # INPUT_PARSER = aoc.parse_re_group_str(r"(a) .* (b) .* (c)")
    # INPUT_PARSER = aoc.parse_re_findall_str(r"(a|b|c)")
    # INPUT_PARSER = aoc.parse_multi_mixed_per_line
    # INPUT_PARSER = aoc.parse_re_group_mixed(r"(foo) .* (\d+)")
    # INPUT_PARSER = aoc.parse_re_findall_mixed(r"\d+|foo|bar")
    # INPUT_PARSER = aoc.ParseBlocks([aoc.parse_one_str_per_line, aoc.parse_re_findall_int(r"\d+")])
    # INPUT_PARSER = aoc.ParseOneWord(aoc.Board.from_int_block)
    # INPUT_PARSER = aoc.CoordinatesParser(chars=None, origin_top_left=True)
    # ---
    # (width, height), start, garden, rocks = puzzle_input
    # max_x, max_y = width - 1, height - 1

    def part1(self, puzzle_input: InputType) -> int:
        conns = collections.defaultdict(set)
        for line in puzzle_input:
            a, b = line.split("-")
            conns[a].add(b)
            conns[b].add(a)

        colls = set()
        for a, bs in conns.items():
            if not a.startswith("t"):
                continue
            for b, c in itertools.permutations(bs, 2):
                if c in conns[b]:
                    colls.add(tuple(sorted([a, b, c])))
        return len(colls)

    def part2(self, puzzle_input: InputType) -> int:
        conns = collections.defaultdict(set)
        for line in puzzle_input:
            a, b = line.split("-")
            conns[a].add(b)
            conns[b].add(a)

        lengths = set()
        for a, b in conns.items():
            b.add(a)
            lengths.add(len(b))

        
        clicks = []
        for party in conns.values():
            c = set()
            for i in range(len(party), 1, -1):
                for candidates in itertools.combinations(party, i):
                    if all(i in conns[j] for i, j in itertools.combinations(candidates, 2)):
                        clicks.append(set(candidates))

        party = max(clicks, key=len)
        return ",".join(sorted(party))


# vim:expandtab:sw=4:ts=4
