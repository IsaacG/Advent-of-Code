"""Codyssi Day N."""

import collections
import itertools
import math


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    if part in [1, 2]:
        # Floyd Warshal
        shortest = collections.defaultdict(dict)
        for line in  data.splitlines():
            src, _, dst, _, weight_s = line.split()
            weight = 1 if part == 1 else int(weight_s)
            shortest[src][src] = 0
            shortest[dst][dst] = 0
            shortest[src][dst] = weight

        nodes = set(shortest)

        for k in nodes:
            for i in nodes:
                for j in nodes:
                    if k not in shortest[i] or j not in shortest[k]:
                        continue
                    if j not in shortest[i] or shortest[i][j] > shortest[i][k] + shortest[k][j]:
                        shortest[i][j] = shortest[i][k] + shortest[k][j]
        
        return math.prod(sorted(shortest["STT"].values())[-3:])

    # Part 3: based on Floyd Warshal. Add visited tracking to avoid repeated visits to the same nodes.
    longest = collections.defaultdict(dict)
    for line in  data.splitlines():
        src, _, dst, _, weight_s = line.split()
        weight = int(weight_s)
        longest[src][src] = (0, [set()])
        longest[dst][dst] = (0, [set()])
        longest[src][dst] = (weight, [set()])

    nodes = set(longest)

    for k in nodes:
        for i in nodes:
            for j in nodes:
                if k not in longest[i] or j not in longest[k]:
                    continue
                if j not in longest[i] or longest[i][j][0] < longest[i][k][0] + longest[k][j][0]:
                    distance = longest[i][k][0] + longest[k][j][0]
                    paths = [a | b | {k} for a, b in itertools.product(longest[i][k][1], longest[k][j][1]) if a.isdisjoint(b)]
                    if paths:
                        longest[i][j] = (distance, paths)

    return max(longest[i][i][0] for i in nodes)


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
