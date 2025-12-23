#!/bin/python
"""Advent of Code: Day 25. Emulate two herds of sea cucumbers moving across the sea floor."""

# Set of RIGHT cucumbers, DOWN cucumbers and width, height.
InputType = tuple[set[tuple[int, int]], set[tuple[int, int]], int, int]


def solve(data: InputType, part: int) -> int:
    """Count the steps until the herds lock up and cease moving."""
    del part
    right, down, width, height = data
    herds = [(right, (1, 0)), (down, (0, 1))]

    change = True
    for step in range(500):
        if not change:
            return step
        change = False

        for i in range(2):
            herd, (dx, dy) = herds[i]
            other_herd = herds[1 - i][0]
            new_herd = herd.copy()

            for x0, y0 in herd:
                new_spot = ((x0 + dx) % width, (y0 + dy) % height)
                if new_spot not in herd and new_spot not in other_herd:
                    new_herd.remove((x0, y0))
                    new_herd.add(new_spot)
                    change = True
            herds[i] = (new_herd, (dx, dy))

    raise RuntimeError("max steps reached")


def input_parser(data: str) -> InputType:
    """Parse the input data."""
    lines = data.splitlines()
    right = {
        (x, y)
        for y, line in enumerate(lines)
        for x, val in enumerate(line)
        if val == ">"
    }
    down = {
        (x, y)
        for y, line in enumerate(lines)
        for x, val in enumerate(line)
        if val == "v"
    }
    width = len(lines[0])
    height = len(lines)
    return right, down, width, height


SAMPLE = """\
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
"""
TESTS = [(1, SAMPLE, 58)]
