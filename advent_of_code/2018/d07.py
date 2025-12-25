#!/bin/python
"""Advent of Code, Day 7: The Sum of Its Parts. Unravel a dependency graph and time it."""

import collections
import re

from lib import aoc


def solve(data: tuple[set[str], dict[str, set[str]]], part: int, testing: bool) -> int:
    """Solve the parts."""
    return (part1 if part == 1 else part2)(data, testing)


def part1(data: tuple[set[str], dict[str, set[str]]], testing: bool) -> str:
    """Return the order to work on jobs per a dependency graph."""
    nodes, blocked = data
    task_order = []

    available = [n for n in nodes if n not in blocked]
    while available:
        available.sort()
        node = available.pop(0)
        task_order.append(node)

        for n, dep in list(blocked.items()):
            if node in dep:
                dep.remove(node)
                if not dep:
                    available.append(n)
                    del blocked[n]
    return "".join(task_order)


def part2(data: tuple[set[str], dict[str, set[str]]], testing: bool) -> int:
    """Return the time to complete tasks given dependencies and N workers."""
    nodes, blocked = data
    if testing:
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


def input_parser(data: str) -> tuple[set[str], dict[str, set[str]]]:
    """Parse the input."""
    patt = re.compile(r"Step (.) must be finished before step (.*) can begin\.")
    dependencies = collections.defaultdict(set)
    nodes = set()
    for line in data.splitlines():
        m = patt.match(line)
        assert m is not None
        a, b = m.groups()
        dependencies[b].add(a)
        nodes.add(a)
        nodes.add(b)
    return nodes, dependencies


SAMPLE = """\
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""
TESTS = [(1, SAMPLE, "CABDFE"), (2, SAMPLE, 15)]
