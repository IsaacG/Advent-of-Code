#!/bin/python
"""Advent of Code: Day 07. Solve the optimal positioning for crab-submarine blasting."""


def solve(data: list[int], part: int) -> int:
    """Find the location where it is cheapest for all the crabs to move."""
    positions = data
    costs = []
    # Return the optimal blast position with constant movement cost.
    # Return the optimal blast position with linear movement cost.
    func = (lambda x: x) if part == 1 else (lambda x: x * (x + 1) // 2)
    for i in range(min(positions), max(positions) + 1):
        costs.append(sum(func(abs(i - pos)) for pos in positions))
    return min(costs)


SAMPLE = "16,1,2,0,4,2,7,1,2,14"
TESTS = [(1, SAMPLE, 37), (2, SAMPLE, 168)]
