#!/bin/python
"""Advent of Code, Day 7: The Sum of Its Parts. Unravel a dependency graph and time it."""

import collections
import re

from lib import aoc

SAMPLE = """\
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""

InputType = tuple[set[str], dict[str, set[str]]]


class Day07(aoc.Challenge):
    """Day 7: The Sum of Its Parts."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want="CABDFE"),
        aoc.TestCase(inputs=SAMPLE, part=2, want=15),
    ]

    def part1(self, parsed_input: InputType) -> str:
        """Return the order to work on jobs per a dependency graph."""
        nodes, blocked = parsed_input
        order = []

        available = [n for n in nodes if n not in blocked]
        while available:
            available.sort()
            node = available.pop(0)
            order.append(node)

            for n, dep in list(blocked.items()):
                if node in dep:
                    dep.remove(node)
                    if not dep:
                        available.append(n)
                        del blocked[n]
        return "".join(order)

    def part2(self, parsed_input: InputType) -> int:
        """Return the time to complete tasks given dependencies and N workers."""
        nodes, blocked = parsed_input
        if self.testing:
            workers = 2
            base = ord("A") - 1
        else:
            workers = 5
            base = ord("A") - 1 - 60  # Add 60 seconds to each job.

        available = [n for n in nodes if n not in blocked]
        working: list[tuple[int, str]] = []
        clock = 0

        while available or working:
            # Mark jobs done once time has arrived.
            while working and working[0][0] == clock:
                node = working.pop(0)[1]
                for n, dep in list(blocked.items()):
                    if node in dep:
                        dep.remove(node)
                        if not dep:
                            available.append(n)
                            del blocked[n]

            # Assign work to workers if work is available.
            available.sort()
            while len(working) < workers and available:
                node = available.pop(0)
                duration = ord(node) - base
                working.append((clock + duration, node))

            # Fast forward to the next event/job completion.
            if working:
                working.sort()
                clock = working[0][0]

        return clock

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        patt = re.compile(r"Step (.) must be finished before step (.*) can begin\.")
        dependencies = collections.defaultdict(set)
        nodes = set()
        for line in puzzle_input.splitlines():
            m = patt.match(line)
            assert m is not None
            a, b = m.groups()
            dependencies[b].add(a)
            nodes.add(a)
            nodes.add(b)
        return nodes, dependencies
