#!/bin/python
"""Advent of Code, Day 19: Tractor Beam."""

import collections
import intcode


def solve(data: str, part: int) -> int:
    """Solve the parts."""
    return (part1 if part == 1 else part2)(data)


def is_on(computer, x: int, y: int) -> bool:
    """Return if a given coordinate is on."""
    computer.reset()
    computer.input.extend([x, y])
    computer.run()
    return computer.output.pop() == 1


def part1(data: str) -> int:
    """Return the size of the beam."""
    computer = intcode.Computer(data)
    total = 0
    left, right, last_y = 0, 0, 0
    for y in range(50):
        # s = sum(is_on(data, x, y) for x in range(50))
        first = next(
            (
                x
                for x in range(left, min(50, left + 3 + y - last_y))
                if is_on(computer, x, y)
            ), None
        )
        if first is None:
            continue
        last_y = y
        left = first
        right = max(right, left)
        right = next(
            (
                x for x in range(right, min(50, right + 5))
                if not is_on(computer, x, y)
            ),
            50,
        ) - 1
        count = right - left + 1
        # assert s == count, f"{s=}, {count=}, {y=}"
        total += count
    return total


def part2(data: str) -> int:
    """Find where a 100x100 fits in the beam."""
    computer = intcode.Computer(data)
    left, right = 10, 10
    prior: collections.deque[tuple[int, int]] = collections.deque()
    for y in range(10, 100000):
        left = next(x for x in range(left, left + 3) if is_on(computer, x, y))
        right = max(right, left)
        right = next(x for x in range(right, right + 5) if not is_on(computer, x, y))
        prior.append((y, right))
        if len(prior) == 100:
            prior_y, prior_right = prior.popleft()
            if left + 100 <= prior_right:
                return left * 10000 + prior_y
    raise RuntimeError("No solution found.")


TESTS = list[tuple[int, int, int]]()
