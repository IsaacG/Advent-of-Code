#!/bin/python
"""Advent of Code, Day 11: Chronal Charge. Find the subgrid with the max sum value."""


def solve(data: int, part: int) -> str:
    serial = data

    def power_level(x: int, y: int) -> int:
        rack_id = x + 10
        power = rack_id * (rack_id * y + serial)
        return ((power // 100) % 10) - 5

    grid = []
    for y in range(300):
        row = []
        for x in range(300):
            row.append(power_level(x + 1, y + 1))
        grid.append(row)

    def max_grid(size: int) -> tuple[int, int, int]:
        xgroups = []
        for row in grid:
            xrow = []
            window = sum(row[:size])
            for x in range(300 - size):
                window += row[x + size]
                xrow.append(window)
                window -= row[x]
            xgroups.append(xrow)

        ygroups = []
        for col in zip(*xgroups):
            ycol = []
            window = sum(col[:size])
            for y in range(300 - size):
                window += col[y + size]
                ycol.append(window)
                window -= col[y]
            ygroups.append(ycol)

        groups = list(zip(*ygroups))
        return max(
            (val, x, y)
            for y, row in enumerate(groups)
            for x, val in enumerate(row)
        )

    (val, x, y), size = max(
        (max_grid(size), size)
        for size in range(2, 3 if part == 1 else 100)
    )

    out = [x + 1, y + 1]
    if part == 2:
        out.append(size + 1)
    return ",".join(str(i) for i in out)


SAMPLE = ["18", "42"]
TESTS = [
    (1, "18", "33,45"),
    (1, "42", "21,61"),
    (2, "18", "90,269,16"),
    (2, "42", "232,251,12"),
]
