#!/bin/python
"""Advent of Code, Day 19: Aplenty."""

import math
import operator
import re
import typing

RuleName: typing.TypeAlias = str
Comparison: typing.TypeAlias = typing.Callable[[float, float], bool]
CompareRule: typing.TypeAlias = tuple[str, Comparison, int, RuleName]
DefaultRule: typing.TypeAlias = tuple[None, None, None, RuleName]
RuleSet: typing.TypeAlias = dict[RuleName, list[CompareRule | DefaultRule]]
InputType = tuple[RuleSet, list[dict[str, int]]]

RULE_RE = re.compile(r"(\w+){((?:.*,)*)(\w+)}")
TEST_RE = re.compile(r"(\w+)([><])(\d+):(\w+)")
ITEM_RE = re.compile(r"([xmas])=(\d+)")
OPS = {">": operator.gt, "<": operator.lt}


def accepted_contraints(rules: RuleSet) -> list[dict[str, tuple[int, int]]]:
    """Return a collection of constraints which lead to accepted."""
    accepted = []

    def reverse(attr, oper, val):
        """Return the reverse of a condition.

        >>> reverse(m > 5)
        m < 6
        """
        if oper == operator.gt:
            return attr, operator.lt, val + 1
        return attr, operator.gt, val - 1

    def recurse(constraints, tests):
        """Recursively explore rules to find constraint sets which are accepted."""
        attr, oper, val, target = tests[0]
        if oper is None:
            # Default rule: no constaints to add, only one brach to explore.
            if target in rules:
                recurse(constraints, rules[target])
            elif target == "A":
                accepted.append(constraints)
        else:
            # Comparison rule: explore both paths with additional constraints added.
            # True path:
            if target in rules:
                recurse(constraints + [(attr, oper, val)], rules[target])
            elif target == "A":
                accepted.append(constraints + [(attr, oper, val)])
            # False path:
            recurse(constraints + [reverse(attr, oper, val)], tests[1:])

    recurse([], rules["in"])
    return accepted


def solve(data: InputType, part: int) -> int:
    """Solve the parts."""
    return (part1 if part == 1 else part2)(data)


def part1(data: InputType) -> int:
    """Return the sum points of the accepted items."""
    rules, items = data
    result = 0
    # For each item, walk through the rules.
    for item in items:
        tests = iter(rules["in"])
        while True:
            attr, oper, val, target = next(tests)
            if oper is None or oper(item[attr], val):
                if target == "A":
                    result += sum(item.values())
                    break
                if target == "R":
                    break
                tests = iter(rules[target])
    return result


def part2(data: InputType) -> int:
    """Return the number of possible accepted items."""
    rules, _ = data

    # Map constraint sets to accepted 4D intervals.
    all_intervals = []
    for constraints in accepted_contraints(rules):
        # Start with a full [1, 4000] interval then update it with each constraint.
        intervals = {attr: [1, 4000] for attr in "xmas"}
        for attr, oper, val in constraints:
            if oper == operator.gt:
                intervals[attr][0] = max(intervals[attr][0], val + 1)
            else:
                intervals[attr][1] = min(intervals[attr][1], val - 1)
        all_intervals.append(intervals)

    # Multiply the interval sizes to get the total number of combinations.
    possibilities = 0
    for intervals in all_intervals:
        possibilities += math.prod(end - start + 1 for start, end in intervals.values())

    return possibilities


def input_parser(data: str) -> InputType:
    """Parse the input data."""
    rule_lines, part_lines = data.split("\n\n")

    rules = {}
    for line in rule_lines.splitlines():
        name, conditions, default = RULE_RE.match(line).groups()
        rules[name] = [
            (attr, OPS[comparison], int(value), target)
            for attr, comparison, value, target in TEST_RE.findall(conditions)
        ] + [(None, None, None, default)]

    items = [
        {key: int(val) for key, val in ITEM_RE.findall(line)}
        for line in part_lines.splitlines()
    ]

    return rules, items


SAMPLE = """\
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
{x=2127,m=1623,a=2188,s=1013}"""
TESTS = [(1, SAMPLE, 19114), (2, SAMPLE, 167409079868000)]
# vim:expandtab:sw=4:ts=4
