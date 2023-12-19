#!/bin/python
"""Advent of Code, Day 19: Aplenty."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import operator
import re

from lib import aoc

SAMPLE = [
    """\
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}""",  # 23
    'in',  # 24
    '{x=787,m=2655,a=1222,s=2876}',  # 25
    'in',  # 26
    'qqz',  # 27
    'qs',  # 28
    'lnx',  # 29
    '{x=1679,m=44,a=2067,s=496}',  # 30
    'in',  # 31
    'px',  # 32
    'rfg',  # 33
    'gd',  # 34
    '{x=2036,m=264,a=79,s=2244}',  # 35
    'in',  # 36
    'qqz',  # 37
    'hdj',  # 38
    'pv',  # 39
    '{x=2461,m=1339,a=466,s=291}',  # 40
    'in',  # 41
    'px',  # 42
    'qkq',  # 43
    'crn',  # 44
    '{x=2127,m=1623,a=2188,s=1013}',  # 45
    'in',  # 46
    'px',  # 47
    'rfg',  # 48
    'x',  # 49
    'm',  # 50
    'a',  # 51
    's',  # 52
    '7540',  # 53
    'x=787',  # 54
    '4623',  # 55
    'x=2036',  # 56
    '6951',  # 57
    'x=2127',  # 58
]

LineType = int
InputType = list[LineType]


class Day19(aoc.Challenge):
    """Day 19: Aplenty."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=19114),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=167409079868000),
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
    # INPUT_PARSER = aoc.ParseBlocks([aoc.parse_one_str_per_line, aoc.parse_re_findall_int(r"\d+")])
    # INPUT_PARSER = aoc.ParseOneWord(aoc.Board.from_int_block)
    # INPUT_PARSER = aoc.parse_ascii_bool_map("#")

    def part1(self, parsed_input: InputType) -> int:
        rules, items = parsed_input
        # print(rules)
        accepted = []
        for item in items:
            # print(f"Check {item=}")
            tests = iter(rules["in"])
            while True:
                attr, op, val, target = next(tests)
                # print(attr, item[attr], op, val, target, op(item[attr], val))
                if op is None:
                    # print("Default", target)
                    if target == "A":
                        accepted.append(item)
                        # print("Accepted")
                        break
                    elif target == "R":
                        # print("Rejected")
                        break
                    else:
                        tests = iter(rules[target])
                elif op(item[attr], val):
                    if target == "A":
                        accepted.append(item)
                        # print("Accepted")
                        break
                    elif target == "R":
                        # print("Rejected")
                        break
                    else:
                        # print("Load rules", target)
                        tests = iter(rules[target])
        return sum(sum(item.values()) for item in accepted)

    def part2(self, parsed_input: InputType) -> int:
        rules, _ = parsed_input

        accepted_contraints = []
        rejected_contraints = []
        
        def reverse(attr, op, val):
            if op == operator.gt:
                return attr, operator.lt, val + 1
            elif op == operator.lt:
                return attr, operator.gt, val - 1

        def recurse(constraints, tests):
            # print(f"Called recurse({constraints}, {tests})")
            attr, op, val, target = tests[0]
            if op is None:
                # print("Default rule to", target)
                if target == "A":
                    accepted_contraints.append(constraints.copy())
                elif target == "R":
                    rejected_contraints.append(constraints.copy())
                else:
                    recurse(constraints, rules[target])
            else:
                if target == "A":
                    accepted_contraints.append(constraints + [(attr, op, val)])
                elif target == "R":
                    rejected_contraints.append(constraints + [(attr, op, val)])
                else:
                    recurse(constraints + [(attr, op, val)], rules[target])
                recurse(constraints + [reverse(attr, op, val)], tests[1:])

        recurse([], rules["in"])
        possibilities = 0
        for constraints in accepted_contraints:
            intervals = {attr: [1, 4000] for attr in "xmas"}
            for attr, op, val in constraints:
                if op == operator.gt:
                    intervals[attr][0] = max(intervals[attr][0], val + 1)
                else:
                    intervals[attr][1] = min(intervals[attr][1], val - 1)
            poss = 1
            for start, end in intervals.values():
                poss *= (end - start + 1)
            # print(constraints, intervals, poss, "\n")
            # print(intervals)
            possibilities += poss
        return possibilities


    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        raise NotImplementedError

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        rule_lines, part_lines = puzzle_input.split("\n\n")

        rules = {}
        for rule in rule_lines.splitlines():
            name, parts_str = rule.removesuffix("}").split("{")
            parts = parts_str.split(",")
            default = parts[-1]
            tests = []
            for part in parts[:-1]:
                cond, target = part.split(":")
                if ">" in cond:
                    attr, val = cond.split(">")
                    tests.append((attr, operator.gt, int(val), target))
                elif "<" in cond:
                    attr, val = cond.split("<")
                    tests.append((attr, operator.lt, int(val), target))

            tests.append((None, None, None, default))
            rules[name] = tests

        items = []
        for part in part_lines.splitlines():
            item = {}
            for vals in part.strip("{}").split(","):
                k, v = vals.split("=")
                item[k] = int(v)
            items.append(item)

        return rules, items



# vim:expandtab:sw=4:ts=4
