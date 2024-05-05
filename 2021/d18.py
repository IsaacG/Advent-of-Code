#!/bin/python
"""Advent of Code: Day 18."""

from __future__ import annotations
import copy
import json

from lib import aoc


SAMPLE = [
    """\
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
""",
    """\
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
]


class Node:
    """Snailfish number node.

    Every Node either contains a number of a pair of subnodes.
    The Node.is_number attribute indicates which one is the case.
    """

    subnodes: list[Node] | None
    number: int | None
    is_number: bool

    def __init__(self, data: list[int] | list[Node] | int):
        """Create a Node from data.

        Data can come in three forms:
        * A pair of Nodes.
        * A pair of lists.
        * An int.
        """
        if isinstance(data, list):
            if all(isinstance(i, Node) for i in data):
                self.subnodes = [i.copy() for i in data]
            else:
                self.subnodes = [Node(i) for i in data]
            self.is_number = False
        elif isinstance(data, int):
            self.number = data
            self.is_number = True
        else:
            raise ValueError(f"invalid Node data {data=}")

    def magnitude(self) -> int:
        """Compute the magnitutde of a Snailfish number."""
        if self.is_number:
            return self.number
        return 3 * self.subnodes[0].magnitude() + 2 * self.subnodes[1].magnitude()

    def __add__(self, other: Node) -> Node:
        """Node addition. Combine two Nodes."""
        return Node([self, other]).reduce()

    def reduce(self) -> Node:
        """Reduce this Node to proper reduced format. Return self.

        Explode the Node. If there is nothing to explode, this is a no-op.
        If there are multiple Nodes to explode, this does them all in one pass.

        Then, split any large numbers. This will split exactly zero or one nodes.
        If this splits zero nodes, the Node is reduced and nothing more is needed.
        If this splits one node, start over with explode and split.
        """
        while True:
            self.explode()
            if not self.split():
                break
        return self

    def split(self) -> bool:
        """Split a Node and return if a split took place.

        If this Node is a big number, replace it with a Node pair.
        """
        if self.is_number:
            if self.number < 10:
                return False
            self.is_number = False
            self.subnodes = [Node(self.number // 2), Node((self.number + 1) // 2)]
            return True

        return any(node.split() for node in self.subnodes)

    def explode(self, depth: int = 0) -> None:
        """Explode a Node.

        This should only be called on Nodes which are not numbers.

        If this Node has too much depth, replace it with 0 and distribute its values
        to the left and right.

        If this Node is fine, check its subnodes.

        If the left explodes, the right value is distributes to the right and the left
        is passed up to the parent to distribute to the left.
        Similarly for the right, if the right explodes, distribute the left to the left
        and the right is passed up to the parent to distribute to the right.
        """
        if depth == 4:
            self.is_number = True
            self.number = 0
            return [node.number for node in self.subnodes]

        depth += 1
        ret = []
        for side in range(2):
            if self.subnodes[side].is_number:
                ret.append(0)
            else:
                vals = self.subnodes[side].explode(depth)
                if vals[1 - side]:
                    self.add_int(vals[1 - side], side)
                ret.append(vals[side])

        return ret

    def add_int(self, value: int, direction: int) -> None:
        """Add an int value to one side.

        If we are adding a number to the right, take the right node
        then traverse down the left side until we find a number node.
        """
        current = self.subnodes[1 - direction]
        while not current.is_number:
            current = current.subnodes[direction]
        current.number += value

    def __str__(self):
        """Return a string version."""
        if self.is_number:
            return str(self.number)
        return "[" + ",".join(str(node) for node in self.subnodes) + "]"

    def copy(self):
        """Return a deep copy of self."""
        return copy.deepcopy(self)

    # def verbose_reduce(self):
    #     while self.need_explode() or self.need_split():
    #         print(f"{self} {self.need_explode()=} {self.need_split()=}")
    #         if self.need_explode():
    #             self.explode()
    #             print(f"{self} exploded")
    #         if self.need_split():
    #             self.split()
    #             print(f"{self} split")
    #     return self

    # def need_split(self):
    #     if self.is_number:
    #         return self.number > 9
    #     return any(node.need_split() for node in self.subnodes)

    # def need_explode(self, depth=0):
    #     if self.is_number:
    #         return False
    #     if depth == 4:
    #         return True
    #     return any(node.need_explode(depth + 1) for node in self.subnodes)


class Day18(aoc.Challenge):
    """Solve snailfish arithmetic."""

    TESTS = (
        aoc.TestCase(inputs="[[1,2],[[3,4],5]]", part=1, want=143),
        aoc.TestCase(inputs="[[[[1,1],[2,2]],[3,3]],[4,4]]", part=1, want=445),
        aoc.TestCase(
            inputs="[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]",
            part=1,
            want=3488
        ),
        aoc.TestCase(inputs="\n".join([f"[{i},{i}]" for i in range(1, 5)]), part=1, want=445),
        aoc.TestCase(inputs="\n".join([f"[{i},{i}]" for i in range(1, 6)]), part=1, want=791),
        aoc.TestCase(inputs="\n".join([f"[{i},{i}]" for i in range(1, 7)]), part=1, want=1137),
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=3488),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=4140),
        aoc.TestCase(inputs=SAMPLE[1], part=2, want=3993),
    )

    def part1(self, parsed_input: list[Node]) -> int:
        """Sum a list of numbers."""
        result = parsed_input[0]
        for number in parsed_input[1:]:
            result += number
        return result.magnitude()

    def part2(self, parsed_input: list[Node]) -> int:
        """Compute the max magnitude from adding any two numbers."""
        return max((a + b).magnitude() for a in parsed_input for b in parsed_input if a != b)

    def input_parser(self, puzzle_input: str) -> list[Node]:
        """Parse the input data."""
        return [Node(json.loads(line)) for line in puzzle_input.splitlines()]
