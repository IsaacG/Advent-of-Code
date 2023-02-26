#!/bin/python
"""Advent of Code, Day 7: The Sum of Its Parts."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

import typer
from lib import aoc

SAMPLE = """\
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""

LineType = int
InputType = list[LineType]


class Day07(aoc.Challenge):
    """Day 7: The Sum of Its Parts."""

    # DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: True, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want="CABDFE"),
        aoc.TestCase(inputs=SAMPLE, part=2, want=15),
    ]

    def part1(self, parsed_input: InputType) -> str:
        nodes, blocked = parsed_input
        order = []

        available = [n for n in nodes if n not in blocked]
        while available:
            available.sort()
            node = available.pop(0)
            order.append(node)
            self.debug(f"Next node: {node}")

            for n, dep in list(blocked.items()):
                if node in dep:
                    dep.remove(node)
                if not dep:
                    available.append(n)
                    del blocked[n]
        return "".join(order)

    def part2(self, parsed_input: InputType) -> int:
        nodes, blocked = parsed_input
        if self.testing:
            workers = 2
            base = ord("A") - 1
        else:
            workers = 5
            base = ord("A") - 1 - 60

        available = [n for n in nodes if n not in blocked]
        working = []
        clock = 0

        while available or working:
            while working and working[0][0] == clock:
                done_click, node = working.pop(0)
                for n, dep in list(blocked.items()):
                    if node in dep:
                        dep.remove(node)
                    if not dep:
                        available.append(n)
                        del blocked[n]

            available.sort()
            while len(working) < workers and available:
                node = available.pop(0)
                duration = ord(node) - base
                working.append((clock + duration, node))
                self.debug(f"Next node: {node}")

            working.sort()
            if working:
                clock = working[0][0]

        if not self.testing:
            assert clock > 177, clock
        return clock

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        patt = re.compile(r"Step (.) must be finished before step (.*) can begin\.")
        dependencies = collections.defaultdict(set)
        nodes = set()
        for line in puzzle_input.splitlines():
            a, b = patt.match(line).groups()
            dependencies[b].add(a)
            nodes.add(a)
            nodes.add(b)
        return nodes, dependencies


if __name__ == "__main__":
    typer.run(Day07().run)

# vim:expandtab:sw=4:ts=4
