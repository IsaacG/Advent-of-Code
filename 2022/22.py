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

    def pre_run(self, parsed_input: InputType) -> None:
        """Set up some class attribs which are shared across methods."""
        points, _ = parsed_input
        self.points = points
        face_corners = {}
        # The grid is 3x4 faces. Use the min to find the size of each face.
        size = min(self.max_x, self.max_y) // 3
        width = size - 1
        # Find which of the 3x4 has a face on it.
        number = 1
        for y in range(0, self.max_y, size):
            for x_offset in range(0, self.max_x + 1, size):
                x = self.max_x - x_offset
                if points.get(complex(x, y), EMPTY) != EMPTY:
                    face_corners[number] = complex(x, y)
                    number += 1

        self.transitions = TRANSITIONS_EXAMPLE if self.testing else TRANSITIONS_INPUT
        corners_to_face = {top_left: number for number, top_left in face_corners.items()}
        transitions = {i: {} for i in face_corners}
        attachment_direction = {i: {} for i in face_corners}


        extended_corners = collections.defaultdict(set)
        for number, top_left in face_corners.items():
            for offset in (0, size, size * 1j, size + size * 1j):
                extended_corners[top_left + offset].add(number)

        edges = set()
        connected = collections.defaultdict(set)
        rotation = 1
        for number, top_left in face_corners.items():
            for direction in (1, -1, 1j, -1j):
                if top_left + size * direction in corners_to_face:
                    other = corners_to_face[top_left + size * direction]
                    transitions[number][direction] = (other, direction * rotation)
                    attachment_direction[number][other] = direction
                    edges.add((number, other, direction, rotation))
                    connected[number].add(other)

        direction_to_corner_offsets = {
            -1j: (0, size),
            1: (size, size + size * 1j),
            1j: (size + size * 1j, size * 1j),
            -1: (size * 1j, 0),
        }
        while edges:
            number, other, direction, rotation = edges.pop()
            offsets = direction_to_corner_offsets[-(direction*rotation)]
            for offset in offsets:
                corner = face_corners[other] + offset
                others = extended_corners[corner] - set([number])
                unattached = list(others - connected[number])
                attached = list(others & connected[number])
                if not unattached:
                    continue

                print(f"{number=} {corner=} {attached=} {unattached=}")
                other = unattached.pop()
                via = attached.pop()
                print(f"{connected[via]=}")
                print(f"{attachment_direction[number][via]} => {attachment_direction[via][other]}")
                other_dir = attachment_direction[number][via]

                assert transitions[number][other_dir][0] == other, f"{transitions[number][other_dir][0]} != {other}"
                transitions[number][attachment_direction[via][other]] = (other, other_dir)
                attachment_direction[number][other] = attachment_direction[via][other]
                attachment_direction[number][other] = attachment_direction[via][other]
                edges.add((number, other, attachment_direction[via][other], attachment_direction[number][via]))
                connected[number].add(other)
                assert transitions[number][attachment_direction[via][other]] == self.transitions[number][attachment_direction[via][other]]



        for number in transitions:
            print(f"{number}: {transitions[number]} ({len(transitions[number])})")
            # print(f"{number}: {self.transitions[number]} ({len(self.transitions[number])})")






        self.corners = {}
        self.face_map = {}
        for number, top_left in face_corners.items():
            self.corners[number] = (
                top_left,
                top_left + width,  # top right
                top_left + complex(width, width),  # bottom right
                top_left + width * 1j,  # bottom left
            )
            self.face_map.update({
                top_left + complex(x, y): number
                for x in range(size)
                for y in range(size)
            })

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

    def solver(self, parsed_input: InputType, part: int) -> int:
        """Return the final location after wandering the map."""
        return 0
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
        self.max_x = len(blockmap.splitlines()[0])
        self.max_y = len(blockmap.splitlines())

        instructions = re.findall(r"(L|R|\d+)", instruction_line)
        return points, instructions



if __name__ == "__main__":
    typer.run(Day22().run)

# vim:expandtab:sw=4:ts=4
