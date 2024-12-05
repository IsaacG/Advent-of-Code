#!/bin/python
"""Advent of Code, Day 5: Print Queue."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = """\
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
97,13,75,29,47"""

InputType = list[list[list[int]]]
Reports: list[list[int]]


class Day05(aoc.Challenge):
    """Day 5: Print Queue."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=143),
        aoc.TestCase(part=2, inputs=SAMPLE, want=123),
    ]
    INPUT_PARSER = aoc.ParseBlocks([aoc.parse_ints])

    def expand_rules(self, rules: list[list[int]]) -> dict[int, set[int]]:
        """Expand the prerequisite tree to a flattened set."""
        prereq_tree = collections.defaultdict(set)
        for a, b in rules:
            prereq_tree[b].add(a)

        expanded = collections.defaultdict(set)
        for node in list(prereq_tree):
            todo = list(prereq_tree[node])
            seen = set()
            while todo:
                got = todo.pop()
                expanded[node].add(got)

        return expanded

    def categorize(self, reports: Reports, rules: dict[int, set[int]]) -> tuple[Reports, Reports]:
        """Sort reports into valid and invalid."""
        groups = {True: [], False: []}
        for report in reports:
            valid = True
            for idx, node in enumerate(report):
                req = rules[node]
                for after in report[idx + 1:]:
                    if after in req:
                        valid = False
                    if not valid:
                        break
                if not valid:
                    break
            groups[valid].append(report)
        return groups[True], groups[False]

    def fix_invalid(self, invalid: Reports, expanded: dict[int, set[int]]) -> Reports:
        """Reorder invalid reports to make them valid."""
        fixed_reports = []
        for report in invalid:
            to_order = set(report)
            ordered = []
            while to_order:
                found = next(
                    node
                    for node in list(to_order)
                    if all(
                        after not in expanded[node]
                        for after in to_order
                    )
                )
                to_order.remove(found)
                ordered.append(found)
            fixed_reports.append(ordered)
        return fixed_reports

    def solver(self, puzzle_input: InputType, part_one: bool) -> int:
        """Return the sum of the middle number of reports."""
        rules, reports = puzzle_input
        expanded = self.expand_rules(rules)
        reports, invalid = self.categorize(reports, expanded)
        if not part_one:
            reports = self.fix_invalid(invalid, expanded)
        return sum(report[len(report) // 2] for report in reports)

# vim:expandtab:sw=4:ts=4
