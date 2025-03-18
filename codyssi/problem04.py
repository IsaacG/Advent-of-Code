"""Codyssi Day N."""

import collections
import itertools


def solve(part: int, data: str) -> int:
    """Solve the puzzle."""
    lines = data.splitlines()
    paths = collections.defaultdict(set)
    for line in lines:
        a, _, b = line.split()
        paths[a].add(b)
        paths[b].add(a)
    if part == 1:
        return len(paths)
    if part == 2:
        locations = {"STT"}
        for _ in range(3):
            locations.update(j for i in locations.copy() for j in paths[i])
        return len(locations)

    locations = {"STT"}
    seen = locations.copy()
    total = 0
    for i in itertools.count():
        total += i * len(locations)
        locations = {j for i in locations for j in paths[i] if j not in seen}
        if not locations:
            return total
        seen.update(locations)
    raise RuntimeError("Not reachable")


TEST_DATA = """\
ADB <-> XYZ
STT <-> NYC
PLD <-> XYZ
ADB <-> NYC
JLI <-> NYC
PTO <-> ADB"""
TESTS = [
    (1, TEST_DATA, 7),
    (2, TEST_DATA, 6),
    (3, TEST_DATA, 15),
]
