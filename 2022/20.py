#!/bin/python
"""Advent of Code, Day 20: Grove Positioning System. Decrypt position data by doing list mixing."""
from __future__ import annotations

import dataclasses
from typing import Iterable, Optional

import typer
from lib import aoc

SAMPLE = """\
1
2
-3
3
-2
0
4"""

LineType = int
InputType = list[LineType]


class LinkedList(aoc.LinkedList):
    """Double linked list."""

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
    PARAMETERIZED_INPUTS = ((1, 1), (811589153, 10))

    def solver(self, parsed_input: InputType, args: tuple[int, int]) -> int:
        """Return the 1000th, 2000th, 3000th digit after mixing the list."""
        decryption_key, rounds = args
        nodelist = LinkedList.circular_list(i * decryption_key for i in parsed_input)

        self.debug(f"Node count: {len(nodelist.nodes)} == {nodelist.len}")
        for _ in range(rounds):
            nodelist.mix_nodes()

        out = nodelist.find_thousandths()
        res = sum(out)
        self.debug(f"Got {out} => {res}")
        return res


if __name__ == "__main__":
    typer.run(Day20().run)

# vim:expandtab:sw=4:ts=4
