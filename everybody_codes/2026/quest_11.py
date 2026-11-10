"""Everyone Codes Event 2026 Day N."""

import collections
import copy
import itertools
import platform

try:
    from lib import helpers
except ModuleNotFoundError as e:
    if platform.python_implementation() != "PyPy":
        raise


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    if platform.python_implementation() == "PyPy":
        a, b = data.split("\n\n")
        n = int(a.split()[-1])
        shortcuts = [[int(i) for i in line.split()] for line in b.splitlines()]
    else:
        meta, shortcuts = data
        n = meta["portals"]

    def portal_strain(portals: dict[int, set[int]]) -> int:
        """Compute the portal strain for a set of portals."""
        total = 0
        for start in range(n):
            distance = {start: 0}
            todo = [(start, 0)]
            while todo:
                portal, steps = todo.pop(0)
                for other_portal in portals[portal]:
                    if other_portal not in distance:
                        distance[other_portal] = steps + 1
                        todo.append((other_portal, steps + 1))
            total += sum(distance.values())
        return total

    # Initial connection between adjacent portals.
    portals = collections.defaultdict(set)
    for i in range(n):
        for j in [1] if part == 1 else [1, 2, 3]:
            portals[i].add((i + j) % n)
            portals[(i + j) % n].add(i)

    initial_strain = portal_strain(portals)

    for i, j in shortcuts:
        portals[i - 1].add(j - 1)
        portals[j - 1].add(i - 1)

    if part == 1:
        return initial_strain - portal_strain(portals)

    if part == 2:
        shortcut_strain = initial_strain
        pairings = [[i] for i in itertools.combinations(range(n), 2)]
        offsets = [0]
    else:
        positions = [i * n // 8 for i in range(8)]
        pairings = [
            list(itertools.batched(pairs, 2))
            for pairs in itertools.permutations(positions, 8)
            if all(a < b for a, b in itertools.batched(pairs, 2))
        ]
        offsets = range(n // 8)

    shortcut_strain = initial_strain
    for offset in range(n // 8):
        for pairs in pairings:
            configuration = copy.deepcopy(portals)
            pairs = [(i + offset, j + offset) for i, j in pairs]
            if any(i in portals[j] for i, j in pairs):
                continue
            for i, j in pairs:
                configuration[i].add(j)
                configuration[j].add(i)
            shortcut_strain = min(shortcut_strain, portal_strain(configuration))


    return initial_strain - shortcut_strain


if __name__ == "__main__":
    helpers.run_solution(globals())
