#!/bin/python
"""Advent of Code, Day 20: Grove Positioning System."""
from __future__ import annotations

import collections
import dataclasses
import functools
import itertools
import math
import re

import typer
from lib import aoc

SAMPLE = [
    """\
1
2
-3
3
-2
0
4""",  # 12
]

LineType = int
InputType = list[LineType]


@dataclasses.dataclass
class Node:
    val: Optional[int]
    prev: Optional[Node] = None
    next: Optional[Node] = None

    def __post_init__(self):
        if self.next:
            self.next.prev = self
        if self.prev:
            self.prev.next = self

    def __str__(self):
        return f"{self.prev.val}-{self.val}-{self.next.val}"

@dataclasses.dataclass
class LinkedList:

    def __init__(self):
        """Create a double linked list."""
        self.head = Node(None)
        self.tail = Node(None, prev=self.head)
        self.nodes = []

    def seal(self):
        """Convert the list to a circular list."""
        self.first = self.head.next
        self.last = self.tail.prev
        self.first.prev = self.last
        self.last.next = self.first
        self.len = len(self.nodes)

    def add(self, val):
        """Insert a new value at the end of the list."""
        self.nodes.append(Node(val, prev=self.tail.prev, next=self.tail))

    def find_p1(self):
        """Return the 1000th, 2000th, 3000th value after 0."""
        out = []
        cur = self.first
        while cur.val != 0:
            cur = cur.next
        for _ in range(3):
            for i in range(1000):
                cur = cur.next
            out.append(cur.val)
        return out

    def move_after(self, node, insert_after):
        """Move a node from its current location to the postion after insert_after."""
        if node == insert_after:
            return
        if node == insert_after.next:
            raise ValueError("node == insert_after")
        # Remove the node from the old location and close the gap.
        node.prev.next, node.next.prev = node.next, node.prev
        # Insert between insert_after and insert_after.next
        node.prev, node.next = insert_after, insert_after.next
        node.prev.next, node.next.prev = node, node

    def move(self, node):
        insert_after = node
        movement = node.val
        if movement >= 0:
            movement = movement % (self.len - 1)
            for _ in range(movement):
                insert_after = insert_after.next
                if insert_after == node:
                    insert_after = insert_after.next
        if movement < 0:
            movement = -(abs(movement) % (self.len - 1))
            for _ in range(abs(movement) + 1):
                insert_after = insert_after.prev
                if insert_after == node:
                    insert_after = insert_after.prev
        self.move_after(node, insert_after)

    def validate(self):
        rev_rev = self.rev()
        rev_rev.reverse()
        assert self.list() == rev_rev, f"not valid"

    def list(self):
        out = []
        cur = self.head.next
        for i in range(self.len):
            out.append(cur.val)
            cur = cur.next
        return out

    def rev(self):
        out = []
        cur = self.head.next.prev
        for i in range(self.len):
            out.append(cur.val)
            cur = cur.prev
        return out


class Day20(aoc.Challenge):
    """Day 20: Grove Positioning System."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=3),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=1623178306),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]
    DECRYPTION_KEY = 811589153

    INPUT_PARSER = aoc.parse_one_int_per_line

    def part1(self, parsed_input: InputType) -> int:
        nodelist = LinkedList()
        for i in parsed_input:
            nodelist.add(i)
        nodelist.seal()
        nodelist.validate()

        self.debug(f"Node count: {len(nodelist.nodes)} == {nodelist.len}")
        for node in nodelist.nodes:
            nodelist.move(node)
        nodelist.validate()

        out = nodelist.find_p1()
        res = sum(out)
        self.debug(f"{out} => {res}")
        return res

    def part2(self, parsed_input: InputType) -> int:
        nodelist = LinkedList()
        for i in parsed_input:
            nodelist.add(i * self.DECRYPTION_KEY)
        nodelist.seal()
        nodelist.validate()

        self.debug(f"Node count: {len(nodelist.nodes)} == {nodelist.len}")
        for _ in range(10):
            for node in nodelist.nodes:
                nodelist.move(node)
        nodelist.validate()

        out = nodelist.find_p1()
        res = sum(out)
        self.debug(f"{out} => {res}")
        return res


if __name__ == "__main__":
    typer.run(Day20().run)

# vim:expandtab:sw=4:ts=4
