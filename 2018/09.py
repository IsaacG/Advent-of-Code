#!/bin/python
"""Advent of Code, Day 9: Marble Mania."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

import typer
from lib import aoc

SAMPLE = [
    "9 players; last marble is worth 25 points",
    "10 players; last marble is worth 1618 points",
    "13 players; last marble is worth 7999 points",
    "17 players; last marble is worth 1104 points",
    "21 players; last marble is worth 6111 points",
    "30 players; last marble is worth 5807 points",
]

LineType = int
InputType = list[LineType]


class Day09(aoc.Challenge):
    """Day 9: Marble Mania."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=32),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=8317),
        aoc.TestCase(inputs=SAMPLE[2], part=1, want=146373),
        aoc.TestCase(inputs=SAMPLE[3], part=1, want=2764),
        aoc.TestCase(inputs=SAMPLE[4], part=1, want=54718),
        aoc.TestCase(inputs=SAMPLE[5], part=1, want=37305),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_re_findall_int(r"\d+")

    def part2(self, parsed_input: InputType) -> int:
        players, last = parsed_input[0]
        return self.part1([[players, last * 100]])

    def part1(self, parsed_input: InputType) -> int:
        players, last = parsed_input[0]
        score = [0] * players
        cur = aoc.Node(0)
        start = cur
        cur.next = cur.prev = cur
        for marble in range(1, last + 1):
            if marble % 23:
                cur = aoc.Node(marble, prev=cur.next, next=cur.next.next)
            else:
                for _ in range(6):
                    cur = cur.prev
                removed = cur.prev
                score[(marble - 1) % players] += marble + removed.val
                removed.prev.next = removed.next
                removed.next.prev = removed.prev

            # i = start
            # out = []
            # while not out or i != start:
            #     if i == cur:
            #         out.append(f"({i.val})")
            #     else:
            #         out.append(str(i.val))
            #     i = i.next
            # print(" ".join(out))
        return max(score)

if __name__ == "__main__":
    typer.run(Day09().run)

# vim:expandtab:sw=4:ts=4
