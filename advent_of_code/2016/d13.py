#!/bin/python
"""Advent of Code, Day 13: A Maze of Twisty Little Cubicles. Walk a cubicle maze."""

import collections

from lib import aoc

SAMPLE = "10"


class Day13(aoc.Challenge):
    """Day 13: A Maze of Twisty Little Cubicles."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=11),
        aoc.TestCase(inputs=SAMPLE, part=2, want=aoc.TEST_SKIP),
    ]

    def solver(self, puzzle_input: int, param: bool) -> int | str:
        """Walk a cubicle maze."""
        want = complex(7, 4) if self.testing else complex(31, 39)
        # Calculate where the walls are vs open space.
        size = 60
        space = {
            complex(x, y)
            for x in range(size)
            for y in range(size)
            if (x*x + 3*x + 2*x*y + y + y*y + puzzle_input).bit_count() % 2 == 0
        }

        # Initialize.
        todo: collections.deque[tuple[int, complex]] = collections.deque()
        todo.append((0, complex(1, 1)))
        seen = {complex(1, 1)}

        # Breadth first search.
        while todo:
            steps, cur = todo.popleft()
            # Part one: return step count when we get to a coordinate.
            if not param and cur == want:
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
