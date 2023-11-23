#!/bin/python
"""Advent of Code, Day 13: Mine Cart Madness."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
|
v
|
|
|
^
|""",
r"""/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   """,
r"""/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/""",
]

LineType = int
InputType = list[LineType]

ROT_LEFT = complex(0, -1)
ROT_STRAIGHT = complex(1, -0)
ROT_RIGHT = complex(0, 1)
ROTATIONS = [ROT_LEFT, ROT_STRAIGHT, ROT_RIGHT]
UP = complex(0, -1)
DOWN = complex(0, 1)
LEFT = complex(-1, 0)
RIGHT = complex(1, 0)

DIRECTIONS = {"^": UP, "v": DOWN, "<": LEFT, ">": RIGHT}
R_DIRECTIONS = {v: k for k, v in DIRECTIONS.items()}
CORNERS = {
    "/": {UP: RIGHT, LEFT: DOWN, RIGHT: UP, DOWN: LEFT},
    "\\": {UP: LEFT, LEFT: UP, RIGHT: DOWN, DOWN: RIGHT},
}


class Day13(aoc.Challenge):
    """Day 13: Mine Cart Madness."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want="0,3"),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want="7,3"),
        aoc.TestCase(inputs=SAMPLE[2], part=2, want="6,4"),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_one_str_per_line
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
    # POST_PROCESS = set

    def part1(self, parsed_input: InputType) -> int:
        tracks, turns, junctions, wagons = parsed_input
        max_x = int(max(p.real for p in tracks))
        max_y = int(max(p.imag for p in tracks))
        for step in itertools.count(start=1):

            if False:
                print("=" * max_x)
                for y in range(max_y + 1):
                    row = []
                    for x in range(max_x + 1):
                        location = complex(x, y)
                        if location in wagons:
                            row.append(R_DIRECTIONS[wagons[location][0]])
                        elif location in turns:
                            row.append("*")
                        elif location in tracks:
                            row.append("#")
                        else:
                            row.append(" ")
                    print("".join(row))
                print()

            wagon_order = sorted(wagons, key=lambda x: (x.imag, x.real))
            for location in wagon_order:
                direction, rotation = wagons[location]
                new_location = location + direction
                if new_location in wagons:
                    return f"{int(new_location.real)},{int(new_location.imag)}"
                if new_location in junctions:
                    direction *= ROTATIONS[rotation % 3]
                    rotation += 1
                elif new_location in turns:
                    direction = turns[new_location][direction]
                del wagons[location]
                wagons[new_location] = (direction, rotation)

            if step > 200:
                break

    def part2(self, parsed_input: InputType) -> int:
        tracks, turns, junctions, wagons = parsed_input
        max_x = int(max(p.real for p in tracks))
        max_y = int(max(p.imag for p in tracks))
        for step in itertools.count(start=1):
            if len(wagons) == 1:
                location = list(wagons)[0]
                return f"{int(location.real)},{int(location.imag)}"

            wagon_order = sorted(wagons, key=lambda x: (x.imag, x.real))
            for location in wagon_order:
                if location not in wagons:
                    continue
                direction, rotation = wagons[location]
                new_location = location + direction
                if new_location in wagons:
                    del wagons[location]
                    del wagons[new_location]
                    continue
                if new_location in junctions:
                    direction *= ROTATIONS[rotation % 3]
                    rotation += 1
                elif new_location in turns:
                    direction = turns[new_location][direction]
                del wagons[location]
                wagons[new_location] = (direction, rotation)

            if step > 20000:
                break



    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        junctions = aoc.parse_ascii_bool_map("+").parse(puzzle_input)
        tracks = aoc.parse_ascii_bool_map("/\-|+^v<>").parse(puzzle_input)
        turns = aoc.parse_ascii_char_map(lambda x: CORNERS.get(x, None)).parse(puzzle_input)
        wagons = aoc.parse_ascii_char_map(lambda x: DIRECTIONS.get(x, None)).parse(puzzle_input)
        wagons = {location: (direction, 0) for location, direction in wagons.items()}
        return (tracks, turns, junctions, wagons)
