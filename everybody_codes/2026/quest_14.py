"""Everyone Codes Event 2026 Day N."""

import copy
import queue
import collections
import itertools
import logging
import platform

try:
    from lib import helpers
    from lib import parsers
except ModuleNotFoundError as e:
    if platform.python_implementation() != "PyPy":
        raise

log = logging.info

def solve(part: int, data: str, testing) -> int:
    """Solve the parts."""
    l = len(data.chars)
    log(l)
    total = 0
    edge_length = collections.defaultdict(lambda: collections.defaultdict(int))
    for pos, char in data.chars.items():
        for n in helpers.neighbors_t(*pos):
            edge_length[char][data.chars.get(n, "FRAME")] += 1

    if part == 1:
        total = 0
        for i, n in edge_length.items():
            for j, size in n.items():
                if i > j or j == "FRAME":
                    total += size
        return total

    def cost(edge_length):
        # Prim's Algorithm
        graph = {"FRAME": 0}
        q = queue.PriorityQueue()
        for i, j in edge_length.items():
            if "FRAME" in j:
                q.put((j["FRAME"], i))
        while not q.empty():
            cost, dst = q.get()
            if dst in graph:
                continue
            graph[dst] = cost
            for n, extra in edge_length[dst].items():
                if n in graph:
                    continue
                q.put((extra, n))
        # print(graph)
        return sum(graph.values())

    best = cost(edge_length)
    if part < 3:
        return best

    for a, b in itertools.combinations(edge_length, r=2):
        mod = copy.deepcopy(edge_length)
        for i in [a, b]:
            for j in mod[i]:
                mod[i][j] = 0
            for j in mod:
                if i in mod[j]:
                    mod[j][i] = 0
        got = cost(mod)
        log("Cost %d with %s", got, (a, b))
        best = min(best, got)
    """
    SOLVE 14.3  13.195  s ---> 1734
    {'correct': False, 'lengthCorrect': True, 'firstCorrect': True, 'penaltyUntil': 1794529224278, 'penaltyLeftMs': 60000}
    """
    if not testing:
        assert best not in {1734}
    return best








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
