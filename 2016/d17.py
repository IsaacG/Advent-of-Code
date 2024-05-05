#!/bin/python
"""Advent of Code, Day 17: Two Steps Forward. Compute the route through a maze or doors which lock and unlock."""
import collections
import hashlib
from lib import aoc

SAMPLE = [
    ('ihgpwlah', 'DDRRRD', 370),
    ('kglvqrro', 'DDUDRLRRUDRD', 492),
    ('ulqzkmiv', 'DRURDRUDDLLDLUURRDULRLDUUDDDRR', 830),
]


class Day17(aoc.Challenge):
    """Day 17: Two Steps Forward."""

    TESTS = [
        aoc.TestCase(inputs=s[0], part=1, want=s[1]) for s in SAMPLE
    ] + [
        aoc.TestCase(inputs=s[0], part=2, want=s[2]) for s in SAMPLE
    ]

    def solver(self, parsed_input: str, find_longest: bool) -> int | str:
        """Compute the route through a maze or doors which lock and unlock."""
        todo: collections.deque[tuple[str, int, int]] = collections.deque()
        todo.append(("", 0, 0))

        dirs = {"L": (-1, 0), "R": (1, 0), "D": (0, 1), "U": (0, -1)}
        doors = "UDLR"
        unlocked = "bcdef"
        longest = 0

        def options(steps) -> list[str]:
            """Return which doors are unlocked for a given set of steps taken."""
            keys = hashlib.md5((parsed_input + steps).encode()).hexdigest()[:4]
            return [door for door, key in zip(doors, keys) if key in unlocked]

        while todo:
            steps, cur_x, cur_y = todo.popleft()

            # Got to the end.
            if cur_x == 3 and cur_y == 3:
                step_count = len(steps)
                if step_count > longest:
                    longest = step_count
                if find_longest:
                    # Do not explore this path further.
                    continue
                else:
                    # Return shortest path.
                    return steps

            for option in options(steps):
                d_x, d_y = dirs[option]
                next_x, next_y = cur_x + d_x, cur_y + d_y
                # Check if the move is within the maze.
                if 0 <= next_x < 4 and 0 <= next_y < 4:
                    todo.append((steps + option, next_x, next_y))

        return longest
