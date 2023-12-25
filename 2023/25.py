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

SAMPLE = [
    """\
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
frs: qnr lhk lsr""",  # 4
]

LineType = int
InputType = list[LineType]


class Day25(aoc.Challenge):
    """Day 25: Snowverload."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [False, True]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=54),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=0),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    # INPUT_PARSER = aoc.parse_one_str_per_line
    # INPUT_PARSER = aoc.parse_one_str
    # INPUT_PARSER = aoc.parse_one_int
    # INPUT_PARSER = aoc.parse_one_str_per_line
    # INPUT_PARSER = aoc.parse_one_int_per_line
    # INPUT_PARSER = aoc.parse_multi_str_per_line
    # INPUT_PARSER = aoc.parse_re_group_str(r"(a) .* (b) .* (c)")
    # INPUT_PARSER = aoc.parse_re_findall_str(r"(a|b|c)")
    # INPUT_PARSER = aoc.parse_multi_int_per_line
    # INPUT_PARSER = aoc.parse_re_group_int(r"(\d+)")
    # INPUT_PARSER = aoc.parse_re_findall_int(aoc.RE_INT)
    # INPUT_PARSER = aoc.parse_multi_mixed_per_line
    # INPUT_PARSER = aoc.parse_re_group_mixed(r"(foo) .* (\d+)")
    # INPUT_PARSER = aoc.parse_re_findall_mixed(r"\d+|foo|bar")
    # INPUT_PARSER = aoc.ParseBlocks([aoc.parse_one_str_per_line, aoc.parse_re_findall_int(r"\d+")])
    # INPUT_PARSER = aoc.ParseOneWord(aoc.Board.from_int_block)
    # INPUT_PARSER = aoc.parse_ascii_bool_map("#")
    # ---
    # INPUT_PARSER = aoc.CharCoordinatesParser("S.#")
    # (width, height), start, garden, rocks = parsed_input
    # max_x, max_y = width - 1, height - 1

    def part1(self, parsed_input: InputType) -> int:
        graph = {src: list(dsts) for src, dsts in parsed_input.items()}
        nodes = list(graph)
        counts = collections.Counter()

        for j in range(200):
            for i in range(50):
                if i and i % 10 == 0:
                    print("Step", j, i)
                start = random.choice(nodes)
                end = random.choice(nodes)
                if start == end:
                    continue
                todo = []
                todo.append((start, set(), set()))
                while todo:
                    cur, path, edges = random.choice(todo)
                    todo.remove((cur, path, edges))
                    if cur == end:
                        counts.update(edges)
                        print(start, end)
                        break

                    newpath = path | {cur}
                    for neighbor in parsed_input[cur]:
                        if neighbor not in path:
                            new_edges = edges | {tuple(sorted([cur, neighbor]))}
                            todo.append((neighbor, newpath, new_edges))

            graph = copy.deepcopy(parsed_input)
            for (a, b), _ in counts.most_common(3):
                graph[a].remove(b)
                graph[b].remove(a)

            todo = set(graph)
            groups = []
            while todo:
                gtodo = {todo.pop()}
                group = set()
                while gtodo:
                    cur = gtodo.pop()
                    todo.discard(cur)
                    group.add(cur)
                    gtodo.update(graph[cur] - group)
                groups.append(group)
            if len(groups) == 2:
                print(counts.most_common(3))
                return math.prod(len(g) for g in groups)

    def part2(self, parsed_input: InputType) -> int:
        raise NotImplementedError

    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        raise NotImplementedError

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        connected = collections.defaultdict(set)
        for line in puzzle_input.splitlines():
            src, dsts = line.split(": ")
            for dst in dsts.split():
                connected[src].add(dst)
                connected[dst].add(src)
        return connected

# vim:expandtab:sw=4:ts=4
