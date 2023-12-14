#!/bin/python
"""Advent of Code, Day 14: Parabolic Reflector Dish."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""",
]

LineType = int
InputType = list[LineType]


class Day14(aoc.Challenge):
    """Day 14: Parabolic Reflector Dish."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=136),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=64),
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

    def part1(self, parsed_input: InputType) -> int:
        stationary, moving = parsed_input
        min_x, min_y, max_x, max_y = aoc.bounding_coords(stationary | moving)
        north = complex(0, -1)
        post_move = set(stationary)
        for rock in sorted(moving, key=lambda x: x.imag):
            while (new_pos := rock + north) not in post_move and rock.imag > 0:
                rock = new_pos
            post_move.add(rock)
        moved = post_move - stationary

        for y in range(min_y, max_y + 1):
            line = []
            for x in range(min_x, max_x + 1):
                if complex(x, y) in stationary:
                    line.append("#")
                if complex(x, y) in moved:
                    line.append("O")
                else:
                    line.append(".")
            print("".join(line))
        return sum(max_y + 1 - rock.imag for rock in moved)

    def part2(self, parsed_input: InputType) -> int:
        stationary, moving = parsed_input
        min_x, min_y, max_x, max_y = aoc.bounding_coords(stationary | moving)
        north = complex(0, -1)
        west = complex(-1, 0)
        south = complex(0, 1)
        east = complex(+1, 0)

        def cycle(moving):
            post_move = set(stationary)
            for rock in sorted(moving, key=lambda x: x.imag, reverse=False):
                while (new_pos := rock + north) not in post_move and rock.imag > min_y:
                    rock = new_pos
                post_move.add(rock)
            moving = post_move - stationary

            post_move = set(stationary)
            for rock in sorted(moving, key=lambda x: x.real, reverse=False):
                while (new_pos := rock + west) not in post_move and rock.real > min_x:
                    rock = new_pos
                post_move.add(rock)
            moving = post_move - stationary

            post_move = set(stationary)
            for rock in sorted(moving, key=lambda x: x.imag, reverse=True):
                while (new_pos := rock + south) not in post_move and rock.imag < max_y:
                    rock = new_pos
                post_move.add(rock)
            moving = post_move - stationary

            post_move = set(stationary)
            for rock in sorted(moving, key=lambda x: x.real, reverse=True):
                while (new_pos := rock + east) not in post_move and rock.real < max_x:
                    rock = new_pos
                post_move.add(rock)
            return post_move - stationary

        cache = {}
        for step in range(1000000000):
            moving = cycle(moving)

            frozen = frozenset(moving)
            if frozen in cache:
                print(f"Cycle repeat {cache[frozen]} -> {step}")
                cycle_size = (step - cache[frozen])
                remaining_steps = 1000000000 - step - 1
                remaining_steps %= cycle_size
                print(remaining_steps)
                for _ in range(remaining_steps):
                    moving = cycle(moving)
                break
            cache[frozenset(moving)] = step

        return sum(max_y + 1 - rock.imag for rock in moving)

        raise NotImplementedError

    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        raise NotImplementedError

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return (
            aoc.parse_ascii_bool_map("#").parse(puzzle_input),
            aoc.parse_ascii_bool_map("O").parse(puzzle_input),
        )

# vim:expandtab:sw=4:ts=4
