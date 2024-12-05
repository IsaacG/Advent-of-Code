#!/bin/python
"""Advent of Code, Day 5: Print Queue."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47""",  # 5
]

LineType = int
InputType = list[LineType]


class Day05(aoc.Challenge):
    """Day 5: Print Queue."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=143),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=123),
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
    INPUT_PARSER = aoc.ParseBlocks([aoc.parse_ints_per_line, aoc.parse_ints_per_line])
    # INPUT_PARSER = aoc.ParseOneWord(aoc.Board.from_int_block)
    # INPUT_PARSER = aoc.AsciiBoolMapParser("#")
    # INPUT_PARSER = aoc.char_map
    # ---
    # INPUT_PARSER = aoc.CharCoordinatesParser("S.#")
    # (width, height), start, garden, rocks = puzzle_input
    # max_x, max_y = width - 1, height - 1

    def part1(self, puzzle_input: InputType) -> int:
        rules, reports = puzzle_input
        reqs = collections.defaultdict(set)
        for a, b in rules:
            reqs[b].add(a)

        expanded = collections.defaultdict(set)
        for node in list(reqs):
            todo = list(reqs[node])
            seen = set()
            while todo:
                got = todo.pop()
                expanded[node].add(got)

        total = 0
        for report in reports:
            valid = True
            print("report", report)
            for idx, node in enumerate(report):
                req = reqs[node]
                for after in report[idx + 1:]:
                    if after in req:
                        valid = False
                    if not valid:
                        break
                if not valid:
                    break
            else:
                total += report[len(report) // 2]

        return total

    def part2(self, puzzle_input: InputType) -> int:
        rules, reports = puzzle_input
        reqs = collections.defaultdict(set)
        for a, b in rules:
            reqs[b].add(a)

        expanded = collections.defaultdict(set)
        for node in list(reqs):
            todo = list(reqs[node])
            seen = set()
            while todo:
                got = todo.pop()
                expanded[node].add(got)

        invalid = []
        for report in reports:
            valid = True
            for idx, node in enumerate(report):
                req = reqs[node]
                for after in report[idx + 1:]:
                    if after in req:
                        valid = False
                        invalid.append(report)
                    if not valid:
                        break
                if not valid:
                    break


        total = 0
        for report in invalid:
            todo = set(report)
            ordered = []
            while todo:
                found = None
                for node in list(todo):
                    for after in todo:
                        if node != after and after in reqs[node]:
                            break
                    else:
                        found = node
                if found is None:
                    raise Exception(f"Could not find valid node for {report} -> {ordered} -> {todo}")
                else:
                    todo.remove(found)
                    ordered.append(found)
            total += ordered[len(ordered) // 2]
            print(report, list(reversed(ordered)))

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
