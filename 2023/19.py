#!/bin/python
"""Advent of Code, Day 19: Aplenty."""

import operator
import typing
from lib import aoc

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

RuleName: typing.TypeAlias = str
Comparison: typing.TypeAlias = typing.Callable[[float, float], bool]
CompareRule: typing.TypeAlias = tuple[str, Comparison, int, RuleName]
DefaultRule: typing.TypeAlias = tuple[None, None, None, RuleName]
InputType = tuple[dict[RuleName, list[CompareRule | DefaultRule]], list[dict[str, int]]]


class Day19(aoc.Challenge):
    """Day 19: Aplenty."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=19114),
        aoc.TestCase(inputs=SAMPLE, part=2, want=167409079868000),
    ]

    def part1(self, parsed_input: InputType) -> int:
        """Return the sum points of the accepted items."""
        rules, items = parsed_input
        result = 0
        # For each item, walk through the rules.
        for item in items:
            tests = iter(rules["in"])
            while True:
                attr, op, val, target = next(tests)
                if op is None or op(item[attr], val):
                    if target == "A":
                        result += sum(item.values())
                        break
                    elif target == "R":
                        break
                    else:
                        tests = iter(rules[target])
        return result

    def part2(self, parsed_input: InputType) -> int:
        """Return the number of possible accepted items."""
        rules, _ = parsed_input
        accepted_contraints = []
        
        def reverse(attr, op, val):
            """Return the reverse of a condition.

            >>> reverse(m > 5)
            m < 6
            """
            if op == operator.gt:
                return attr, operator.lt, val + 1
            return attr, operator.gt, val - 1

        def recurse(constraints, tests):
            """Recursively explore rules to find constraint sets which are accepted."""
            attr, op, val, target = tests[0]
            if op is None:
                # Default rule: no constaints to add, only one brach to explore.
                if target == "A":
                    accepted_contraints.append(constraints.copy())
                elif target != "R":
                    recurse(constraints, rules[target])
            else:
                # Comparison rule: explore both paths with additional constraints added.
                # True path:
                if target == "A":
                    accepted_contraints.append(constraints + [(attr, op, val)])
                elif target != "R":
                    recurse(constraints + [(attr, op, val)], rules[target])
                # False path:
                recurse(constraints + [reverse(attr, op, val)], tests[1:])

        # Compute all constraint sets that lead to approval.
        recurse([], rules["in"])

        # Map constraint sets to accepted 4D intervals.
        all_intervals = []
        for constraints in accepted_contraints:
            # Start with a full [1, 4000] interval then update it with each constraint.
            intervals = {attr: [1, 4000] for attr in "xmas"}
            for attr, op, val in constraints:
                if op == operator.gt:
                    intervals[attr][0] = max(intervals[attr][0], val + 1)
                else:
                    intervals[attr][1] = min(intervals[attr][1], val - 1)
            all_intervals.append(intervals)

        # Multiply the interval sizes to get the total number of combinations.
        possibilities = 0
        for intervals in all_intervals:
            possibilities += math.prod(end - start + 1 for start, end in intervals.values())

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
