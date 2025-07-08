"""Codyssi Day 19."""

from __future__ import annotations
import collections
import dataclasses
import typing


@dataclasses.dataclass(order=True)
class Node:
    """A node in a binary tree."""

    number: int
    id: str

    def __post_init__(self) -> None:
        self.children: list[Node | None] = [None, None]

    def insert(self, other: Node) -> None:
        """Insert a node into the current (sub)tree."""
        idx = 1 if other > self else 0
        if self.children[idx] is not None:
            self.children[idx] = other
        else:
            typing.cast(Node, self.children[idx]).insert(other)

    def find_path(self, number: int) -> list[str]:
        """Return the path to a specific number."""
        idx = 1 if number > self.number else 0
        if self.children[idx] is None:
            return [self.id]
        return [self.id] + typing.cast(Node, self.children[idx]).find_path(number)

    def walk_sum(self, data: collections.defaultdict[int, int], level: int = 1) -> None:
        """Walk the tree and add the numbers at each level to a collection."""
        data[level] += self.number
        for child in self.children:
            if child is not None:
                child.walk_sum(data, level + 1)

    @classmethod
    def from_string(cls, line: str) -> Node:
        """Return a new Node from a string."""
        id_, number = line.split(" | ")
        return Node(number=int(number), id=id_)


def solve(part: int, data: str) -> int | str:
    """Solve the parts."""
    artifacts, recheck = data.split("\n\n")
    root, *rest = [Node.from_string(line) for line in artifacts.splitlines()]
    for item in rest:
        root.insert(item)

    if part == 1:
        summed: collections.defaultdict[int, int] = collections.defaultdict(int)
        root.walk_sum(summed)
        # Return the max-level-sum * the number of levels.
        return max(summed.keys()) * max(summed.values())
    if part == 2:
        # Return the path to a specific value.
        return "-".join(root.find_path(500000))
    if part == 3:
        # Find the paths to two nodes.
        one, two = [root.find_path(int(line.split(" | ")[1])) for line in recheck.splitlines()]
        # Walk one path in reverse until a common node is found in the other path.
        for node in reversed(one):
            if node in two:
                return node
    raise RuntimeError("No valid solutions.")


TEST_DATA = """\
ozNxANO | 576690
pYNonIG | 323352
MUantNm | 422646
lOSlxki | 548306
SDJtdpa | 493637
ocWkKQi | 747973
qfSKloT | 967749
KGRZQKg | 661714
JSXfNAJ | 499862
LnDiFPd | 55528
FyNcJHX | 9047
UfWSgzb | 200543
PtRtdSE | 314969
gwHsSzH | 960026
JoyLmZv | 833936

MUantNm | 422646
FyNcJHX | 9047
"""
TESTS = [
    (1, TEST_DATA, 12645822),
    (2, TEST_DATA, "ozNxANO-pYNonIG-MUantNm-lOSlxki-SDJtdpa-JSXfNAJ"),
    (3, TEST_DATA, "pYNonIG"),
]
