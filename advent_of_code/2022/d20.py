#!/bin/python
"""Advent of Code, Day 20: Grove Positioning System. Decrypt position data by doing list mixing."""
from __future__ import annotations

import dataclasses
from typing import Iterable, Optional

from lib import aoc

SAMPLE = """\
1
2
-3
3
-2
0
4"""


@dataclasses.dataclass(slots=True)
class Node:
    """Node in a double linked list."""
    val: Optional[int]
    prev: Optional[Node] = None
    next: Optional[Node] = None

    def __post_init__(self):
        """Update any neighboring nodes."""
        if self.next:
            self.next.prev = self
        if self.prev:
            self.prev.next = self


class LinkedList:
    """Double linked list."""

    first: Node
    last: Node
    len: int

    def __init__(self):
        """Create a double linked list."""
        self.head = Node(None)
        self.tail = Node(None, prev=self.head)
        self.nodes = []
        self.sealed = False

    def seal(self) -> None:
        """Convert the list to a circular list."""
        self.first = self.head.next
        self.last = self.tail.prev
        self.first.prev = self.last
        self.last.next = self.first
        self.len = len(self.nodes)
        self.sealed = True

    @classmethod
    def circular_list(cls, values: Iterable[int]) -> LinkedList:
        """Return a circular list from inputs."""
        nodelist = cls()
        for value in values:
            nodelist.add(value)
        nodelist.seal()
        return nodelist

    def add(self, val: int) -> None:
        """Insert a new value at the end of the list."""
        assert not self.sealed
        self.nodes.append(Node(val, prev=self.tail.prev, next=self.tail))

    def move_after(self, node: Node, insert_after: Node) -> None:
        """Move a node from its current location to the postion after insert_after."""
        if node == insert_after:
            return
        if node == insert_after.next:
            raise ValueError("node == insert_after")
        # Remove the node from the old location and close the gap.
        assert node.prev is not None
        assert node.next is not None
        node.prev.next, node.next.prev = node.next, node.prev
        # Insert between insert_after and insert_after.next
        node.prev, node.next = insert_after, insert_after.next
        assert node.prev is not None
        assert node.next is not None
        node.prev.next, node.next.prev = node, node

    def find_thousandths(self) -> list[int]:
        """Return the 1000th, 2000th, 3000th value after 0."""
        out: list[int] = []
        cur = self.first
        while cur.val != 0:
            cur = cur.next
        for _ in range(3):
            for _ in range(1000):
                cur = cur.next
            out.append(cur.val)
        return out

    def mix_nodes(self) -> None:
        """Move nodes by positions equal to its value."""
        modulo = self.len - 1
        for node in self.nodes:
            insert_after = node
            movement = node.val
            movement = movement % modulo if movement >= 0 else -(-movement % modulo)
            if movement >= 0:
                for _ in range(movement):
                    insert_after = insert_after.next
            if movement < 0:
                for _ in range(abs(movement) + 1):
                    insert_after = insert_after.prev
            self.move_after(node, insert_after)


class Day20(aoc.Challenge):
    """Day 20: Grove Positioning System."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=3),
        aoc.TestCase(inputs=SAMPLE, part=2, want=1623178306),
    ]

    def solver(self, puzzle_input: list[int], part_one: bool) -> int:
        """Return the 1000th, 2000th, 3000th digit after mixing the list."""
        decryption_key = 1 if part_one else 811589153
        nodelist = LinkedList.circular_list(i * decryption_key for i in puzzle_input)

        self.debug(f"Node count: {len(nodelist.nodes)} == {nodelist.len}")
        for _ in range(1 if part_one else 10):
            nodelist.mix_nodes()

        out = nodelist.find_thousandths()
        res = sum(out)
        self.debug(f"Got {out} => {res}")
        return res
