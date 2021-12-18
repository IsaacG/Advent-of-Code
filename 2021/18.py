#!/bin/python
"""Advent of Code: Day 18."""

from __future__ import annotations
import collections
import copy
import dataclasses
import functools
import math
import re

import typer
from lib import aoc

InputType = list[int]

SAMPLE = ["""\
[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]
"""]
FULL = ("""\
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
""","""\
[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]
""", 4140)
P2 = """\
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
"""


@dataclasses.dataclass
class Node:
    left: int | Node
    right: int | Node

    @classmethod
    def from_list(cls, lst):
        assert isinstance(lst, list), lst
        assert len(lst) == 2
        l, r = lst
        if isinstance(l, list):
            l = Node.from_list(l)
        if isinstance(r, list):
            r = Node.from_list(r)

        return Node(l, r)

    def magnitude(self):
        l = self.left
        r = self.right
        if isinstance(l, Node):
            l = l.magnitude()
        if isinstance(r, Node):
            r = r.magnitude()
        return 3 * l + 2 * r

    def __add__(self, other):
        n = Node(copy.deepcopy(self), copy.deepcopy(other))
        n.reduce()
        return n

    def reduce(self):
        # print(self)
        while self.need_explode() or self.need_split():
            # print(f"{self} {self.need_explode()=} {self.need_split()=}")
            if self.need_explode():
                self.explode()
                # print(f"{self} exploded")
            else:
                self.split()
                # print(f"{self} split")

    def split(self):
        if isinstance(self.left, int) and self.left > 9:
            self.left = Node(self.left//2, (self.left+1)//2)
            return True
        if isinstance(self.left, Node):
            s = self.left.split()
            if s: return s

        if isinstance(self.right, int) and self.right > 9:
            self.right = Node(self.right//2, (self.right+1)//2)
            return True
        if isinstance(self.right, Node):
            s = self.right.split()
            if s: return s
        return False

    def need_split(self):
        for n in (self.left, self.right):
            if isinstance(n, int) and n > 9:
                return True
        for n in (self.left, self.right):
            if isinstance(n, Node) and n.need_split():
                return True
        return False

    def add_int_left(self, val):
        if isinstance(self.left, int):
            self.left += val
        else:
            c = self.left
            while isinstance(c, Node) and isinstance(c.right, Node):
                c = c.right
            c.right += val

    def add_int_right(self, val):
        if isinstance(self.right, int):
            self.right += val
        else:
            c = self.right
            while isinstance(c, Node) and isinstance(c.left, Node):
                c = c.left
            c.left += val

    def explode(self, depth=0):
        if depth == 3:
            if isinstance(self.left, Node):
                l, r = self.left.left, self.left.right
                self.left = 0
                self.add_int_right(r)
                return True, l, 0
            if isinstance(self.right, Node):
                l, r = self.right.left, self.right.right
                self.right = 0
                self.add_int_left(l)
                return True, 0, r

        if isinstance(self.left, Node):
            exploded, l, r = self.left.explode(depth+1)
            if exploded and r:
                self.add_int_right(r)
            if exploded:
                return exploded, l, 0
        if isinstance(self.right, Node):
            exploded, l, r = self.right.explode(depth+1)
            if exploded and l:
                self.add_int_left(l)
            if exploded:
                return exploded, 0, r
        return False, 0, 0
        
    def need_explode(self, depth=0):
        if depth == 4:
            return True
        return (
            (isinstance(self.left, Node) and self.left.need_explode(depth + 1))
            or
            (isinstance(self.right, Node) and self.right.need_explode(depth + 1))
        )

    def __str__(self):
        return f"[{self.left},{self.right}]"
        


class Day18(aoc.Challenge):

    DEBUG = True

    TESTS = (
        # aoc.TestCase(inputs="[[1,2],[[3,4],5]]", part=1, want=143),
        # aoc.TestCase(inputs="[[[[1,1],[2,2]],[3,3]],[4,4]]", part=1, want=445),
        # aoc.TestCase(inputs="[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", part=1, want=3488),
        # aoc.TestCase(inputs="[[[[[9,8],1],2],3],4]", part=1, want=548),
        # aoc.TestCase(inputs="\n".join([f"[{i},{i}]" for i in range(1,5)]), part=1, want=445),
        # aoc.TestCase(inputs="\n".join([f"[{i},{i}]" for i in range(1,6)]), part=1, want=791),
        # aoc.TestCase(inputs="\n".join([f"[{i},{i}]" for i in range(1,7)]), part=1, want=1137),
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=3488),
        aoc.TestCase(inputs=FULL[0], part=1, want=FULL[2]),
        aoc.TestCase(inputs=P2, part=2, want=3993),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=0),
    )

    # Convert lines to type:
    INPUT_TYPES = int
    # Split on whitespace and coerce types:
    # INPUT_TYPES = [str, int]
    # Apply a transform function
    # TRANSFORM = lambda _, l: (l[0], int(l[1:]))

    def part1(self, parsed_input: InputType) -> int:
        n = parsed_input[0]
        for m in parsed_input[1:]:
            n += m
            # print(n)
        return n.magnitude()

    def part2(self, parsed_input: InputType) -> int:
        return max((a + b).magnitude() for a in parsed_input for b in parsed_input if a != b)

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return [Node.from_list(eval(line)) for line in puzzle_input.splitlines()]



if __name__ == "__main__":
    # a = Node.from_list([[[[7,7],[7,8]],[[9,5],[8,0]]],[[[9,10],20],[8,[9,0]]]])
    # print(a)
    # a.split()
    # print(a)
    typer.run(Day18().run)

# vim:expandtab:sw=4:ts=4
