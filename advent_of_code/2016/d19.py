#!/bin/python
"""Advent of Code, Day 19: An Elephant Named Joseph. Compute the winner of the Josephus problem."""


def solve(data: int, part: int) -> int:
    """Solve variations of the Josephus problem."""
    if part == 1:
        circle = list(range(data))
        while len(circle) > 1:
            odd = len(circle) % 2
            circle = circle[::2]
            if odd:
                circle = circle[1:]
        return circle[0] + 1

    stop = data - 1
    size = 1
    while True:
        counter = 1
        while counter <= size // 2:
            if size == stop:
                return counter
            size += 1
            counter += 1
        while counter <= size + 1:
            if size == stop:
                return counter
            size += 1
            counter += 2


TESTS = [(1, "5", 3), (2, "5", 2)]
