#!/bin/python
"""Advent of Code, Day 8: Playground."""
from __future__ import annotations

import collections
import functools
import itertools
import logging
import math
import re

from lib import aoc

SAMPLE = [
    """\
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689""",  # 0
]

LineType = int
InputType = list[LineType]
log = logging.info


class Day08(aoc.Challenge):
    """Day 8: Playground."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=40),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=25272),
    ]

    # INPUT_PARSER = aoc.parse_ints
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
        boxes = set(tuple(i) for i in puzzle_input)
        circuits = []
        closest = 0
        distances = []

        def delta(a, b):
            return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2

        for a in boxes:
            for b in boxes:
                if a >= b:
                    continue
                distances.append((delta(a, b), a, b))
        distances.sort()
        it = iter(distances)

        connections = 0
        for _, a, b in distances[:10 if self.testing else 1000]:
            # print("Consider", a, b)
            ca = next((i for i in circuits if a in i), {a,})
            cb = next((i for i in circuits if b in i), {b,})
            if ca == cb:
                connections += 1
                continue
            if len(ca) > 1:
                circuits.remove(ca)
            if len(cb) > 1:
                circuits.remove(cb)
            cc = ca | cb
            circuits.append(cc)
            connections += 1
            # print(connections, a, b, len(cc))

        sizes = [len(i) for i in circuits]
        print(sizes)
        sizes.sort(reverse=1)
        # assert len(sizes) >= 3
        return math.prod(sizes[:3])

    def part2(self, puzzle_input: InputType) -> int:
        boxes = set(tuple(i) for i in puzzle_input)
        circuits = []
        closest = 0
        distances = []

        def delta(a, b):
            return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2

        for a in boxes:
            for b in boxes:
                if a >= b:
                    continue
                distances.append((delta(a, b), a, b))
        distances.sort()
        it = iter(distances)
        count = len(boxes)

        connections = 0
        for _, a, b in distances:
            # print("Consider", a, b)
            ca = next((i for i in circuits if a in i), {a,})
            cb = next((i for i in circuits if b in i), {b,})
            if ca == cb:
                continue
            if len(ca) > 1:
                circuits.remove(ca)
            if len(cb) > 1:
                circuits.remove(cb)
            cc = ca | cb
            circuits.append(cc)
            if len(cc) == count:
                print(len(circuits))
                return a[0] * b[0]

        sizes = [len(i) for i in circuits]
        print(sizes)
        sizes.sort(reverse=1)
        # assert len(sizes) >= 3
        return math.prod(sizes[:3])

# vim:expandtab:sw=4:ts=4
