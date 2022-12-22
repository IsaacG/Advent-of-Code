#!/bin/python
"""Advent of Code, Day 22: Monkey Map."""
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

LineType = int
InputType = list[LineType]
OPEN = "."
WALL = "#"
EMPTY = " "


class Day22(aoc.Challenge):
    """Day 22: Monkey Map."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=6032),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=5031),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    def part1(self, parsed_input: InputType) -> int:
        points, dirs = parsed_input
        instructions = re.findall(r"(L|R|\d+)", dirs)
        x = min(p.real for p in points if p.imag == 0 and points[p] == OPEN)
        idx = 0

        @functools.cache
        def get_next(gncur, gndir):
            gnnxt = gncur + gndir
            if gnnxt in points:
                if points[gnnxt] == WALL:
                    return gncur
                elif points[gnnxt] == OPEN:
                    return gnnxt

            gndir *= -1
            gnnxt = gncur
            while gnnxt in points and points[gnnxt] != EMPTY:
                gnnxt += gndir
            if gnnxt not in points or points[gnnxt] == EMPTY:
                gnnxt -= gndir
            if points[gnnxt] == WALL:
                return gncur
            return gnnxt

        pos = complex(x, 0)
        direction = 1
        print(f"start, {pos=}, {direction=}")
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
            print(f"{idx=}, {instruction}, {pos=}, {direction=}")
        print(pos, direction)
        x = int(pos.real) + 1
        y = int(pos.imag) + 1
        d = {1: 0, 1j: 1, -1: 2, -1j: 3}[direction]
        score = 1000 * y + 4 * x + d
        print(x, y, d, score)
        return score




    def part2(self, parsed_input: InputType) -> int:
        if self.testing:
            faces = {
                1: (8+0j, 11+3j),
                2: (0+4j, 3+7j),
                3: (4+4j, 7+7j),
                4: (8+4j, 11+7j),
                5: (8+8j, 11+11j),
                6: (12+8j, 15+11j),
            }
            transitions = {
                1: {
                    4: (1j, 1j),
                    3: (-1, 1j),
                    2: (-1j, 1j),
                    6: (1, -1),
                },
                2: {
                    3: (1, 1),
                    1: (-1j, 1j),
                    5: (1j, -1j),
                    6: (-1, -1j),
                },
                3: {
                    1: (-1j, 1),
                    2: (-1, -1),
                    4: (1, 1),
                    5: (1j, 1),
                },
                4: {
                    1: (-1j, -1j),
                    3: (-1, -1),
                    5: (1j, 1j),
                    6: (1, 1j),
                },
                5: {
                    2: (1j, -1j),
                    3: (-1, -1j),
                    4: (-1j, -1j),
                    6: (1, 1),
                },
                6: {
                    1: (1, -1),
                    2: (1j, 1),
                    4: (-1j, -1),
                    5: (-1, -1),
                },
            }
        else:
            faces = {
                1: (100+0j, 149+49j),
                2: (50+0j, 99+49j),
                3: (50+50j, 99+99j),
                4: (50+100j, 99+149j),
                5: (0+100j, 49+149j),
                6: (0+150j, 49+199j),
            }
            transitions = {
                1: {
                    2: (-1, -1),
                    4: (1, -1),
                    3: (1j, -1),
                    6: (-1j, -1j),
                },
                2: {
                    1: (1, 1),
                    6: (-1j, 1),
                    3: (1j, 1j),
                    5: (-1, 1),
                },
                3: {
                    2: (-1j, -1j),
                    5: (-1, 1j),
                    1: (1, -1j),
                    4: (1j, 1j),
                },
                4: {
                    3: (-1j, -1j),
                    5: (-1, -1),
                    6: (1j, -1),
                    1: (1, -1),
                },
                5: {
                    6: (1j, 1j),
                    2: (-1, 1),
                    3: (-1j, 1),
                    4: (1, 1),
                },
                6: {
                    4: (1, -1j),
                    1: (1j, 1j),
                    5: (-1j, -1j),
                    2: (-1, 1j),
                },
            }
        points, dirs = parsed_input
        instructions = re.findall(r"(L|R|\d+)", dirs)
        x = min(p.real for p in points if p.imag == 0 and points[p] == OPEN)
        idx = 0

        def get_face(gf_pos):
            for gf_nm, (gf_s, gf_e) in faces.items():
                if gf_s.real <= gf_pos.real <= gf_e.real and gf_s.imag <= gf_pos.imag <= gf_e.imag:
                    return gf_nm
            raise ValueError(f"{gf_pos} not valid")

        @functools.cache
        def get_next(gncur, gndir):
            gnnxt = gncur + gndir
            if gnnxt in points and points[gnnxt] != EMPTY:
                cur_face, next_face = get_face(gncur), get_face(gnnxt)
                if cur_face == next_face:
                    if points[gnnxt] == WALL:
                        return gncur, gndir
                    elif points[gnnxt] == OPEN:
                        return gnnxt, gndir

            cur_face = get_face(gncur)
            next_face, ndir = next(
                (nf, nd) for nf, (od, nd) in transitions[cur_face].items()
                if od == gndir
            )
    
            top_left, bottom_right = faces[cur_face]
            top_right = complex(bottom_right.real, top_left.imag)
            bottom_left = complex(top_left.real, bottom_right.imag)

            relative_pos = None
            if gndir == 1:  # moving right - dist from top right
                relative_pos = gncur - top_right
            elif gndir == -1:  # moving left - dist from top left
                relative_pos = gncur - top_left
            elif gndir == 1j:  # moving down - dist from bottom left
                relative_pos = gncur - bottom_left
            elif gndir == -1j:  # moving up - dist from top left
                relative_pos = gncur - top_left
            assert relative_pos.imag == 0 or relative_pos.real == 0
            offset = relative_pos.imag or relative_pos.real

            print(f"Moving from face {cur_face} to {next_face}, old_dir={gndir}, new_dir={ndir}")

            top_left, bottom_right = faces[next_face]
            top_right = complex(bottom_right.real, top_left.imag)
            bottom_left = complex(top_left.real, bottom_right.imag)

            down_of_top_left = top_left + complex(0, offset)
            down_of_top_right = top_right + complex(0, offset)
            right_of_top_left = top_left + offset
            right_of_bottom_left = bottom_left + offset

            up_of_bottom_left = bottom_left + complex(0, -offset)
            up_of_bottom_right = bottom_right + complex(0, -offset)
            left_of_top_right = top_right - offset
            left_of_bottom_right = bottom_right - offset

            new_position = {
                (1, 1): down_of_top_left,
                (-1, -1): down_of_top_right,
                (1j, 1j): right_of_top_left,
                (-1j, -1j): right_of_bottom_left,
                (1, 1j): left_of_top_right,
                (1j, -1j): left_of_bottom_right,
                (-1j, 1j): left_of_bottom_right,
                (-1j, 1): down_of_top_left,
                (-1, 1j): right_of_top_left,
                (-1, 1): up_of_bottom_left,
                (1, -1j): right_of_bottom_left,
                (1, -1): up_of_bottom_right,
                (1j, -1): down_of_top_right,
            }[(gndir, ndir)]
            if points[new_position] == WALL:
                return gncur, gndir
            return new_position, ndir



        pos = complex(x, 0)
        direction = 1
        print(f"start, {pos=}, {direction=}")
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
            from_face = get_face(pos)
            # print(f"{idx=}, {instruction}, {pos=}, {from_face=}, {direction=}")
        print(pos, direction)
        x = int(pos.real) + 1
        y = int(pos.imag) + 1
        d = {1: 0, 1j: 1, -1: 2, -1j: 3}[direction]
        score = 1000 * y + 4 * x + d
        print(x, y, d, score)
        return score




    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        mp, dirs = puzzle_input.split("\n\n")
        points = {}
        for y, row in enumerate(mp.splitlines()):
            for x, char in enumerate(row):
                points[complex(x, y)] = char
        return points, dirs



if __name__ == "__main__":
    typer.run(Day22().run)

# vim:expandtab:sw=4:ts=4
