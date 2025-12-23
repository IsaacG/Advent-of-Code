#!/bin/python
"""Advent of Code, Day 24: Never Tell Me The Odds."""
import itertools
import z3  # type: ignore

START = 200000000000000
END = 400000000000000


def solve(data: list[list[int]], part: int, testing: bool) -> int:
    """Solve the parts."""
    return (part1 if part == 1 else part2)(data, testing)


def part1(data: list[list[int]], testing: bool) -> int:
    start, end = {True: (7, 27), False: (START, END)}[testing]

    # Compute the line equation for each input. y = m * x + b
    equations = []
    for idx, (px, py, pz, vx, vy, vz) in enumerate(data):
        slope = vy / vx
        intersect = py - slope * px
        equations.append((idx, px, vx, slope, intersect))

    count = 0
    for equation_one, equation_two in itertools.product(equations, repeat=2):
        idx_one, px_one, vx_one, slope_one, intersect_one = equation_one
        idx_two, px_two, vx_two, slope_two, intersect_two = equation_two
        if idx_one >= idx_two:
            # Only compare once.
            continue
        if slope_one == slope_two:
            # Parallel lines do not intersect.
            continue
        intersect_x = (intersect_two - intersect_one) / (slope_one - slope_two)
        intersect_y = slope_one * intersect_x + intersect_one
        # Check the lines intersect inside the box and not in the past.
        if start <= intersect_x <= end and start <= intersect_y <= end:
            if ((intersect_x - px_one) >= 0) == (vx_one > 0) and ((intersect_x - px_two) >= 0) == (vx_two > 0):
                count += 1

    return count


def part2(data: list[list[int]], testing: bool) -> int:
    del testing
    x = z3.Int("x")
    y = z3.Int("y")
    z = z3.Int("z")
    vx = z3.Int("vx")
    vy = z3.Int("vy")
    vz = z3.Int("vz")
    ans = z3.Int("ans")
    solver = z3.Solver()
    for idx, (x1, y1, z1, vx1, vy1, vz1) in enumerate(data[:3]):
        time = z3.Int(f"t{idx}")
        solver.add(x1 + vx1 * time == x + vx * time)
        solver.add(y1 + vy1 * time == y + vy * time)
        solver.add(z1 + vz1 * time == z + vz * time)
    solver.add(ans == x + y + z)
    if solver.check() != z3.sat:
        raise RuntimeError("No solution found")
    return solver.model()[ans]


SAMPLE = """\
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""
TESTS = [(1, SAMPLE, 2)]
# vim:expandtab:sw=4:ts=4
