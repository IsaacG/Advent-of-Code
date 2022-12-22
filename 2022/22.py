#!/bin/python
"""Advent of Code, Day 22: Monkey Map. Wander a wrapped map to find a final location."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

import typer
from lib import aoc

SAMPLE = [
    """\
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5""",  # 0
]

InputType = tuple[dict[complex, str], str]
OPEN = "."
WALL = "#"
EMPTY = " "

# Coordinates of the top-left and bottom-right of each face.
FACES_EXAMPLE = {
    1: (8 + 0j, 11 + 3j),
    2: (0 + 4j, 3 + 7j),
    3: (4 + 4j, 7 + 7j),
    4: (8 + 4j, 11 + 7j),
    5: (8 + 8j, 11 + 11j),
    6: (12 + 8j, 15 + 11j),
}
# For each face, map exit direction to new face and new direction.
TRANSITIONS_EXAMPLE = {
    1: {
        -1: (3, 1j),
        -1j: (2, 1j),
        1: (6, -1),
        1j: (4, 1j),
    },
    2: {
        -1: (6, -1j),
        -1j: (1, 1j),
        1: (3, 1),
        1j: (5, -1j),
    },
    3: {
        -1: (2, -1),
        -1j: (1, 1),
        1: (4, 1),
        1j: (5, 1),
    },
    4: {
        -1: (3, -1),
        -1j: (1, -1j),
        1: (6, 1j),
        1j: (5, 1j),
    },
    5: {
        -1: (3, -1j),
        -1j: (4, -1j),
        1: (6, 1),
        1j: (2, -1j),
    },
    6: {
        -1: (5, -1),
        -1j: (4, -1),
        1: (1, -1),
        1j: (2, 1),
    },
}
FACES_INPUT = {
    1: (100 + 0j, 149 + 49j),
    2: (50 + 0j, 99 + 49j),
    3: (50 + 50j, 99 + 99j),
    4: (50 + 100j, 99 + 149j),
    5: (0 + 100j, 49 + 149j),
    6: (0 + 150j, 49 + 199j),
}
TRANSITIONS_INPUT = {
    1: {
        -1: (2, -1),
        -1j: (6, -1j),
        1: (4, -1),
        1j: (3, -1),
    },
    2: {
        -1: (5, 1),
        -1j: (6, 1),
        1: (1, 1),
        1j: (3, 1j),
    },
    3: {
        -1: (5, 1j),
        -1j: (2, -1j),
        1: (1, -1j),
        1j: (4, 1j),
    },
    4: {
        -1: (5, -1),
        -1j: (3, -1j),
        1: (1, -1),
        1j: (6, -1),
    },
    5: {
        -1: (2, 1),
        -1j: (3, 1),
        1: (4, 1),
        1j: (6, 1j),
    },
    6: {
        -1: (2, 1j),
        -1j: (5, -1j),
        1: (4, -1j),
        1j: (1, 1j),
    },
}
# Map movement direction to the relative "left" corner on face egress.
# Up: top_left, Right: top_right, Down: bottom_right, Left: bottom_left
EGRESS_TO_CORNER = {-1j * 1j ** i: i for i in range(4)}
# Map ingress direction to corner and offset vector.
# Right: top_left, Down: top_right, Left: bottom_right, Up: bottom_left
INGRESS_TO_CORNER = {1 * 1j ** i: i for i in range(4)}
DIRECTION_SCORE = {1j ** i: i for i in range(4)}


# TODO: validate face transitions: each face needs 4 unique ingress/egress face/directions
# TODO: validate when moving to a new face, if we spin 180 deg and move one, we return to the prior spot

class Day22(aoc.Challenge):
    """Day 22: Monkey Map."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=6032),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=5031),
    ]
    DEBUG = False
    PARAMETERIZED_INPUTS = [1, 2]

    @functools.cache
    def get_next_flat(self, cur_position: complex, cur_dir: complex) -> tuple[complex, complex]:
        """Return the next position and direction for a flat-map."""
        points = self.points
        next_position = cur_position + cur_dir
        # If we do not run off the edge...
        if next_position in points:
            # If we hit a wall, stay in place.
            if points[next_position] == WALL:
                return cur_position, cur_dir
            # If the next position is open, move there.
            elif points[next_position] == OPEN:
                return next_position, cur_dir

        # We ran off the edge of the map or into EMPTY.
        # Flip directions and try to move to the far edge.
        rev_dir = -1 * cur_dir
        next_position = cur_position
        while next_position + rev_dir in points and points[next_position + rev_dir] != EMPTY:
            next_position += rev_dir
        # If we hit a wall, stay in place.
        if points[next_position] == WALL:
            return cur_position, cur_dir
        return next_position, cur_dir

    @functools.cache
    def get_next_cube(self, cur_position, cur_dir):
        """Return the next position and direction for a cube-map."""
        points = self.points
        cur_face = self.face_map[cur_position]
        next_position = cur_position + cur_dir
        next_face = self.face_map.get(next_position)

        # If we remain on the same face, try moving in the direction one unit.
        if cur_face == next_face and next_position in points:
            if cur_face == next_face:
                if points[next_position] == WALL:
                    return cur_position, cur_dir
                elif points[next_position] == OPEN:
                    return next_position, cur_dir

        # We're moving from one face to another!
        next_face, next_dir = self.transitions[cur_face][cur_dir]
        self.debug(f"Moving from face {cur_face} to {next_face}, old_dir={cur_dir}, new_dir={next_dir}")

        # Find the offset from the egress corner, 1j from the egress direction.
        egress_corner = self.corners[cur_face][EGRESS_TO_CORNER[cur_dir]]
        offset = abs(egress_corner - cur_position)

        # Compute the position use the offset from an ingress corner.
        ingress_corner = self.corners[next_face][INGRESS_TO_CORNER[next_dir]]
        new_position = ingress_corner + offset * next_dir * 1j

        if points[new_position] == WALL:
            return cur_position, cur_dir
        return new_position, next_dir

    def pre_run(self, parsed_input: InputType) -> None:
        """Set up some class attribs which are shared across methods."""
        points, _ = parsed_input
        self.points = points
        self.faces = FACES_EXAMPLE if self.testing else FACES_INPUT
        self.transitions = TRANSITIONS_EXAMPLE if self.testing else TRANSITIONS_INPUT
        self.corners = {}
        self.face_map = {}
        for number, (top_left, bottom_right) in self.faces.items():
            top_right = complex(bottom_right.real, top_left.imag)
            bottom_left = complex(top_left.real, bottom_right.imag)
            self.corners[number] = (top_left, top_right, bottom_right, bottom_left)
            for x in range(int(top_left.real), int(bottom_right.real) + 1):
                for y in range(int(top_left.imag), int(bottom_right.imag) + 1):
                    self.face_map[complex(x, y)] = number

    def solver(self, parsed_input: InputType, part: int) -> int:
        """Return the final location after wandering the map."""
        points, instructions = parsed_input
        get_next = self.get_next_flat if part == 1 else self.get_next_cube
        start_x = min(p.real for p in points if p.imag == 0 and points[p] == OPEN)

        pos = complex(start_x, 0)
        direction = 1
        self.debug(f"start, {pos=}, {direction=}")
        for idx, instruction in enumerate(instructions):
            if instruction.isdigit():
                for i in range(int(instruction)):
                    pos, direction = get_next(pos, direction)
            elif instruction == "R":
                direction *= 1j
            elif instruction == "L":
                direction *= -1j
            else:
                raise ValueError(instruction)
            if part == 2:
                from_face = self.face_map[pos]
                self.debug(f"{idx=}, {instruction}, {pos=}, {from_face=}, {direction=}")

        final_x = int(pos.real) + 1
        final_y = int(pos.imag) + 1
        final_d = DIRECTION_SCORE[direction]
        score = 1000 * final_y + 4 * final_x + final_d
        self.debug(f"Final location (base-1): {final_x=}, {final_y=}, {direction=}, {final_d=}, {score=}")
        return score

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        blockmap, instruction_line = puzzle_input.split("\n\n")
        points = {}
        for y_offset, row in enumerate(blockmap.splitlines()):
            for x_offset, char in enumerate(row):
                points[complex(x_offset, y_offset)] = char

        instructions = re.findall(r"(L|R|\d+)", instruction_line)
        return points, instructions



if __name__ == "__main__":
    typer.run(Day22().run)

# vim:expandtab:sw=4:ts=4
