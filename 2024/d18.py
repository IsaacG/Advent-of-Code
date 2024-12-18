#!/bin/python
"""Advent of Code, Day 18: RAM Run."""

# TODO: switch from complex to tuples.
# TODO: generic binary search

import queue
from lib import aoc

SAMPLE = """\
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""


class Day18(aoc.Challenge):
    """Day 18: RAM Run."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=22),
        aoc.TestCase(part=2, inputs=SAMPLE, want="6,1"),
    ]

    def maze_solver(self, puzzle_input: list[list[int]], steps: int) -> int | None:
        """Return the number of steps needed to complete the maze."""
        fallen = set(complex(*i) for i in puzzle_input[:steps])
        size = 7 if self.testing else 71
        spaces = {complex(x, y) for x in range(size) for y in range(size)}
        spaces -= fallen

        start = complex(0)
        end = complex(size - 1, size - 1)

        todo: queue.PriorityQueue[tuple[int, float, float]] = queue.PriorityQueue()
        todo.put((0, start.real, start.imag))
        seen = set()
        while not todo.empty():
            cost, x, y = todo.get()
            p = complex(x, y)
            if p == end:
                return cost
            for n in aoc.neighbors(p):
                if n in seen or n not in spaces:
                    continue
                seen.add(n)
                todo.put((cost + 1, n.real, n.imag))

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
