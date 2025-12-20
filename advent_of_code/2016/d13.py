#!/bin/python
"""Advent of Code, Day 13: A Maze of Twisty Little Cubicles. Walk a cubicle maze."""
import collections
from lib import aoc


def solve(data: int, part: int, testing: bool) -> int | str:
    """Walk a cubicle maze."""
    want = complex(7, 4) if testing else complex(31, 39)
    # Calculate where the walls are vs open space.
    size = 60
    space = {
        complex(x, y)
        for x in range(size)
        for y in range(size)
        if (x*x + 3*x + 2*x*y + y + y*y + data).bit_count() % 2 == 0
    }

    # Initialize.
    todo: collections.deque[tuple[int, complex]] = collections.deque()
    todo.append((0, complex(1, 1)))
    seen = {complex(1, 1)}

    # Breadth first search.
    while todo:
        steps, cur = todo.popleft()
        # Part one: return step count when we get to a coordinate.
        if part == 1 and cur == want:
            return steps
        steps += 1
        # Step two: return the number of locations visited in 50 moves.
        if steps == 50:
            return len(seen) + 1
        for direction in aoc.FOUR_DIRECTIONS:
            new = cur + direction
            if new in space and new not in seen:
                todo.append((steps, new))
                seen.add(new)

    raise RuntimeError("No solution found.")


TESTS = [(1, "10", 11)]
