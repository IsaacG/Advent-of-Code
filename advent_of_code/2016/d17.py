#!/bin/python
"""Advent of Code, Day 17: Two Steps Forward. Compute the route through a maze or doors which lock and unlock."""
import collections
import hashlib


def solve(data: str, part: int) -> int | str:
    """Compute the route through a maze or doors which lock and unlock."""
    todo: collections.deque[tuple[str, int, int]] = collections.deque()
    todo.append(("", 0, 0))
    find_longest = part == 2

    dirs = {"L": (-1, 0), "R": (1, 0), "D": (0, 1), "U": (0, -1)}
    doors = "UDLR"
    unlocked = "bcdef"
    longest = 0

    def options(steps) -> list[str]:
        """Return which doors are unlocked for a given set of steps taken."""
        keys = hashlib.md5((data + steps).encode()).hexdigest()[:4]
        return [door for door, key in zip(doors, keys) if key in unlocked]

    while todo:
        steps, cur_x, cur_y = todo.popleft()

        # Got to the end.
        if cur_x == 3 and cur_y == 3:
            longest = max(longest, len(steps))
            if find_longest:
                # Do not explore this path further.
                continue
            # Return shortest path.
            return steps

        for option in options(steps):
            d_x, d_y = dirs[option]
            next_x, next_y = cur_x + d_x, cur_y + d_y
            # Check if the move is within the maze.
            if 0 <= next_x < 4 and 0 <= next_y < 4:
                todo.append((steps + option, next_x, next_y))

    return longest


TESTS = [
    (1, 'ihgpwlah', 'DDRRRD'),
    (1, 'kglvqrro', 'DDUDRLRRUDRD'),
    (1, 'ulqzkmiv', 'DRURDRUDDLLDLUURRDULRLDUUDDDRR'),
    (2, 'ihgpwlah', 370),
    (2, 'kglvqrro', 492),
    (2, 'ulqzkmiv', 830),
]
