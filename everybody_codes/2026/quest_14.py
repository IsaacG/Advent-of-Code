"""Everyone Codes Event 2026 Day 14."""

import collections
import copy
import itertools
import heapq
import queue

from lib import helpers


def solve(part: int, data: helpers.Map) -> int:
    """Solve the parts."""
    # Compute the border length for each section.
    border_length = collections.defaultdict(lambda: collections.defaultdict(int))
    for pos, char in data.chars.items():
        for neighbor in helpers.neighbors_t(*pos):
            border_length[char][data.chars.get(neighbor, "FRAME")] += 1

    if part == 1:
        # Sum the border from each section to its neighbors.
        return sum(
            size
            for i, neighbors in border_length.items()
            for j, size in neighbors.items()
            if i > j or j == "FRAME"
        )

    def cost(border_length: dict[str, dict[str, int]]) -> int:
        """Return the min cost to create a spanning graph.

        Prim's Algorithm.
        """
        graph = {"FRAME": 0}
        q = [
            (j["FRAME"], i)
            for i, j in border_length.items()
            if "FRAME" in j
        ]
        heapq.heapify(q)

        while q:
            cost, node = heapq.heappop(q)
            if node in graph:
                continue
            graph[node] = cost
            for neighbor, extra in border_length[node].items():
                if neighbor in graph:
                    continue
                heapq.heappush(q, (extra, neighbor))
        return sum(graph.values())

    best = cost(border_length)
    if part == 2:
        return best

    # Part 3: try every combo of nodes where the cost from each node is 0.
    for a, b in itertools.combinations(border_length, r=2):
        updated_borders = copy.deepcopy(border_length)
        for i in [a, b]:
            for j in updated_borders[i]:
                updated_borders[i][j] = 0
            for j in updated_borders:
                if i in updated_borders[j]:
                    updated_borders[j][i] = 0
        best = min(best, cost(updated_borders))
    return best


if __name__ == "__main__":
    helpers.run_solution(globals())
