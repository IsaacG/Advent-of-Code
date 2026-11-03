"""Everyone Codes Story 1 Day 2."""

from __future__ import annotations
import collections
import collections.abc
import dataclasses


@dataclasses.dataclass
class Node:
    """A node in the tree."""
    node_id: int
    rank: int
    symbol: str
    is_root: bool = False
    children: list[Node | None] = dataclasses.field(default_factory=lambda: [None, None])

    @classmethod
    def from_text(cls, node_id: int, text: str) -> Node:
        """Build a Node from text input."""
        rank, symbol = text.split("=")[1].strip("[]").split(",")
        return Node(node_id, rank=int(rank), symbol=symbol)

    def add(self, node: Node, idx: int | None = None) -> None:
        """Add a child node."""
        assert self.is_root != (idx is None), "An index must always and only be used when adding to the root."
        if idx is None:
            idx = 0 if node.rank < self.rank else 1
        if self.children[idx] is None:
            self.children[idx] = node
        else:
            self.children[idx].add(node)

    def walk(
        self, depth: int = 1, collected: collections.defaultdict[int, list[str]] | None = None
    ) -> collections.defaultdict[int, list[str]]:
        """Walk the tree, collecting the symbols by level."""
        collected = collected or collections.defaultdict(list)
        collected[depth].append(self.symbol)
        for child in self.children:
            if child is not None:
                child.walk(depth + 1, collected)
        return collected

    def find_parents(self, node_id: int) -> collections.abc.Iterable[tuple[Node, int]]:
        """Walk the tree and yield nodes which have a child (parent node and child index) with a given node ID."""
        for idx, child in enumerate(self.children):
            if child is None:
                continue
            if child.node_id == node_id:
                yield (self, idx)
            yield from child.find_parents(node_id)

    def swap_values(self, node_id: int) -> None:
        """Swap the values contained within two nodes, identified by ID."""
        a, b = [node.children[idx] for node, idx in self.find_parents(node_id)]
        a.rank, b.rank = b.rank, a.rank
        a.symbol, b.symbol = b.symbol, a.symbol
        a.node_id, b.node_id = b.node_id, a.node_id

    def swap_branches(self, node_id: int) -> None:
        """Swap two branches which have the same node ID."""
        (p1, i1), (p2, i2) = list(self.find_parents(node_id))
        p1.children[i1], p2.children[i2] = p2.children[i2], p1.children[i1]

    def to_text(self) -> str:
        """Return tree text, extracting the longer level from both halves."""
        assert self.is_root
        return "".join(
            "".join(max(tree.walk().values(), key=len))
            for tree in self.children
        )


def solve(part: int, data: str) -> str:
    """Solve the parts."""
    root = Node(node_id=0, rank=-1, symbol="", is_root=True)

    for line in data.splitlines():
        cmd, node, *rest = line.split()
        if cmd == "ADD":
            node_id = int(node.split("=")[1])
            # Add a left and right node.
            for idx, text in enumerate(rest):
                root.add(Node.from_text(node_id, text), idx)
        elif cmd == "SWAP" and part == 2:
            root.swap_values(int(node))
        elif cmd == "SWAP" and part == 3:
            root.swap_branches(int(node))
        else:
            print(f"Unknown {cmd}, {line}")

    return root.to_text()


TEST_DATA = [
    """\
ADD id=1 left=[10,A] right=[30,H]
ADD id=2 left=[15,D] right=[25,I]
ADD id=3 left=[12,F] right=[31,J]
ADD id=4 left=[5,B] right=[27,L]
ADD id=5 left=[3,C] right=[28,M]
ADD id=6 left=[20,G] right=[32,K]
ADD id=7 left=[4,E] right=[21,N]""",
    """\
ADD id=1 left=[160,E] right=[175,S]
ADD id=2 left=[140,W] right=[224,D]
ADD id=3 left=[122,U] right=[203,F]
ADD id=4 left=[204,N] right=[114,G]
ADD id=5 left=[136,V] right=[256,H]
ADD id=6 left=[147,G] right=[192,O]
ADD id=7 left=[232,I] right=[154,K]
ADD id=8 left=[118,E] right=[125,Y]
ADD id=9 left=[102,A] right=[210,D]
ADD id=10 left=[183,Q] right=[254,E]
ADD id=11 left=[146,E] right=[148,C]
ADD id=12 left=[173,Y] right=[299,S]
ADD id=13 left=[190,B] right=[277,B]
ADD id=14 left=[124,T] right=[142,N]
ADD id=15 left=[153,R] right=[133,M]
ADD id=16 left=[252,D] right=[276,M]
ADD id=17 left=[258,I] right=[245,P]
ADD id=18 left=[117,O] right=[283,!]
ADD id=19 left=[212,O] right=[127,R]
ADD id=20 left=[278,A] right=[169,C]""",
    """\
ADD id=1 left=[10,A] right=[30,H]
ADD id=2 left=[15,D] right=[25,I]
ADD id=3 left=[12,F] right=[31,J]
ADD id=4 left=[5,B] right=[27,L]
ADD id=5 left=[3,C] right=[28,M]
SWAP 1
SWAP 5
ADD id=6 left=[20,G] right=[32,K]
ADD id=7 left=[4,E] right=[21,N]""",
    """\
ADD id=1 left=[10,A] right=[30,H]
ADD id=2 left=[15,D] right=[25,I]
ADD id=3 left=[12,F] right=[31,J]
ADD id=4 left=[5,B] right=[27,L]
ADD id=5 left=[3,C] right=[28,M]
SWAP 1
SWAP 5
ADD id=6 left=[20,G] right=[32,K]
ADD id=7 left=[4,E] right=[21,N]
SWAP 2""",
    """\
ADD id=1 left=[10,A] right=[30,H]
ADD id=2 left=[15,D] right=[25,I]
ADD id=3 left=[12,F] right=[31,J]
ADD id=4 left=[5,B] right=[27,L]
ADD id=5 left=[3,C] right=[28,M]
SWAP 1
SWAP 5
ADD id=6 left=[20,G] right=[32,K]
ADD id=7 left=[4,E] right=[21,N]
SWAP 2
SWAP 5""",
]
TESTS = [
    (1, TEST_DATA[0], "CFGNLK"),
    (1, TEST_DATA[1], "EVERYBODYCODES"),
    (2, TEST_DATA[2], "MGFLNK"),
    (3, TEST_DATA[3], "DJMGL"),
    (3, TEST_DATA[4], "DJCGL"),
]
