#!/bin/python
"""Advent of Code, Day 16: The Floor Will Be Lava."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....""",  # 5
]

LineType = int
InputType = list[LineType]
UP, DOWN, RIGHT, LEFT = complex(0, -1), complex(0, 1), complex(1), complex(-1)


class Day16(aoc.Challenge):
    """Day 16: The Floor Will Be Lava."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=46),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=51),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    # INPUT_PARSER = aoc.parse_one_str_per_line
    # INPUT_PARSER = aoc.parse_one_str
    # INPUT_PARSER = aoc.parse_one_int
    # INPUT_PARSER = aoc.parse_one_str_per_line
    # INPUT_PARSER = aoc.parse_one_int_per_line
    # INPUT_PARSER = aoc.parse_multi_str_per_line
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
    INPUT_PARSER = aoc.parse_ascii_char_map(lambda x: x)

    def part1(self, parsed_input: InputType) -> int:
        return self.energized(parsed_input, complex(-1), RIGHT)

    def energized(self, parsed_input: InputType, start_pos, start_dir) -> int:
        min_x, min_y, max_x, max_y = aoc.bounding_coords(parsed_input)
        energized = set()
        seen = set()
        beams = {(start_pos, start_dir)}
        while beams:
            new_beams = set()
            for pos, direction in beams:
                next_pos = pos + direction
                char = parsed_input.get(next_pos, None)
                if char is None:
                    continue
                if char == ".":
                    new_beams.add((next_pos, direction))
                elif char == "|":
                    if direction in (UP, DOWN):
                        new_beams.add((next_pos, direction))
                    else:
                        new_beams.add((next_pos, UP))
                        new_beams.add((next_pos, DOWN))
                elif char == "-":
                    if direction in (RIGHT, LEFT):
                        new_beams.add((next_pos, direction))
                    else:
                        new_beams.add((next_pos, RIGHT))
                        new_beams.add((next_pos, LEFT))
                elif char == "/":
                    if direction == RIGHT:
                        direction = UP
                    elif direction == DOWN:
                        direction = LEFT
                    elif direction == LEFT:
                        direction = DOWN
                    elif direction == UP:
                        direction = RIGHT
                    new_beams.add((next_pos, direction))
                elif char == "\\":
                    if direction == RIGHT:
                        direction = DOWN
                    elif direction == DOWN:
                        direction = RIGHT
                    elif direction == LEFT:
                        direction = UP
                    elif direction == UP:
                        direction = LEFT
                    new_beams.add((next_pos, direction))
            beams = new_beams - seen
            energized.update(pos for pos, direction in new_beams)
            seen.update(new_beams)

            if False:
                for y in range(min_y, max_y + 1):
                    line = ""
                    for x in range(min_x, max_x + 1):
                        p = complex(x, y)
                        if p in energized:
                            line += "#"
                        else:
                            line += parsed_input[p]
                    print(line)
                print()

        if False:
            for y in range(min_y, max_y + 1):
                line = ""
                for x in range(min_x, max_x + 1):
                    p = complex(x, y)
                    directions = [direction for pos, direction in seen if pos == p]
                    if len(directions) == 0 or parsed_input[p] != ".":
                        line += parsed_input[p]
                    elif len(directions) > 1:
                        line += str(len(directions))
                    else:
                        line += {RIGHT: ">", LEFT: "<", UP: "^", DOWN: "v"}[directions[0]]
                print(line)
            print()

        got = len(energized)
        return got

    def part2(self, parsed_input: InputType) -> int:
        min_x, min_y, max_x, max_y = aoc.bounding_coords(parsed_input)

        maxes = []
        m = max(
            self.energized(parsed_input, complex(min_x - 1, y), RIGHT)
            for y in range(min_y, max_y + 1)
        )
        maxes.append(m)
        m = max(
            self.energized(parsed_input, complex(max_x + 1, y), LEFT)
            for y in range(min_y, max_y + 1)
        )
        maxes.append(m)
        m = max(
            self.energized(parsed_input, complex(x, min_y - 1), DOWN)
            for x in range(min_x, max_x + 1)
        )
        maxes.append(m)
        m = max(
            self.energized(parsed_input, complex(x, max_y + 1), UP)
            for x in range(min_x, max_x + 1)
        )
        maxes.append(m)

        return max(maxes)

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
