#!/bin/python
"""Advent of Code, Day 13: Point of Incidence."""


def find_mirror(points: set[tuple[int, int]], point: tuple[int, int] | None) -> int | None:
    """Find the row/column around which the data is mirrored.

    Optionally take a point which must be reflected.
    """
    min_x = min(x for x, _ in points)
    min_y = min(y for _, y in points)
    max_x = max(x for x, _ in points)
    max_y = max(y for _, y in points)

    for x in range(min_x, max_x):
        shift = 2 * x + 1
        if point is not None and not min_x <= shift - point[0] <= max_x:
            continue
        if all((shift - p[0], p[1]) in points for p in points if min_x <= shift - p[0] <= max_x):
            return x + 1

    for y in range(min_y, max_y):
        shift = 2 * y + 1
        if point is not None and not min_y <= shift - point[1] <= max_y:
            continue
        if all((p[0], shift - p[1]) in points for p in points if min_y <= shift - p[1] <= max_y):
            return 100 * (y + 1)

    return None


def find_with_change(points: set[tuple[int, int]], _: None) -> int:
    """Try finding the mirror with a point toggled."""
    points = points.copy()
    min_x = min(x for x, _ in points)
    min_y = min(y for _, y in points)
    max_x = max(x for x, _ in points)
    max_y = max(y for _, y in points)
    ops = {True: [points.remove, points.add], False: [points.add, points.remove]}
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            point = (x, y)
            op_a, op_b = ops[point in points]
            # Add/compute/remove or remove/compute/add.
            op_a(point)
            mirror = find_mirror(points, point)
            op_b(point)
            if mirror:
                return mirror
    raise RuntimeError("Unsolved")


def solve(data: list[set[tuple[int, int]]], part: int) -> int:
    func = find_mirror if part == 1 else find_with_change
    return sum(func(points.coords["#"], None) for points in data)  # type: ignore


SAMPLE = """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
TESTS = [(1, SAMPLE, 405), (2, SAMPLE, 400)]
# vim:expandtab:sw=4:ts=4
