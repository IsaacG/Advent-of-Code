#!/bin/python
"""Advent of Code, Day 24: Never Tell Me The Odds."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re
import z3

from lib import aoc

SAMPLE = [
    """\
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3""",  # 0
]

START = 200000000000000
END = 400000000000000

LineType = int
InputType = list[LineType]


class Day24(aoc.Challenge):
    """Day 24: Never Tell Me The Odds."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [False, True]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=2),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
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
    INPUT_PARSER = aoc.parse_re_findall_int(aoc.RE_INT)
    # INPUT_PARSER = aoc.parse_multi_mixed_per_line
    # INPUT_PARSER = aoc.parse_re_group_mixed(r"(foo) .* (\d+)")
    # INPUT_PARSER = aoc.parse_re_findall_mixed(r"\d+|foo|bar")
    # INPUT_PARSER = aoc.ParseBlocks([aoc.parse_one_str_per_line, aoc.parse_re_findall_int(r"\d+")])
    # INPUT_PARSER = aoc.ParseOneWord(aoc.Board.from_int_block)
    # INPUT_PARSER = aoc.parse_ascii_bool_map("#")
    # ---
    # INPUT_PARSER = aoc.CharCoordinatesParser("S.#")
    # (width, height), start, garden, rocks = parsed_input
    # max_x, max_y = width - 1, height - 1

    def part1(self, parsed_input: InputType) -> int:
        if self.testing:
            start, end = 7, 27
        else:
            start, end = START, END

        eqns = []
        for idx, (px, py, pz, vx, vy, vz) in enumerate(parsed_input):
            slope = vy / vx
            # y = slope * x + b
            b = py - slope * px
            eqns.append((idx, px, vx, slope, b))

        count = 0
        for (idx_one, px_one, vx_one, a, c), (idx_two, px_two, vx_two, b, d) in itertools.product(eqns, repeat=2):
            if idx_one >= idx_two:
                continue
            if a == b:
                # print(f"{parsed_input[idx_one]}\n{parsed_input[idx_two]}\nPARALLEL\n\n")
                continue
            intersect_x = (d - c ) / (a - b)
            intersect_y = a * intersect_x + c
            if start <= intersect_x <= end and start <= intersect_y <= end:
                if ((intersect_x - px_one) >= 0) == (vx_one > 0) and ((intersect_x - px_two) >= 0) == (vx_two > 0):
                    count += 1
                    # print(f"{parsed_input[idx_one]}\n{parsed_input[idx_two]}\n{(intersect_x, intersect_y)}\n\n")
                else:
                    # print(f"{parsed_input[idx_one]}\n{parsed_input[idx_two]}\nPAST {(intersect_x, intersect_y)}\n\n")
                    pass


        if not self.testing:
            assert count != 4946
        return count

    def part2(self, parsed_input: InputType) -> int:
        (px_one, py_one, pz_one, vx_one, vy_one, vz_one) = parsed_input[0]
        (px_two, py_two, pz_two, vx_two, vy_two, vz_two) = parsed_input[0]
        data = [(idx, px, py, pz, vx, vy, vz) for idx, (px, py, pz, vx, vy, vz) in enumerate(parsed_input)]

        x = z3.Int("x")
        y = z3.Int("y")
        z = z3.Int("z")
        vx = z3.Int("vx")
        vy = z3.Int("vy")
        vz = z3.Int("vz")
        ans = z3.Int("ans")
        ts = [z3.Int(f"t{i}") for i in range(len(data))]
        solver = z3.Solver()
        for i, x1, y1, z1, vx1, vy1, vz1 in data[:3]:
            solver.add(x1 + vx1 * ts[i] == x + vx * ts[i])
            solver.add(y1 + vy1 * ts[i] == y + vy * ts[i])
            solver.add(z1 + vz1 * ts[i] == z + vz * ts[i])
        solver.add(ans == x + y + z)
        if solver.check() != z3.sat:
            raise RuntimeError("No solution found")
        model = solver.model()
        return model[ans]



        normalized_slopes = [
            (vx / vz, vy / vz, 1) for (idx, px, py, pz, vx, vy, vz) in data
        ]
        counts = collections.Counter(normalized_slopes)
        return
        for (idx_one, px_one, py_one, pz_one, vx_one, vy_one, vz_one), (idx_two, px_two, py_two, pz_two, vx_two, vy_two, vz_two) in itertools.product(data, repeat=2):
            if idx_one >= idx_two:
                continue

        for i in range(0, 10000000000):
            p_one = (px_one + vx_one * i, py_one + vy_one * i, pz_one + vz_one * i)
            p_two = (px_two + vx_two * i, py_two + vy_two * i, pz_two + vz_two * i)


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
# vim:expandtab:sw=4:ts=4
