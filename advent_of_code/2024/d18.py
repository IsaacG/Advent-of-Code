#!/bin/python
"""Advent of Code, Day 18: RAM Run."""

import queue
from lib import aoc

SAMPLE = "5,4\n4,2\n4,5\n3,0\n2,1\n6,3\n2,4\n1,5\n0,6\n3,3\n2,6\n5,1\n1,2\n5,5\n2,5\n6,5\n1,4\n0,4\n6,4\n1,1\n6,1\n1,0\n0,5\n1,6\n2,0"


class Day18(aoc.Challenge):
    """Day 18: RAM Run."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=22),
        aoc.TestCase(part=2, inputs=SAMPLE, want="6,1"),
    ]

    def maze_solver(self, puzzle_input: list[list[int]], steps: int) -> int | None:
        """Return the number of steps needed to complete the maze."""
        fallen = set(tuple(i) for i in puzzle_input[:steps])
        size = 7 if self.testing else 71
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

    def part1(self, puzzle_input: list[list[int]]) -> int:
        """Return the number of steps to get to the end after a fixed number of blocks have fallen."""
        num_fallen = 12 if self.testing else 1024
        if (got := self.maze_solver(puzzle_input, num_fallen)) is not None:
            return got
        raise RuntimeError("Not solved")

    def part2(self, puzzle_input: list[list[int]]) -> str:
        """Return the first block which makes solving the maze impossible."""
        low = 0
        high = len(puzzle_input)

        while low < high:
            cur = (high + low) // 2
            if self.maze_solver(puzzle_input, cur) is None:
                high = cur
            else:
                low = cur + 1
        got = ",".join(str(i) for i in puzzle_input[high - 1])
        return got

# vim:expandtab:sw=4:ts=4
