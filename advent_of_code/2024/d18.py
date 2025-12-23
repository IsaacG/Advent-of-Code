#!/bin/python
"""Advent of Code, Day 18: RAM Run."""

import queue
from lib import aoc


def maze_solver(data: list[list[int]], steps: int, testing: bool) -> int | None:
    """Return the number of steps needed to complete the maze."""
    fallen = set(tuple(i) for i in data[:steps])
    size = 7 if testing else 71
    spaces = {(x, y) for x in range(size) for y in range(size)}
    spaces -= fallen

    start = (0, 0)
    end = (size - 1, size - 1)

    todo: queue.PriorityQueue[tuple[int, tuple[int, int]]] = queue.PriorityQueue()
    todo.put((0, start))
    seen = set()
    while not todo.empty():
        cost, p = todo.get()
        if p == end:
            return cost
        for n in aoc.t_neighbors4(p):
            if n in seen or n not in spaces:
                continue
            seen.add(n)
            todo.put((cost + 1, n))

    return None


def solve(data: list[list[int]], part: int, testing: bool) -> str:
    """Return the first block which makes solving the maze impossible."""
    if part == 1:
        # Return the number of steps to get to the end after a fixed number of blocks have fallen.
        num_fallen = 12 if testing else 1024
        got = maze_solver(data, num_fallen, testing)
        if got is None:
            raise RuntimeError("Not solved")
        return got

    low = 0
    high = len(data)

    while low < high:
        cur = (high + low) // 2
        if maze_solver(data, cur, testing) is None:
            high = cur
        else:
            low = cur + 1
    got = ",".join(str(i) for i in data[high - 1])
    return got


SAMPLE = "5,4\n4,2\n4,5\n3,0\n2,1\n6,3\n2,4\n1,5\n0,6\n3,3\n2,6\n5,1\n1,2\n5,5\n2,5\n6,5\n1,4\n0,4\n6,4\n1,1\n6,1\n1,0\n0,5\n1,6\n2,0"
TESTS = [(1, SAMPLE, 22), (2, SAMPLE, "6,1")]
# vim:expandtab:sw=4:ts=4
