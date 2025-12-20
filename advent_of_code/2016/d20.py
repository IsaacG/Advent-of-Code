#!/bin/python
"""Advent of Code, Day 20: Firewall Rules. Find valid IPs between blacklisted ranges."""

def solve(data: list[tuple[int, int]], part: int, testing: bool) -> int:
    """Find valid IPs between blacklisted ranges."""
    # Set the upper limit.
    if testing:
        data.append((10, 10))
    else:
        data.append((4294967296, 4294967296))

    cur = 0
    allowed = 0
    for low, high in data:
        if low <= cur <= high:
            cur = high + 1
        elif cur < low:
            # Part 1: return the first allowed IP.
            if part == 1:
                return cur
            # Part 2: count valid IPS.
            allowed += low - cur
            cur = high + 1
    return allowed


def input_parser(puzzle_input: str) -> list[tuple[int, int]]:
    """Parse the input data."""
    return sorted(tuple(int(i) for i in line.split("-")) for line in puzzle_input.splitlines())


TESTS = [
    (1, "5-8\n0-2\n4-7", 3),
    (2, "5-8\n0-2\n4-7", 2),
]
