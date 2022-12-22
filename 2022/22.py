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


# TODO: validate face transitions: each face needs 4 unique ingress/egress face/directions
# TODO: validate when moving to a new face, if we spin 180 deg and move one, we return to the prior spot

class Day22(aoc.Challenge):
    """Day 22: Monkey Map."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=6032),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=5031),
    ]
    DEBUG = False

    def part1(self, parsed_input: InputType) -> int:
        points, dirs = parsed_input
        instructions = re.findall(r"(L|R|\d+)", dirs)
        x = min(p.real for p in points if p.imag == 0 and points[p] == OPEN)
        idx = 0

        @functools.cache
        def get_next(cur_position, gndir):
            next_position = cur_position + gndir
            if next_position in points:
                if points[next_position] == WALL:
                    return cur_position
                elif points[next_position] == OPEN:
                    return next_position

            gndir *= -1
            next_position = cur_position
            while next_position in points and points[next_position] != EMPTY:
                next_position += gndir
            if next_position not in points or points[next_position] == EMPTY:
                next_position -= gndir
            if points[next_position] == WALL:
                return cur_position
            return next_position

        pos = complex(x, 0)
        direction = 1
        self.debug(f"start, {pos=}, {direction=}")
        for idx, instruction in enumerate(instructions):
            if instruction.isdigit():
                for i in range(int(instruction)):
                    pos = get_next(pos, direction)
            elif instruction == "R":
                direction *= 1j
            elif instruction == "L":
                direction *= -1j
            else:
                raise ValueError(instruction)
            self.debug(f"{idx=}, {instruction}, {pos=}, {direction=}")
        x = int(pos.real) + 1
        y = int(pos.imag) + 1
        d = {1: 0, 1j: 1, -1: 2, -1j: 3}[direction]
        score = 1000 * y + 4 * x + d
        self.debug(f"Final location (base-1): {x=}, {y=}, {direction=}, {d=}, {score=}")
        return score

    def pre_run(self):
        self.faces = FACES_EXAMPLE if self.testing else FACES_INPUT
        self.corners = {}
        for number, (top_left, bottom_right) in self.faces.items():
            top_right = complex(bottom_right.real, top_left.imag)
            bottom_left = complex(top_left.real, bottom_right.imag)
            self.corners[number] = (top_left, top_right, bottom_right, bottom_left)

    def get_face(self, position: complex) -> int:
        """Given a position, return which cube face it is on."""
        faces = self.faces
        for face_number, (top_left, bottom_right) in faces.items():
            if (
                top_left.real <= position.real <= bottom_right.real
                and top_left.imag <= position.imag <= bottom_right.imag
            ):
                return face_number
        raise ValueError(f"{position} not valid")

    def part2(self, parsed_input: InputType) -> int:
        points, dirs = parsed_input
        instructions = re.findall(r"(L|R|\d+)", dirs)
        x = min(p.real for p in points if p.imag == 0 and points[p] == OPEN)
        idx = 0

        faces = self.faces
        if self.testing:
            transitions = TRANSITIONS_EXAMPLE
        else:
            transitions = TRANSITIONS_INPUT

        @functools.cache
        def get_next(cur_position, gndir):
            next_position = cur_position + gndir
            if next_position in points and points[next_position] != EMPTY:
                cur_face, next_face = self.get_face(cur_position), self.get_face(next_position)
                if cur_face == next_face:
                    if points[next_position] == WALL:
                        return cur_position, gndir
                    elif points[next_position] == OPEN:
                        return next_position, gndir

            cur_face = self.get_face(cur_position)
            next_face, next_dir = transitions[cur_face][gndir]
    
            top_left, top_right, bottom_right, bottom_left = self.corners[cur_face]
            # Map movement direction to the relative "left" corner.
            direction_to_left_corner = {
                -1: bottom_left,   # Left
                -1j: top_left,     # Up
                1: top_right,      # Right
                1j: bottom_right,  # Down
            }
            offset_v2 = abs(direction_to_left_corner[gndir] - cur_position)

            self.debug(f"Moving from face {cur_face} to {next_face}, old_dir={gndir}, new_dir={next_dir}")

            top_left, top_right, bottom_right, bottom_left = self.corners[next_face]
            ingress_mapping = {
                False: {
                    -1:  (bottom_right, -1j),  # Left
                    -1j: (bottom_left,   +1),  # Up
                    1:   (top_left,     +1j), # Right
                    1j:  (top_right,     -1), # Down
                },
                True: {
                    -1:  (bottom_right, -1j),  # Left
                    -1j: (bottom_left,   +1),  # Up
                    1:   (top_left,     +1j), # Right
                    1j:  (top_right,     -1), # Down
                }
            }
            flip = (gndir == -next_dir or gndir * -1j == next_dir)
            corner, mult = ingress_mapping[flip][next_dir]
            new_position = corner + offset_v2 * mult


            if points[new_position] == WALL:
                return cur_position, gndir
            return new_position, next_dir



        pos = complex(x, 0)
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
            from_face = self.get_face(pos)
            self.debug(f"{idx=}, {instruction}, {pos=}, {from_face=}, {direction=}")
        x = int(pos.real) + 1
        y = int(pos.imag) + 1
        d = {1: 0, 1j: 1, -1: 2, -1j: 3}[direction]
        score = 1000 * y + 4 * x + d
        self.debug(f"Final location (base-1): {x=}, {y=}, {direction=}, {d=}, {score=}")
        return score

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        blockmap, instructions = puzzle_input.split("\n\n")
        points = {}
        for y, row in enumerate(blockmap.splitlines()):
            for x, char in enumerate(row):
                points[complex(x, y)] = char
        self.points = points
        return points, instructions



if __name__ == "__main__":
    typer.run(Day22().run)

# vim:expandtab:sw=4:ts=4
