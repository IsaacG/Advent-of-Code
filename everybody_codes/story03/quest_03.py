"""Everyone Codes Day N."""
from __future__ import annotations

import dataclasses
import logging
from lib import helpers
from lib import parsers

log = logging.info

@dataclasses.dataclass
class Node:
    id: str
    plug: str
    leftSocket: str
    rightSocket: str
    data: str
    left: Node | None = None
    right: Node | None = None
    leftStrong: bool | None = None
    rightStrong: bool | None = None

    def __post_init__(self) -> None:
        self.plugParts = set(self.plug.split())
        self.leftParts = set(self.leftSocket.split())
        self.rightParts = set(self.rightSocket.split())

    def add(self, n: Node | None, part: int) -> Node | None:
        if part == 1:
            if self.left is None:
                if n.plug == self.leftSocket:
                    self.left = n
                    return None
            elif self.left.add(n, part) is None:
                return None
            if self.right is None:
                if n.plug == self.rightSocket:
                    self.right = n
                    return None
            elif self.right.add(n, part) is None:
                return None
            return n
        if part == 2:
            if self.left is None:
                if n.plugParts & self.leftParts:
                    self.left = n
                    self.leftStrong = n.plug == self.leftSocket
                    return None
            elif self.left.add(n, part) is None:
                return None
            if self.right is None:
                if n.plugParts & self.rightParts:
                    self.right = n
                    self.rightStrong = n.plug == self.rightSocket
                    return None
            elif self.right.add(n, part) is None:
                return None
            return n
        if part == 3:
            log(f"Trying to connect {n.id} to {self.id}")
            if self.left is None and n.plugParts & self.leftParts:
                self.left = n
                self.leftStrong = n.plug == self.leftSocket
                return None
            if self.leftStrong is False and n.plug == self.leftSocket:
                old = self.left
                self.left = n
                self.leftStrong = True
                n = old
            elif self.left is not None:
                n = self.left.add(n, part)
                if n is None:
                    return None

            if self.right is None and n.plugParts & self.rightParts:
                self.right = n
                self.rightStrong = n.plug == self.rightSocket
                return None
            if self.rightStrong is False and n.plug == self.rightSocket:
                old = self.right
                self.right = n
                self.rightStrong = True
                return old
            elif self.right is not None:
                n = self.right.add(n, part)

            return n

    def ids(self) -> list[int]:
        got = []
        if self.left is not None:
            got.extend(self.left.ids())
        got.append(int(self.id))
        if self.right is not None:
            got.extend(self.right.ids())
        return got

    def datas(self) -> list[str]:
        got = []
        if self.left is not None:
            got.extend(self.left.datas())
        got.append(self.data)
        if self.right is not None:
            got.extend(self.right.datas())
        return got


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    parts = [
        Node(**dict(i.split("=", maxsplit=1) for i in line.split(", ")))
        for line in data
    ]
    root = parts[0]
    for i, node in enumerate(parts[1:], start=2):
        start_id = node.id
        while node is not None:
            start = node.id
            node = root.add(node, part)
            if node is not None and start == node.id:
                raise RuntimeError(f"No solution!! Tried to attach {start_id} and ended pup with {start} unable to connect.")
    # print("\n".join(root.datas()))
    return sum(i * j for i, j in enumerate(root.ids(), start=1))



PARSER = parsers.parse_one_str_per_line
TEST_DATA = [
    """\
id=1, plug=BLUE HEXAGON, leftSocket=GREEN CIRCLE, rightSocket=BLUE PENTAGON, data=?
id=2, plug=GREEN CIRCLE, leftSocket=BLUE HEXAGON, rightSocket=BLUE CIRCLE, data=?
id=3, plug=BLUE PENTAGON, leftSocket=BLUE CIRCLE, rightSocket=BLUE CIRCLE, data=?
id=4, plug=BLUE CIRCLE, leftSocket=RED HEXAGON, rightSocket=BLUE HEXAGON, data=?
id=5, plug=RED HEXAGON, leftSocket=GREEN CIRCLE, rightSocket=RED HEXAGON, data=?""",
    """\
id=1, plug=RED TRIANGLE, leftSocket=RED TRIANGLE, rightSocket=RED TRIANGLE, data=?
id=2, plug=GREEN TRIANGLE, leftSocket=BLUE CIRCLE, rightSocket=GREEN CIRCLE, data=?
id=3, plug=BLUE PENTAGON, leftSocket=BLUE CIRCLE, rightSocket=GREEN CIRCLE, data=?
id=4, plug=RED TRIANGLE, leftSocket=BLUE PENTAGON, rightSocket=GREEN PENTAGON, data=?
id=5, plug=RED PENTAGON, leftSocket=GREEN CIRCLE, rightSocket=GREEN CIRCLE, data=?""",
    """\
id=1, plug=RED TRIANGLE, leftSocket=RED TRIANGLE, rightSocket=RED TRIANGLE, data=?
id=2, plug=GREEN TRIANGLE, leftSocket=BLUE CIRCLE, rightSocket=GREEN CIRCLE, data=?
id=3, plug=BLUE PENTAGON, leftSocket=BLUE CIRCLE, rightSocket=GREEN CIRCLE, data=?
id=4, plug=RED TRIANGLE, leftSocket=BLUE PENTAGON, rightSocket=GREEN PENTAGON, data=?
id=5, plug=RED PENTAGON, leftSocket=GREEN CIRCLE, rightSocket=GREEN CIRCLE, data=?""",
    """\
id=1, plug=RED TRIANGLE, leftSocket=BLUE TRIANGLE, rightSocket=GREEN TRIANGLE, data=?
id=2, plug=GREEN TRIANGLE, leftSocket=BLUE CIRCLE, rightSocket=GREEN CIRCLE, data=?
id=3, plug=BLUE PENTAGON, leftSocket=BLUE CIRCLE, rightSocket=GREEN CIRCLE, data=?
id=4, plug=RED TRIANGLE, leftSocket=BLUE PENTAGON, rightSocket=GREEN PENTAGON, data=?
id=5, plug=BLUE TRIANGLE, leftSocket=GREEN CIRCLE, rightSocket=RED CIRCLE, data=?
id=6, plug=BLUE TRIANGLE, leftSocket=GREEN CIRCLE, rightSocket=RED CIRCLE, data=?""",
]
TESTS = [
    (1, TEST_DATA[0], 43),
    (2, TEST_DATA[1], 50),
    (3, TEST_DATA[2], 38),
    (3, TEST_DATA[3], 60),
]

if __name__ == "__main__":
    helpers.run_solution(globals())
