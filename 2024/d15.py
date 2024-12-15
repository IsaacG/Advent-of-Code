#!/bin/python
"""Advent of Code, Day 15: Warehouse Woes."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^""",  # 0
    """\
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<""",  # 8
    """\
#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^""",
]

LineType = int
InputType = list[LineType]


class Day15(aoc.Challenge):
    """Day 15: Warehouse Woes."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=10092),
        aoc.TestCase(part=1, inputs=SAMPLE[1], want=2028),
        # aoc.TestCase(part=2, inputs=SAMPLE[2], want=9021),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=9021),
        # aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_one_str

    def part1(self, puzzle_input: InputType) -> int:
        board, instructions = aoc.ParseBlocks([aoc.CoordinatesParser(), aoc.parse_one_str]).parse(puzzle_input)
        robot = board.coords["@"].copy().pop()
        walls = board.coords["#"]
        boxes = board.coords["O"].copy()
        instructions = [aoc.ARROW_DIRECTIONS[i] for i in instructions.replace("\n", "")]
        for idx, instruction in enumerate(instructions):
            distance = 1
            while robot + distance * instruction in boxes:
                distance += 1
            if robot + distance * instruction in walls:
                pass
            else:
                new_robot = robot + instruction
                if distance > 1:
                    boxes.remove(new_robot)
                    boxes.add(robot + distance * instruction)
                robot = new_robot
            # char_map = {robot: "@"} | {i: "O" for i in boxes} | {i: "#" for i in walls}
            # print(char_map)
            # self.tprint("\n", idx + 1)
            # self.tprint(aoc.render_char_map(char_map, board.height, board.width))

        return int(sum(b.imag * 100 + b.real for b in boxes))

    def part2(self, puzzle_input: InputType) -> int:
        puzzle_input = puzzle_input.replace("#", "##")
        puzzle_input = puzzle_input.replace("O", "[]")
        puzzle_input = puzzle_input.replace(".", "..")
        puzzle_input = puzzle_input.replace("@", "@.")
        board, instructions = aoc.ParseBlocks([aoc.CoordinatesParser(), aoc.parse_one_str]).parse(puzzle_input)
        robot = board.coords["@"].copy().pop()
        walls = board.coords["#"]
        boxes = board.coords["["].copy()
        instructions = instructions.replace("\n", "")

        # char_map = {robot: "@"} | {i: "[" for i in boxes} | {i + 1: "]" for i in boxes} | {i: "#" for i in walls}
        # self.tprint("\n", 0, "initial")
        # self.tprint(aoc.render_char_map(char_map, board.height, board.width))

        for idx, instruction in enumerate(instructions):
            direction = aoc.ARROW_DIRECTIONS[instruction]
            # Sideways pushing, box size is one.
            if direction in [1, -1]:
                wall_distance = 1
                box_distance = 1 if direction == 1 else 2
                while robot + box_distance * direction in boxes:
                    # self.tprint(f"Box at {distance * direction}. Check further.")
                    box_distance += 2
                    wall_distance += 2
                if robot + wall_distance * direction in walls:
                    pass
                else:
                    box = robot + direction * (1 if direction == 1 else 2)
                    robot += direction
                    while box in boxes:
                        boxes.remove(box)
                        boxes.add(box + direction)
                        box += 2 * direction
            else:
                pushing = {robot + direction}
                boxes_moved = set()
                while all(i not in walls for i in pushing):
                    new_pushing = set()
                    for i in pushing:
                        for j in [0, 1]:
                            if i - j in boxes:
                                boxes_moved.add(i - j)
                                new_pushing.add(i - j + direction)
                                new_pushing.add(i - j + direction + 1)
                    if new_pushing:
                        pushing = new_pushing
                    else:
                        break
                if all(i not in walls for i in pushing):
                    robot += direction
                    for box in boxes_moved:
                        boxes.remove(box)
                    for box in boxes_moved:
                        boxes.add(box + direction)

            # char_map =  {i: "[" for i in boxes} | {i + 1: "]" for i in boxes} | {i: "#" for i in walls} | {robot: "@"}
            # self.tprint("\n", idx + 1, instruction)
            # self.tprint(aoc.render_char_map(char_map, board.height, board.width))

        return int(sum(b.imag * 100 + b.real for b in boxes))

    # def solver(self, puzzle_input: InputType, part_one: bool) -> int | str:

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
