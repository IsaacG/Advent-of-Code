#!/bin/python
"""Advent of Code, Day 8: Haunted Wasteland."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
   """\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)""",  # 4
    """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)""",  # 16
    '''\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)''',
]

LineType = int
InputType = list[LineType]


class Day08(aoc.Challenge):
    """Day 8: Haunted Wasteland."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=2),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=6),
        aoc.TestCase(inputs=SAMPLE[2], part=2, want=6),
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
    # INPUT_PARSER = aoc.parse_re_findall_int(r"\d+")
    # INPUT_PARSER = aoc.parse_multi_mixed_per_line
    # INPUT_PARSER = aoc.parse_re_group_mixed(r"(foo) .* (\d+)")
    # INPUT_PARSER = aoc.parse_re_findall_mixed(r"\d+|foo|bar")
    INPUT_PARSER = aoc.ParseBlocks([aoc.parse_one_str_per_line, aoc.parse_one_str_per_line])

    def part1(self, parsed_input: InputType) -> int:
        instructions, nodes = parsed_input
        mapping = {}
        for line in nodes:
            start, left, right = re.findall(r"[a-zA-Z]+", line)
            mapping[start] = (left, right)
        location = "AAA"
        steps = 0
        for d in itertools.cycle(instructions[0]):
            idx = {"L": 0, "R": 1}[d]
            location = mapping[location][idx]
            steps += 1
            if location == "ZZZ":
                return steps



        return 0

    def part2(self, parsed_input: InputType) -> int:
        instructions, nodes = parsed_input
        mapping = {}
        for line in nodes:
            start, left, right = re.findall(r"[a-zA-Z0-9]+", line)
            mapping[start] = (left, right)
        locations = {i for i in mapping if i.endswith("A")}

        factors = []
        for location in locations:
            steps = 0
            for d in itertools.cycle(instructions[0]):
                idx = {"L": 0, "R": 1}[d]
                location = mapping[location][idx]
                steps += 1
                if location.endswith("Z"):
                    factors.append(steps)
                    break
        return math.lcm(*factors)

    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        raise NotImplementedError

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
