"""Codyssi Day N."""

import collections
import functools
import math


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    shortest = collections.defaultdict(dict)
    for line in  data.splitlines():
        src, _, dst, _, weight_s = line.split()
        weight = 1 if part == 1 else int(weight_s)
        shortest[src][src] = 0
        shortest[dst][dst] = 0
        shortest[src][dst] = weight

    nodes = set(shortest)

    if part in [1, 2]:
        # Floyd Warshal
        for k in nodes:
            for i in nodes:
                for j in nodes:
                    if k not in shortest[i] or j not in shortest[k]:
                        continue
                    if j not in shortest[i] or shortest[i][j] > shortest[i][k] + shortest[k][j]:
                        shortest[i][j] = shortest[i][k] + shortest[k][j]
        
        return math.prod(sorted(shortest["STT"].values())[-3:])

    @functools.cache
    def longest(start: str, end: str, unvisited: frozenset[str]) -> int | None:
        """Return the longest path from start to end using only unvisited. Dynamic programming."""
        # Possible paths to the end.
        distances = []
        # If there is a direct path to the end, add it.
        if end in shortest[start]:
            distances.append(shortest[start][end])

        # For all possible next-nodes that are unvisited, find the longest node to that candidate then the end.
        for candidate in shortest[start]:
            if candidate in unvisited and (l := longest(candidate, end, frozenset(unvisited - {candidate}))):
                distances.append(shortest[start][candidate] + l)
        return max(distances, default=None)

    return max(longest(i, i, frozenset(nodes - {i})) for i in nodes)


TEST_DATA = """\
STT -> MFP | 5
AIB -> ZGK | 6
ZGK -> KVX | 20
STT -> AFG | 4
AFG -> ZGK | 16
MFP -> BDD | 13
BDD -> AIB | 5
AXU -> MFP | 4
CLB -> BLV | 20
AIB -> BDD | 13
BLV -> AXU | 17
AFG -> CLB | 2"""
TESTS = [
    (1, TEST_DATA, 36),
    (2, TEST_DATA, 44720),
    (3, TEST_DATA, 18),
]
