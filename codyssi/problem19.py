"""Codyssi Day 19."""

import collections
import logging

log = logging.info


class Node:

    def __init__(self, id_, number):
        self.id = id_
        self.number = int(number)
        self.children = [None, None]

    def add(self, other):
        if other.number > self.number:
            idx = 1
        else:
            idx = 0
        if self.children[idx] is None:
            self.children[idx] = other
        else:
            self.children[idx].add(other)

    def find_path(self, number):
        if number > self.number:
            idx = 1
        else:
            idx = 0
        if self.children[idx] is None:
            return [self.id]
        else:
            return [self.id] + self.children[idx].find_path(number)

    def walk_sum(self, data, level):
        data[level] += self.number
        for child in self.children:
            if child is not None:
                child.walk_sum(data, level + 1)


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    parts = data.split("\n\n")
    lines = parts[0].splitlines()
    items = []
    for line in lines:
        id_, number = line.split(" | ")
        node = Node(id_, int(number))
        items.append(node)
    root = items[0]
    for item in items[1:]:
        root.add(item)
    data = collections.defaultdict(int)
    root.walk_sum(data, 1)

    if part == 1:
        return max(data.keys()) * max(data.values())
    if part == 2:
        return "-".join(root.find_path(500000))
    if part == 3:
        paths = [root.find_path(int(line.split(" | ")[1])) for line in parts[1].splitlines()]

        for node in reversed(paths[0]):
            if node in paths[1]:
                return node
        return
        for i in range(len(paths[0])):
            if paths[0][i + 1] != paths[1][i + 1]:
                return paths[0][i]


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
