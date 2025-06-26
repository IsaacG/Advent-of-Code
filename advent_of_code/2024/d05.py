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

    def solver(self, puzzle_input: InputType, part_one: bool) -> int:
        """Return the sum of the middle number of reports."""
        pairs, reports = puzzle_input
        prereq_tree = collections.defaultdict(set)
        for a, b in pairs:
            prereq_tree[b].add(a)

        total = 0
        for report in reports:
            pages = set(report)
            simplified_rules = {a: b & pages for a, b in prereq_tree.items() if a in pages}
            correct_order = sorted(pages, key=lambda p: len(simplified_rules.get(p, [])))
            if (report == correct_order) == part_one:
                total += correct_order[len(correct_order) // 2]
        return total


# vim:expandtab:sw=4:ts=4
