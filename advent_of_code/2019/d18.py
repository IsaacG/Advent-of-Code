#!/bin/python
"""Advent of Code, Day 18: Many-Worlds Interpretation."""
from __future__ import annotations

import collections
import functools
import itertools
import logging
import math
import queue
import re

from lib import aoc

SAMPLE = [
    """\
#########
#b.A.@.a#
#########""",  # 7
    """\
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################""",  # 17
    """\
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################""",  # 33
    """\
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################""",  # 42
    """\
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################""",  # 60
    """\
#######
#a.#Cd#
##...##
##.@.##
##...##
#cB#Ab#
#######""",
    """\
###############
#d.ABC.#.....a#
######...######
######.@.######
######...######
#b.....#.....c#
###############""",
    """\
#############
#DcBa.#.GhKl#
#.###...#I###
#e#d#.@.#j#k#
###C#...###J#
#fEbA.#.FgHi#
#############""",
    """\
#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba...BcIJ#
#####.@.#####
#nK.L...G...#
#M###N#H###.#
#o#m..#i#jk.#
#############""",
]

InputType = None
log = logging.info


class Day18(aoc.Challenge):
    """Day 18: Many-Worlds Interpretation."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=8),
        aoc.TestCase(part=1, inputs=SAMPLE[1], want=86),
        aoc.TestCase(part=1, inputs=SAMPLE[2], want=132),
        aoc.TestCase(part=1, inputs=SAMPLE[3], want=136),
        aoc.TestCase(part=1, inputs=SAMPLE[4], want=81),
        aoc.TestCase(part=2, inputs=SAMPLE[5], want=8),
        aoc.TestCase(part=2, inputs=SAMPLE[6], want=24),
        aoc.TestCase(part=2, inputs=SAMPLE[7], want=32),
        aoc.TestCase(part=2, inputs=SAMPLE[8], want=72),
    ]

    INPUT_PARSER = aoc.parse_one_str

    def part1(self, puzzle_input: InputType) -> int:
        data = aoc.CoordinatesParser(ignore="#", origin_top_left=True).parse(puzzle_input)
        nodes = {char: pos for pos, char in data.chars.items() if char.islower() or char == "@"}
        keys = set(nodes) - {"@"}
        num_keys = len(keys)
        edges = {node: {} for node in nodes}
        for start, pos in nodes.items():
            todo = collections.deque([(0, pos, frozenset())])
            seen = {pos}
            while len(edges[start]) < num_keys - 1:
                steps, pos, doors = todo.popleft()
                char = data.chars[pos]
                if char.islower() and char != start:
                    edges[start][char] = (steps, doors)
                steps += 1
                for n in data.neighbors(pos):
                    if n in seen:
                        continue
                    seen.add(n)
                    char = data.chars[n]
                    if char.isupper():
                        todo.append((steps, n, frozenset(doors | {char.lower()})))
                    else:
                        todo.append((steps, n, doors))
        todo = collections.deque()
        todo.append((0, "@", frozenset()))
        smallest = 1e9
        seen = {}
        while todo:
            steps, pos, got = todo.pop()
            if steps > smallest:
                continue
            if len(got) == num_keys:
                if steps < smallest:
                    smallest = steps
                continue
            for key, (distance, doors) in edges[pos].items():
                new_steps = steps + distance
                if key in got or doors - got or new_steps > smallest:
                    continue
                new_got = frozenset(got | {key})
                if (key, new_got) in seen and seen[key, new_got] <= new_steps:
                    continue
                seen[key, new_got] = new_steps
                todo.append((new_steps, key, new_got))

        return smallest

    def part2(self, puzzle_input: InputType) -> int:
        data = aoc.CoordinatesParser(ignore=None, origin_top_left=True).parse(puzzle_input)

        center = data.coords["@"].copy().pop()
        data.update(center, "#")
        for i, n in enumerate([complex(-1, -1), complex(1, -1), complex(1, 1), complex(-1, 1)]):
            data.update(center + n, str(i))
        for n in data.neighbors(center):
            data.update(n, "#")

        new_map = aoc.render_char_map(data.chars, data.max_y + 1, data.max_x + 1)
        # print(puzzle_input)
        # print()
        # print(new_map)
        data = aoc.CoordinatesParser(ignore="#", origin_top_left=True).parse(new_map)

        nodes = {char: pos for pos, char in data.chars.items() if char.islower() or char in "0123"}
        keys = {n for n in nodes if n.islower()}
        num_keys = len(keys)
        edges = {node: {} for node in nodes}
        for start, pos in nodes.items():
            todo = collections.deque([(0, pos, frozenset())])
            seen = {pos}
            while todo:
                steps, pos, doors = todo.popleft()
                char = data.chars[pos]
                if char.islower() and char != start:
                    edges[start][char] = (steps, doors)
                steps += 1
                for n in data.neighbors(pos):
                    if n in seen:
                        continue
                    seen.add(n)
                    char = data.chars[n]
                    if char.isupper():
                        todo.append((steps, n, frozenset(doors | {char.lower()})))
                    else:
                        todo.append((steps, n, doors))
        todo = collections.deque()
        todo.append((0, "0", "1", "2", "3", frozenset()))
        smallest = 1e9
        seen = {}
        while todo:
            steps, *positions, got = todo.pop()
            if steps > smallest:
                continue
            if len(got) == num_keys:
                if steps < smallest:
                    smallest = steps
                continue
            for bot, pos in enumerate(positions):
                for key, (distance, doors) in edges[pos].items():
                    new_steps = steps + distance
                    if key in got or doors - got or new_steps > smallest:
                        continue
                    new_got = frozenset(got | {key})
                    new_positions = positions.copy()
                    new_positions[bot] = key
                    if (*new_positions, new_got) in seen and seen[*new_positions, new_got] <= new_steps:
                        continue
                    seen[*new_positions, new_got] = new_steps
                    todo.append((new_steps, *new_positions, new_got))

        if not self.testing:
            assert smallest < 2388
        return smallest

    # def solver(self, puzzle_input: InputType, part_one: bool) -> int | str:


# vim:expandtab:sw=4:ts=4
