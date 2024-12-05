#!/bin/python
"""Advent of Code, Day 5: Print Queue."""

import collections
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
Reports = list[list[int]]


class Day05(aoc.Challenge):
    """Day 5: Print Queue."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=143),
        aoc.TestCase(part=2, inputs=SAMPLE, want=123),
    ]
    INPUT_PARSER = aoc.ParseBlocks([aoc.parse_ints])

    def expand_rules(self, pairs: list[list[int]]) -> dict[int, set[int]]:
        """Expand the prerequisite tree to a flattened set."""
        prereq_tree = collections.defaultdict(set)
        for a, b in pairs:
            prereq_tree[b].add(a)

        expanded = collections.defaultdict(set)
        for node, todo in list(prereq_tree.items()):
            while todo:
                got = todo.pop()
                expanded[node].add(got)

        return expanded

    def categorize(self, reports: Reports, rules: dict[int, set[int]]) -> tuple[Reports, Reports]:
        """Sort reports into valid and invalid."""
        groups: dict[bool, Reports] = {True: [], False: []}
        for report in reports:
            valid = all(
                after not in rules[node]
                for idx, node in enumerate(report)
                for after in report[idx + 1:]
            )
            groups[valid].append(report)
        return groups[True], groups[False]

    def fix_invalid(self, invalid: Reports, rules: dict[int, set[int]]) -> Reports:
        """Reorder invalid reports to make them valid."""
        fixed_reports = []
        for report in invalid:
            to_order = set(report)
            ordered = []
            while to_order:
                found = next(
                    node
                    for node in list(to_order)
                    if all(after not in rules[node] for after in to_order)
                )
                to_order.remove(found)
                ordered.append(found)
            fixed_reports.append(ordered)
        return fixed_reports

    def solver(self, puzzle_input: InputType, part_one: bool) -> int:
        """Return the sum of the middle number of reports."""
        pairs, reports = puzzle_input
        rules = self.expand_rules(pairs)
        reports, invalid = self.categorize(reports, rules)
        if not part_one:
            reports = self.fix_invalid(invalid, rules)
        return sum(report[len(report) // 2] for report in reports)

# vim:expandtab:sw=4:ts=4
