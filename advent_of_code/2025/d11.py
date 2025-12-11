#!/bin/python
"""Advent of Code, Day 11: Reactor."""
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
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out""",  # 0
    """\
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out""",
]

LineType = int
InputType = list[LineType]
log = logging.info


class Day11(aoc.Challenge):
    """Day 11: Reactor."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=5),
        aoc.TestCase(part=2, inputs=SAMPLE[1], want=2),
        # aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    def part1(self, puzzle_input: InputType) -> int:
        g = {}
        for src, *dsts in puzzle_input:
            g[src.strip(":")] = dsts

        q = collections.deque()
        q.append("you")
        total = 0
        while q:
            node = q.popleft()
            if node == "out":
                total += 1
            else:
                for i in g[node]:
                    q.append(i)
        print("\n".join(["==="] + [f"{k}={v!r}" for k, v in locals().items()] + ["==="]))
        return total

    def part2(self, puzzle_input: InputType) -> int:
        names = set()
        for src, *dsts in puzzle_input:
            names.add(src.strip(":"))
            names.update(dsts)
        nums = dict((n, i) for i, n in enumerate(names))

        g = {}
        for src, *dsts in puzzle_input:
            g[nums[src.strip(":")]] = [nums[d] for d in dsts]
        svr = nums["svr"]
        out = nums["out"]
        dac = nums["dac"]
        fft = nums["fft"]

        @functools.cache
        def paths_via(node):
            if node == out:
                return {0: 1, 1: 0, 2: 0, 3: 0}
            paths = {i: 0 for i in range(4)}
            for i in g[node]:
                p = paths_via(i)
                for i, j in p.items():
                    paths[i] += j
            if node == dac:
                paths[1] = paths[0]
                paths[3] = paths[2]
                paths[0] = 0
                paths[2] = 0
            elif node == fft:
                paths[2] = paths[0]
                paths[3] = paths[1]
                paths[0] = 0
                paths[1] = 0
            return paths

        return paths_via(svr)[3]


        q = collections.deque()
        q.append((nums["svr"], frozenset(), False, False))
        total = 0
        while q:
            node, seen, x, y = q.popleft()
            if node == out and x and y:
                total += 1
                continue
            if node == out:
                continue
            if node == dac:
                x = True
            if node == fft:
                y = True
            for i in g[node]:
                if i in seen:
                    continue
                seen = frozenset(seen | {i})
                q.append((i, seen, x, y))
        print("\n".join(["==="] + [f"{k}={v!r}" for k, v in locals().items()] + ["==="]))
        return total


    # def solver(self, puzzle_input: InputType, part_one: bool) -> int | str:

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return super().input_parser(puzzle_input)
        return puzzle_input.splitlines()
        return puzzle_input
        return [int(i) for i in puzzle_input.splitlines()]
        mutate = lambda x: (x[0], int(x[1])) 
        return [mutate(line.split()) for line in puzzle_input.splitlines()]
        # Words: mixed str and int
        return [
            tuple(
                int(i) if i.isdigit() else i
                for i in line.split()
            )
            for line in puzzle_input.splitlines()
        ]
        # Regex splitting
        patt = re.compile(r"(.*) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.")
        return [
            tuple(
                int(i) if i.isdigit() else i
                for i in patt.match(line).groups()
            )
            for line in puzzle_input.splitlines()
        ]

# vim:expandtab:sw=4:ts=4
