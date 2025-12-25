#!/bin/python
"""Advent of Code, Day 9: Marble Mania. Simulate a marble game."""
from __future__ import annotations
import dataclasses
from lib import aoc

SAMPLE = [
    "9 players; last marble is worth 25 points",
    "10 players; last marble is worth 1618 points",
    "13 players; last marble is worth 7999 points",
    "17 players; last marble is worth 1104 points",
    "21 players; last marble is worth 6111 points",
    "30 players; last marble is worth 5807 points",
]


@dataclasses.dataclass
class Node:
    """Node in a double linked list."""
    val: int
    prev: Node | None = None
    next: Node | None = None

    def __post_init__(self):
        """Update any neighboring nodes."""
        if self.next:
            self.next.prev = self
        if self.prev:
            self.prev.next = self


class Day09(aoc.Challenge):
    """Day 9: Marble Mania."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=32),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=8317),
        aoc.TestCase(inputs=SAMPLE[2], part=1, want=146373),
        aoc.TestCase(inputs=SAMPLE[3], part=1, want=2764),
        aoc.TestCase(inputs=SAMPLE[4], part=1, want=54718),
        aoc.TestCase(inputs=SAMPLE[5], part=1, want=37305),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]
    INPUT_PARSER = aoc.parse_ints

    def solver(self, puzzle_input: list[list[int]], part_one: bool) -> int:
        players, last = puzzle_input[0]
        # Multiple last value by 1 or 100 for parts 1, 2.
        last *= 1 if part_one else 100

        score = [0] * players
        cur = Node(0)
        cur.next = cur.prev = cur

        for marble in range(1, last + 1):
            if marble % 23:
                cur = Node(marble, prev=cur.next, next=cur.next.next)
            else:
                for _ in range(6):
                    cur = cur.prev
                removed = cur.prev
                score[(marble - 1) % players] += marble + removed.val
                removed.prev.next = removed.next
                removed.next.prev = removed.prev

        return max(score)
