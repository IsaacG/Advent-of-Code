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
L|-JF""",  # 13
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

LineType = str
InputType = list[LineType]


class Day10(aoc.Challenge):
    """Day 10: Pipe Maze."""

    # DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=4),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=8),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=1),
        # aoc.TestCase(inputs=SAMPLE[2], part=2, want=4),
        aoc.TestCase(inputs=SAMPLE[3], part=2, want=8),
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
    INPUT_PARSER = aoc.parse_ascii_char_map(str)

    def get_loop(self, pipes: InputType) -> set[complex]:
        start = next(i for i, j in pipes.items() if j == "S")
        dirops = {
            complex(+1, 0): "-J7",
            complex(0, -1): "|F7",
            complex(-1, 0): "-FL",
            complex(0, +1): "|JL",
        }
        rotate = {
            (complex(+1, 0), "J"): complex(0, -1),
            (complex(+1, 0), "7"): complex(0, +1),
            (complex(0, -1), "F"): complex(+1, 0),
            (complex(0, -1), "7"): complex(-1, 0),
            (complex(-1, 0), "F"): complex(0, +1),
            (complex(-1, 0), "L"): complex(0, -1),
            (complex(0, +1), "J"): complex(-1, 0),
            (complex(0, +1), "L"): complex(+1, 0),
        }
        s_val = {
            frozenset({complex(-1, 0), complex(+1, 0)}): "-",
            frozenset({complex(-1, 0), complex(0, -1)}): "J",
            frozenset({complex(-1, 0), complex(0, +1)}): "7",
            frozenset({complex(+1, 0), complex(0, -1)}): "L",
            frozenset({complex(+1, 0), complex(0, +1)}): "F",
            frozenset({complex(0, -1), complex(0, +1)}): "|",
        }
        neighbors = [(direction, options) for direction, options in dirops.items() if start + direction in pipes and pipes[start + direction] in options]
        direction = neighbors[0][0]
        location = start + direction
        loop = {start}
        while location != start:
            loop.add(location)
            if (pipe := pipes[location]) in "J7FL":
                direction = rotate[direction, pipe]
            location += direction
        return loop, start, s_val[frozenset(d for d, o in neighbors)]

    def part1(self, parsed_input: InputType) -> int:
        loop = self.get_loop(parsed_input)[0]
        return len(loop) // 2

    def part2(self, parsed_input: InputType) -> int:
        pipes = parsed_input
        loop, start, s_val = self.get_loop(pipes)
        pipes[start] = s_val
        x_min = int(min(pos.real for pos in loop))
        x_max = int(max(pos.real for pos in loop))
        y_min = int(min(pos.imag for pos in loop))
        y_max = int(max(pos.imag for pos in loop))
        self.debug(f"({x_min}, {y_min}), ({x_max}, {y_max})")

        surrounded = set()
        todo = set(pipes) - loop
        while todo:
            innerdo = {todo.pop()}
            group = set()
            while innerdo:
                pos = innerdo.pop()
                group.add(pos)
                for neighbor in aoc.neighbors(pos):
                    if neighbor in todo:
                        innerdo.add(neighbor)
                        todo.discard(neighbor)
            group_x_min = int(min(pos.real for pos in group))
            group_x_max = int(max(pos.real for pos in group))
            group_y_min = int(min(pos.imag for pos in group))
            group_y_max = int(max(pos.imag for pos in group))
            self.debug(f"{group=}",)
            if group_x_min > x_min and group_x_max < x_max and group_y_min > y_min and group_y_max < y_max:
                self.debug("Surrounded")
                surrounded.update(group)

        count = 0
        self.debug("=====")
        for y in range(y_min, y_max + 1):
            line = []
            for x in range(x_min, x_max + 1):
                pos = complex(x, y)
                if pos in surrounded:
                    line.append("*")
                else:
                    line.append(pipes[pos])
            self.debug("".join(line))
        self.debug("=====")
        for y in range(y_min, y_max + 1):
            inside = False
            line = []
            transition = []
            pipe_start = ""
            for x in range(x_min, x_max + 1):
                pos = complex(x, y)
                if pos in surrounded:
                    if inside:
                        count += 1
                        line.append("I")
                    else:
                        line.append("O")
                elif pos in loop:
                    line.append(aoc.COLOR_SOLID)
                    char = pipes[pos]
                    if char in "FL":
                        pipe_start = char
                    elif (char == "|") or (char == "J" and pipe_start == "F") or (char == "7" and pipe_start == "L"):
                        inside = not inside
                        transition.append((x, inside))
                else:
                    line.append(".")
            self.debug("".join(line))
            if y == 3: self.debug(transition)
        return count


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
