"""Everyone Codes Event 2026 Day N."""

import collections
import logging
import itertools
from lib import helpers
from lib import parsers

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    # print(data)
    n = data[0]["portals"]
    connections = collections.defaultdict(set)
    for i in range(n):
        for j in range(1, 2 if part == 1 else 4):
            connections[i].add((i + j) % n)
            connections[(i + j) % n].add(i)

    distance = {0: 0}
    todo = [(0, 0)]
    while todo:
        cur, steps = todo.pop(0)
        for p in connections[cur]:
            if p not in distance:
                distance[p] = steps + 1
                todo.append((p, steps + 1))
    strain = n * sum(distance.values())
    # print("strain", strain)

    for a, b in data[1]:
        connections[a - 1].add(b - 1)
        connections[b - 1].add(a - 1)
    # print(connections)

    def tot(connections):
        total = 0
        for start in range(n):
            distance = {start: 0}
            todo = [(start, 0)]
            while todo:
                cur, steps = todo.pop(0)
                for p in connections[cur]:
                    if p not in distance:
                        distance[p] = steps + 1
                        todo.append((p, steps + 1))
            # print(start, sum(distance.values()), distance)
            total += sum(distance.values())
        return total

    if part == 1:
        total = tot(connections)
    elif part == 2:
        total = strain
        for i in range(n - 1):
            for j in range(i + 1, n):
                if j not in connections[i]:
                    connections[i].add(j)
                    connections[j].add(i)
                    total = min(total, tot(connections))
                    connections[i].remove(j)
                    connections[j].remove(i)
    else:
        assert n % 8 == 0

        conns = []
        positions = [i * n // 8 for i in range(8)]
        for pairs in itertools.permutations(positions, 8):
            p = list(pairs)
            if all(a < b for a, b in itertools.batched(p, 2)):
                conns.append(list(itertools.batched(p, 2)))

        # print("Combinations:", len(conns), n // 8)
        assert conns, positions
        assert all(len(i) == 4 for i in conns)

        total = strain
        # print("Normal strain", tot(connections))
        for offset in range(n // 8):
            for pairs in conns:
                if any(i + offset in connections[j + offset] for i, j in pairs):
                    continue
                for i, j in pairs:
                    i += offset
                    j += offset
                    connections[i].add(j)
                    connections[j].add(i)
                total = min(total, tot(connections))
                for i, j in pairs:
                    i += offset
                    j += offset
                    connections[i].remove(j)
                    connections[j].remove(i)

    # print("total", total)

    return strain - total


# PARSER = parsers.parse_one_str
TEST_DATA = [
    """\
""",
    """\
""",
    """\
""",
    """\
""",
    """\
""",
]
TESTS = [
    # (1, TEST_DATA[0], None),
    # (2, TEST_DATA[1], None),
    # (3, TEST_DATA[2], None),
]

if __name__ == "__main__":
    helpers.run_solution(globals())
