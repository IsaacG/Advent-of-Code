#!/bin/python
"""Advent of Code, Day 10: Pipe Maze."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
-L|F7
7S-7|
L|7||
-L-J|
L|-JF""",
    """\
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ""",
    """\
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........""",
    """\
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""
]

# Valid neighboring pipes from the start in each direction.
START_NEIGHBORS = {
    complex(+1, 0): "-J7",
    complex(0, -1): "|F7",
    complex(-1, 0): "-FL",
    complex(0, +1): "|JL",
}
# Rotation to apply when entering corners from either side.
ROTATE = {
    (complex(+1, 0), "J"): complex(0, -1),
    (complex(+1, 0), "7"): complex(0, +1),
    (complex(0, -1), "F"): complex(+1, 0),
    (complex(0, -1), "7"): complex(-1, 0),
    (complex(-1, 0), "F"): complex(0, +1),
    (complex(-1, 0), "L"): complex(0, -1),
    (complex(0, +1), "J"): complex(-1, 0),
    (complex(0, +1), "L"): complex(+1, 0),
}
# The replacement starting symbol based on which sides has a connecting pipe.
START_SYMBOL = {
    frozenset({complex(-1, 0), complex(+1, 0)}): "-",
    frozenset({complex(-1, 0), complex(0, -1)}): "J",
    frozenset({complex(-1, 0), complex(0, +1)}): "7",
    frozenset({complex(+1, 0), complex(0, -1)}): "L",
    frozenset({complex(+1, 0), complex(0, +1)}): "F",
    frozenset({complex(0, -1), complex(0, +1)}): "|",
}


class Day10(aoc.Challenge):
    """Day 10: Pipe Maze. Navigate a pipe maze then identify interior cells."""

    PARAMETERIZED_INPUTS = [True, False]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=4),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=8),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=1),
        aoc.TestCase(inputs=SAMPLE[2], part=2, want=4),
        aoc.TestCase(inputs=SAMPLE[3], part=2, want=8),
    ]
    INPUT_PARSER = aoc.char_map

    def solver(self, parsed_input: dict[complex, str], param: bool) -> int:
        pipes = parsed_input

        # Figure out the start position details.
        start = next(pos for pos, char in pipes.items() if char == "S")
        start_neighbors = [
            (direction, options)
            for direction, options in START_NEIGHBORS.items()
            if pipes.get(start + direction, "?") in options
        ]
        # Update the start position symbol.
        pipes[start] = START_SYMBOL[frozenset(direction for direction, _ in start_neighbors)]
        # Start in either direction.
        direction = start_neighbors[0][0]

        # Walk the loop and record each position.
        location = start + direction
        loop = {start}
        while location != start:
            loop.add(location)
            if (pipe := pipes[location]) in "J7FL":
                direction = ROTATE[direction, pipe]
            location += direction

        # Part 1: return the length of the loop.
        if param:
            return len(loop) // 2

        # Walk the board. Track if we are inside the loop (odd number of crossings).
        # If inside the loop and we find a surrounded cell, tally it up.
        min_x, min_y, max_x, max_y = aoc.bounding_coords(loop)
        count = 0
        for y in range(min_y, max_y + 1):
            # Start each line outside the loop.
            inside = False
            for x in range(min_x, max_x + 1):
                pos = complex(x, y)
                if pos in loop:
                    if pipes[pos] in "|F7":
                        # Toggle inside when crossing a pipe.
                        # Shift by a fractional percent and look at just lower junctions.
                        # If we look at right/left then crossings like LJ are incorrect.
                        inside = not inside
                elif inside:
                    count += 1
        return count

# vim:expandtab:sw=4:ts=4
