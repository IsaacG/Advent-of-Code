#!/bin/python
"""Advent of Code, Day 15: Timing is Everything. Determine when a hole in disks line up."""

import itertools
import math

SAMPLE = """\
Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1."""
TESTS = [(1, SAMPLE, 5)]


def solve(data: list[list[int]], part: int) -> int:
    """Return the correct time to press the button to get a capsule."""
    if part == 2:
        # Part two. Add an additional disk.
        new_disk = [data[-1][0] + 1, 11, 0, 0]
        data.append(new_disk)

    sizes = [i[1] for i in data]
    # Disk sizes must be co-prime for CRT approach.
    method = smart_solver if math.lcm(*sizes) == math.prod(sizes) else brute_force
    disks = sorted(
        (number + start, positions)
        for number, positions, _, start in data
    )
    return method(disks)


def smart_solver(disks: list[tuple[int, int]]) -> int:
    """Use a smarter algorithm to solve CRT.

    Solve one disk at a time. Once we have a good start time, t, for a disk with N positions,
    the following start times are at t + k*N. Advance until that start time works for a disk
    with M positions. Since all position counts are co-prime, the next valid time is t + k*N*M.
    We can solve one disk at a time and accumulate (product) the time steps.
    See CRT, Chinese Remainder Theorum.
    """
    start_time = 0
    step = 1
    while disks:
        # Next disk to solve.
        begin, positions = disks.pop()
        # Advance by `step`, which keeps all the other disks in position, until this disk works.
        while (begin + start_time) % positions:
            start_time += step
        # Lock this disk by updating the step.
        step *= positions
    return start_time


def brute_force(disks: list[tuple[int, int]]) -> int:
    """Brute force the solution, trying all times."""
    return next(
        time
        for time in itertools.count()
        if all(((start + time) % positions) == 0 for start, positions in disks)
    )
