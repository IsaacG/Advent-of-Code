#!/bin/python
"""Advent of Code, Day 18: Lavaduct Lagoon."""
from __future__ import annotations

import collections
import functools
import itertools
import more_itertools
import math
import re

from lib import aoc

UP, DOWN, RIGHT, LEFT = aoc.FOUR_DIRECTIONS
SAMPLE = [
    """\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)""",  # 0
    'U',  # 1
    'D',  # 2
    'L',  # 3
    'R',  # 4
    '#',  # 5
    '.',  # 6
    """\
#######
#.....#
###...#
..#...#
..#...#
###.###
#...#..
##..###
.#....#
.######""",  # 7
    """\
#######
#######
#######
..#####
..#####
#######
#####..
#######
.######
.######""",  # 8
]

LineType = int
InputType = list[LineType]


class Day18(aoc.Challenge):
    """Day 18: Lavaduct Lagoon."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=62),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=952408144115),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    # INPUT_PARSER = aoc.parse_one_str_per_line
    # INPUT_PARSER = aoc.parse_one_str
    # INPUT_PARSER = aoc.parse_one_int
    # INPUT_PARSER = aoc.parse_one_str_per_line
    # INPUT_PARSER = aoc.parse_one_int_per_line
    INPUT_PARSER = aoc.parse_multi_str_per_line
    # INPUT_PARSER = aoc.parse_re_group_str(r"(a) .* (b) .* (c)")
    # INPUT_PARSER = aoc.parse_re_findall_str(r"(a|b|c)")
    # INPUT_PARSER = aoc.parse_multi_int_per_line
    # INPUT_PARSER = aoc.parse_re_group_int(r"(\d+)")
    # INPUT_PARSER = aoc.parse_re_findall_int(r"\d+")
    # INPUT_PARSER = aoc.parse_multi_mixed_per_line
    # INPUT_PARSER = aoc.parse_re_group_mixed(r"(foo) .* (\d+)")
    # INPUT_PARSER = aoc.parse_re_findall_mixed(r"\d+|foo|bar")
    # INPUT_PARSER = aoc.ParseBlocks([aoc.parse_one_str_per_line, aoc.parse_re_findall_int(r"\d+")])
    # INPUT_PARSER = aoc.ParseOneWord(aoc.Board.from_int_block)
    # INPUT_PARSER = aoc.parse_ascii_bool_map("#")

    def part1(self, parsed_input: InputType) -> int:
        position = complex(0)
        dug = {position}
        for direction, distance, color in parsed_input:
            offset = {"R": aoc.RIGHT, "L": aoc.LEFT, "U": aoc.UP, "D": aoc.DOWN}[direction]
            for i in range(int(distance)):
                position += offset
                dug.add(position)

        todo = {complex(1, 1)}
        interior = set()
        while todo:
            cur = todo.pop()
            interior.add(cur)
            for n in aoc.neighbors(cur):
                if n not in interior and n not in dug:
                    todo.add(n)
        return len(interior) + len(dug)


        return 0

    def part2(self, parsed_input: InputType) -> int:
        position = complex(0)
        vert, horiz = set(), set()
        prior_d = 0
        dug_size = 0
        for _, _, color in parsed_input:
            color = color.strip("()#")
            distance = int(color[:-1], 16)
            name = {"0": "R", "2": "L", "3": "U", "1": "D"}[color[-1]]
            offset = {"0": aoc.RIGHT, "2": aoc.LEFT, "3": aoc.UP, "1": aoc.DOWN}[color[-1]]
            assert prior_d != offset and prior_d != -offset
            prior_d = offset
            print(color, name, distance)
            start = position
            end = position + offset * distance
            dug_size += distance
            position = end

            if offset in (UP, DOWN):
                if start.imag > end.imag:
                    start, end = end, start
                vert.add((start, end))
            else:
                if start.real > end.real:
                    start, end = end, start
                horiz.add((start, end))

        assert position == complex(0)

        count = 0
        y_points = sorted({int(p.imag) for ps in vert for p in ps})
        x_points = sorted({int(p.real) for ps in vert for p in ps})
        # print("x-values", x_points)
        # print("y-values", y_points)
        # print("vert", vert)
        print()
        for start_y, end_y in zip(y_points, y_points[1:]):
            open_ranges = [
                int(start.real) for (start, end) in vert
                if start.imag <= start_y and end_y <= end.imag
            ]
            open_ranges.sort()
            # print(f"OPEN {start_y=}, {end_y=}, {open_ranges}")
            for start_x, end_x in more_itertools.chunked(open_ranges, 2):
                block_size = (end_x - start_x) * (end_y - start_y)
                count += block_size
                # print(f"BLOCK ({start_x, start_y})-({end_x, end_y}) {block_size=}, {count=}")
        result = count + (dug_size // 2) + 1
        if not self.testing:
            assert result > 131431619066808
        return result




        vert_by_start = collections.deque(sorted(vert, key=lambda x: (x[0].imag, x[0].real)))
        vert_by_end = collections.deque(sorted(vert, key=lambda x: (x[1].imag, x[1].real)))
        print(f"{vert_by_start=}")
        pending = []
        open_ranges = []
        count = 0
        y = 0
        all_y_vals = collections.deque(sorted(p.imag for start, end in vert for p in (start, end)))
        while vert_by_start or vert_by_end:
            while vert_by_start and vert_by_start[0][0].imag <= y:
                start, end = vert_by_start.popleft()
                want_y = all_y_vals.popleft()
                assert want_y == start.imag
                open_ranges.append((start, end))

            x_points = sorted(int(p[0].real) for p in open_ranges)
            y_points = sorted(int(p[0].imag) for p in open_ranges)
            assert len(x_points) % 2 == 0
            print(f"{open_ranges=}, {x_points=}")
            for start_x, end_x in itertools.batched(x_points, 2):
                assert end_x > start_x
                count += end_x - start_x + 1
            print(f"{open_ranges=}, {x_points=}")


            return





        raise NotImplementedError

    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        raise NotImplementedError

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return super().input_parser(puzzle_input)
        return puzzle_input.splitlines()
        return puzzle_input
        return [int(i) for i in puzzle_input.splitlines()]
        mutate = lambda x: (x[0], int(x[1])) 
        return [mutate(line.split()) for line in puzzle_input.splitlines()]
        # Words: mixed str and int
        return [
            tuple(
                int(i) if i.isdigit() else i
                for i in line.split()
            )
            for line in puzzle_input.splitlines()
        ]
        # Regex splitting
        patt = re.compile(r"(.*) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.")
        return [
            tuple(
                int(i) if i.isdigit() else i
                for i in patt.match(line).groups()
            )
            for line in puzzle_input.splitlines()
        ]

# vim:expandtab:sw=4:ts=4
