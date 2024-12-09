#!/bin/python
"""Advent of Code, Day 22: Monkey Map. Wander a wrapped map to find a final location."""

import collections
import functools
from typing import Type

from lib import aoc

SAMPLE = """\
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

10R5L5R10L4R5L5"""

InputType = tuple[dict[complex, str], str]
OPEN = "."
WALL = "#"
EMPTY = " "


class Mapper:
    """Base class, handles navigating a map."""

    def __init__(self, points: dict[complex, str]) -> None:
        """Initialize."""
        self.points = points
        start_x = min(p.real for p in points if p.imag == 0 and points[p] == OPEN)
        self.start = complex(start_x, 0)

    def get_next(self, cur_position: complex, cur_dir: complex) -> tuple[complex, complex]:
        """Return the next position and direction for a move."""
        raise NotImplementedError


class FlatMap(Mapper):
    """Navigate a flat map with edge-wrapping."""

    @functools.cache
    def get_next(self, cur_position: complex, cur_dir: complex) -> tuple[complex, complex]:
        """Return the next position and direction."""
        points = self.points
        next_position = cur_position + cur_dir
        # If we run off the edge, try wrapping.
        if points.get(next_position, EMPTY) == EMPTY:
            # Flip directions and try to move to the far edge.
            rev_dir = -1 * cur_dir
            next_position = cur_position
            while next_position + rev_dir in points and points[next_position + rev_dir] != EMPTY:
                next_position += rev_dir

        # If we hit a wall, stay in place. Otherwise, advance.
        if points[next_position] == WALL:
            return cur_position, cur_dir
        return next_position, cur_dir


class CubeMap(Mapper):
    """Fold and navigate a cube map with edge-wrapping."""

    def __init__(self, points: dict[complex, str]) -> None:
        """Initialize."""
        super().__init__(points)

        # The grid is 3x4 or 3x5 faces. Use the min to find the size of each face.
        board_width = int(max(point.real for point in points)) + 1
        board_height = int(max(point.imag for point in points)) + 1
        size_of_faces = min(board_width, board_height) // 3

        face_top_left = self.compute_tiles(points, size_of_faces, board_height, board_width)
        self.transitions = self.compute_transitions(size_of_faces, face_top_left)
        self.egress_corners = self.compute_egress_corners(face_top_left, size_of_faces)
        self.face_map = self.compute_face_map(face_top_left, size_of_faces)

    def compute_tiles(
        self,
        points: dict[complex, str],
        size_of_faces: int,
        board_height: int,
        board_width: int,
    ) -> dict[int, complex]:
        """Return tile faces and their top left corner."""
        face = 0
        face_top_left = {}
        for y_pos in range(0, board_height, size_of_faces):
            for x_pos in range(0, board_width, size_of_faces):
                if points.get(complex(x_pos, y_pos), EMPTY) != EMPTY:
                    face_top_left[face] = complex(x_pos, y_pos)
                    face += 1
        return face_top_left

    def compute_transitions(
        self,
        size_of_faces: int,
        face_top_left: dict[int, complex],
    ) -> dict[int, dict[complex, tuple[int, complex]]]:
        """Build a map of edge transitions."""
        transitions: dict[int, dict[complex, tuple[int, complex]]] = {i: {} for i in face_top_left}

        # any_corner_to_face maps a corner to all the faces touching that corner on the flat map.
        any_corner_to_face = collections.defaultdict(set)
        for face, top_left in face_top_left.items():
            for offset in (0, 1, 1j, 1 + 1j):
                any_corner_to_face[top_left + offset * size_of_faces].add(face)

        # Reverse the mapping to find a face from a corner.
        top_left_to_face = {top_left: face for face, top_left in face_top_left.items()}
        # Stitch edges, build up the transition map. Track edges to explore further.
        edges_todo = set()
        for face, top_left in face_top_left.items():
            for direction in (1, -1, 1j, -1j):
                neighboring_corner = top_left + size_of_faces * direction
                if neighboring_corner in top_left_to_face:
                    other = top_left_to_face[neighboring_corner]
                    transitions[face][direction] = (other, direction)
                    edges_todo.add((face, other, direction, direction))

        # Map a given ingress direction, to the relevant corners of the face.
        # If entering from tne top, the relevant corners are top left, top right.
        # If entering from tne left (dir=right), the relevant corners are top left, bottom left.
        corners_of_interest = {
            1j: (0, size_of_faces),
            -1: (size_of_faces, size_of_faces + size_of_faces * 1j),
            -1j: (size_of_faces + size_of_faces * 1j, size_of_faces * 1j),
            1: (size_of_faces * 1j, 0),
        }

        # Explore all edges to discover additional edges to stitch.
        while edges_todo:
            face, via, direction, dir_face_via_ingress = edges_todo.pop()
            # Faces already attached.
            attached_to_face = {other for other, _ in transitions[face].values()}

            # Corners to explore, attatched to "via" and part of this edge.
            offsets = corners_of_interest[dir_face_via_ingress]
            for offset in offsets:
                corner = face_top_left[via] + offset
                unattached = any_corner_to_face[corner] - set([face]) - attached_to_face
                if not unattached:
                    continue

                # Stitch `other` onto `face`, connected through `via`.
                other = unattached.pop()

                # Four directions: face to via, via to other, via from face, other from via.
                dir_face_via_egress = next(d for d, n in transitions[face].items() if n[0] == via)
                dir_via_other_egress = next(d for d, n in transitions[via].items() if n[0] == other)

                dir_face_via_ingress = transitions[face][dir_face_via_egress][1]
                dir_via_other_ingress = transitions[via][dir_via_other_egress][1]

                rot_via_other = dir_via_other_ingress / dir_via_other_egress

                # Use the transitions face to via and via to other to compute face to via.
                rot_face_other = (dir_via_other_egress / dir_face_via_ingress)
                dir_face_other_egress = dir_face_via_egress * rot_face_other
                dir_face_other_ingress = rot_via_other * dir_face_via_ingress

                # Stitch the edges in both direction.
                transitions[face][dir_face_other_egress] = (other, dir_face_other_ingress)
                transitions[other][-dir_face_other_ingress] = (face, -dir_face_other_egress)
                # Add the edges to explore further.
                edges_todo.add((face, other, dir_face_other_egress, dir_face_other_ingress))
                edges_todo.add((other, face, -dir_face_other_ingress, -dir_face_other_egress))

        assert sum(len(t) for t in transitions.values()) == 24
        return transitions

    def compute_egress_corners(
        self, face_top_left: dict[int, complex], size_of_faces: int,
    ) -> dict[tuple[int, complex], complex]:
        """Return the egress corners for each face."""
        # The four corners of each face, used to compute
        # the egress/ingress offset relative to a corner.
        corners = {}
        for number, top_left in face_top_left.items():
            corners[number] = (
                top_left,
                top_left + size_of_faces - 1,  # top right
                top_left + complex(size_of_faces - 1, size_of_faces - 1),  # bottom right
                top_left + complex(0, size_of_faces - 1),  # bottom left
            )

        # Map movement direction to the relative "left" corner on face egress.
        # Up: top_left, Right: top_right, Down: bottom_right, Left: bottom_left
        # Find the offset from the egress corner, 1j from the egress direction.
        return {
            (number, -1j * 1j ** i): options[i]
            for i in range(4)
            for number, options in corners.items()
        }

    def compute_face_map(
        self, face_top_left: dict[int, complex], size_of_faces: int,
    ) -> dict[complex, int]:
        """Return a map of position to face."""
        # The lookup can also be done by comparing points to the corners
        # but a static map is faster.
        face_map = {}
        for number, top_left in face_top_left.items():
            face_map.update({
                top_left + complex(x, y): number
                for x in range(size_of_faces)
                for y in range(size_of_faces)
            })
        return face_map

    @functools.cache
    def get_next(self, cur_position: complex, cur_dir: complex) -> tuple[complex, complex]:
        """Return the next position and direction."""
        next_dir = cur_dir
        cur_face = self.face_map[cur_position]
        next_position = cur_position + cur_dir
        next_face = self.face_map.get(next_position)

        # If we wander off the face, figure out the new face and position.
        if cur_face != next_face or self.points.get(next_position, EMPTY) == EMPTY:
            # We're moving from one face to another!
            next_face, next_dir = self.transitions[cur_face][cur_dir]

            # Up: top_left, Right: top_right, Down: bottom_right, Left: bottom_left
            egress_corner = self.egress_corners[cur_face, cur_dir]
            # Ingress is rotated..
            # Right: top_left, Down: top_right, Left: bottom_right, Up: bottom_left
            ingress_corner = self.egress_corners[next_face, next_dir * -1j]
            offset = abs(egress_corner - cur_position)
            next_position = ingress_corner + offset * next_dir * 1j

        if self.points[next_position] == WALL:
            return cur_position, cur_dir
        return next_position, next_dir


class Day22(aoc.Challenge):
    """Day 22: Monkey Map."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=6032),
        aoc.TestCase(inputs=SAMPLE, part=2, want=5031),
    ]
    INPUT_PARSER = aoc.ParseBlocks([aoc.CoordinatesParser(), aoc.parse_re_findall_str(r"(L|R|\d+)")])

    def solver(self, puzzle_input: InputType, part_one: bool) -> int:
        """Return the final location after wandering the map."""
        points, instructions = puzzle_input
        map_class = FlatMap if part_one else CubeMap
        mapper = map_class(points.chars)

        pos = mapper.start
        direction = complex(1, 0)
        for instruction in instructions[0]:
            match instruction:
                case "R":
                    direction *= 1j
                case "L":
                    direction *= -1j
                case _:
                    for i in range(int(instruction)):
                        pos, direction = mapper.get_next(pos, direction)

        final_x = int(pos.real) + 1
        final_y = int(pos.imag) + 1
        final_d = {1j ** i: i for i in range(4)}[direction]
        score = 1000 * final_y + 4 * final_x + final_d
        return score
