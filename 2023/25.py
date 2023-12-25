#!/bin/python
"""Advent of Code, Day 25: Snowverload."""
from __future__ import annotations

import collections
import copy
import functools
import itertools
import math
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
        all_components = set(parsed_input)

        todo = [(list(all_components)[0], [])]
        pathcount = collections.defaultdict(int)
        while todo:
            cur, path = todo.pop()
            if cur == "ntq":
                print(cur, path)
            pathcount[cur] += 1
            for neighbor in parsed_input[cur]:
                if neighbor not in path:
                    todo.append((neighbor, path + [cur]))

        print(pathcount)
        return




        connections = set()
        for src, dsts in parsed_input.items():
            for dst in dsts:
                if src < dst:
                    connections.add((src, dst))
        print(f"{len(connections)=}")
        sorted_conns = sorted(connections, key=lambda x: len(parsed_input[x]))

        some_conns = set()
        for src, dsts in parsed_input.items():
            for dst in dsts:
                if len(parsed_input[src]) > 5 or len(parsed_input[dst]) > 5:
                    continue
                if src < dst:
                    some_conns.add((src, dst))
        print(f"{len(some_conns)=}")

        def get_wires():
            for src_a, dsts_a in parsed_input.items():
                for dst_a in dsts_a:
                    for src_b in dsts_a:
                        dsts_b = parsed_input[src_b]
                        for dst_b in dsts_b:
                            for src_c in dsts_a | dsts_b:
                                dsts_c = parsed_input[src_c]
                                for dst_c in dsts_c:
                                    triple = {frozenset({src_a, dst_a}), frozenset({src_b, dst_b}), frozenset({src_c, dst_c})}
                                    if len(triple) == 3 and all(len(i) == 2 for i in triple):
                                        yield [sorted(i) for i in triple]

                        

        cpy = copy.deepcopy(parsed_input)
        for step, triple in enumerate(get_wires()):
            if step and step % 100000 == 0:
                print(step)

            todo = {i for pair in triple for i in pair}
            if len(todo) != 6:
                continue

            valid = True
            for (src_a, dst_a), (src_b, dst_b) in zip(triple, triple[1:]):
                if (
                    src_a not in parsed_input[src_b]
                    and src_a not in parsed_input[dst_b]
                    and dst_a not in parsed_input[src_b]
                    and dst_a not in parsed_input[dst_b]
                ):
                    valid = False
            if not valid: continue


            for src, dst in triple:
                cpy[src].discard(dst)
                cpy[dst].discard(src)
            todo = {i for pair in triple for i in pair}
            groups = []
            while todo:
                gtodo = {todo.pop()}
                group = set()
                while gtodo:
                    cur = gtodo.pop()
                    todo.discard(cur)
                    group.add(cur)
                    gtodo.update(cpy[cur] - group)
                groups.append(group)
            if len(groups) == 2:
                return math.prod(len(g) for g in groups)
            for src, dst in triple:
                cpy[src].add(dst)
                cpy[dst].add(src)

        return 0

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
