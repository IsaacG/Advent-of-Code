"""Everyone Codes Day N."""
from __future__ import annotations

import dataclasses
import logging
from lib import helpers
from lib import parsers

log = logging.info


@dataclasses.dataclass
class Socket:
    description: str
    node: Node | None = None
    strong: bool = False

    def __post_init__(self) -> None:
        self.parts = set(self.description.split())

    def ids(self) -> list[int]:
        if self.node is None:
            return []
        return self.node.ids()

    def plug(self, node: Node) -> Node | None:
        old = self.node
        self.node = node
        self.strong = self.strong_match(node)
        return old

    def strong_match(self, node: Node) -> bool:
        return self.description == node.plug

    def weak_match(self, node: Node) -> bool:
        return bool(self.parts & node.plug_parts)


class Node:

    def __init__(self, id_: str, plug: str, *sockets: str):
        self.id = id_
        self.plug = plug
        self.plug_parts = set(self.plug.split())
        self.sockets = [Socket(s) for s in sockets]

    def add_socket(self, n: Node | None, part: int, side: int) -> Node | None:
        """Try to connect a node to a given (left/right) socket."""
        if n is None:
            return n

        socket = self.sockets[side]
        if part < 3:
            if socket.node:
                # If the socket is occupied, traverse it.
                n = socket.node.add(n, part)
            elif socket.strong_match(n) or part == 2 and socket.weak_match(n):
                # If the socket is empty and there is a (strong/weak) match, connect.
                n = socket.plug(n)
            return n

        log(f"Trying to connect {n.id} to {self.id}")
        if not socket.node and socket.weak_match(n):
            # If the socket is empty and there is a (weak) match, plug in.
            n = socket.plug(n)
        elif not socket.strong and socket.strong_match(n):
            # If the socket is weakly matched and this node is a strong match, plug in.
            n = socket.plug(n)
        elif socket.node:
            # If we cannot plug in here, traverse down.
            n = socket.node.add(n, part)
        return n

    def add(self, n: Node | None, part: int) -> Node | None:
        # Try attaching left then right.
        for i in range(2):
            n = self.add_socket(n, part, i)
        return n

    def ids(self) -> list[int]:
        return self.sockets[0].ids() + [int(self.id)] + self.sockets[1].ids()


def solve(part: int, data: list[str]) -> int:
    """Solve the parts."""
    # Parse input into Nodes.
    details = [dict(i.split("=", maxsplit=1) for i in line.split(", ")) for line in data]
    parts = [Node(d["id"], d["plug"], d["leftSocket"], d["rightSocket"]) for d in details]
    # Take the first node as the root.
    root = parts[0]
    # Attach all other nodes.
    for i, node in enumerate(parts[1:], start=2):
        start_id = node.id
        # Loop around as needed.
        while node is not None:
            start = node.id
            node = root.add(node, part)
            if node is not None and start == node.id:
                raise RuntimeError(
                    f"No solution!! Tried to attach {start_id} and ended up with {start} unable to connect."
                )
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
