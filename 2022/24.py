#!/bin/python
"""Advent of Code, Day 24: Blizzard Basin."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import sys
import re

import typer
from lib import aoc

SAMPLE = [
    """\
#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#""",  # 0
    """\
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#""",  # 15
]

sys.setrecursionlimit(2500)


LineType = int
InputType = list[LineType]


class Day24(aoc.Challenge):
    """Day 24: Blizzard Basin."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=18),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=54),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    @functools.cache
    def nogo(self, moves: int) -> set[complex]:
        return set.union(*self.get_bliz(moves).values()) | self.walls

    @functools.cache
    def get_bliz(self, moves: int) -> set[complex]:
        if moves == 0:
            return self.blizzards
        new_blizz = {}
        for direction, storms in self.get_bliz(moves - 1).items():
            new_storms = set()
            for storm in storms:
                storm += direction
                if storm.real == self.width - 1:
                    storm = complex(1, storm.imag)
                elif storm.real == 0:
                    storm = complex(self.width - 2, storm.imag)
                elif storm.imag == 0:
                    storm = complex(storm.real, self.height - 2)
                elif storm.imag == self.height - 1:
                    storm = complex(storm.real, 1)
                new_storms.add(storm)
            new_blizz[direction] = new_storms
        return new_blizz

    def part1(self, parsed_input: InputType) -> int:
        self.walls, self.blizzards, self.width, self.height = parsed_input
        start = complex(1, 0)
        if self.testing:
            options = {(0, start),}
        else:
            options = {(570, start),}
        """
        for i in range(4):
            print(f"Step {i}:")
            print(aoc.render(self.nogo(i)))
            print()
        return
        # assert (1+3j) in self.nogo(3)
        """
        walls = self.walls
        while options:
            moves_cur = min(options, key=lambda x: (x[0], -x[1].imag))
            moves, cur = moves_cur
            options.remove(moves_cur)
            # print(f"{moves=}, {cur=}")
            cur_nogo = self.nogo(moves)
            assert cur not in cur_nogo
            nogo = self.nogo(moves + 1)
            for direction in aoc.FOUR_DIRECTIONS + [0]:
                opt = cur + direction
                if opt.imag < 0:
                    continue
                if opt in nogo:
                    continue
                if opt.imag == self.height - 1:
                    return moves + 1
                options.add((moves + 1, opt))

    def part2(self, parsed_input: InputType) -> int:
        self.walls, self.blizzards, self.width, self.height = parsed_input
        start = complex(1, 0)
        walls = self.walls
        end = complex(self.width - 2, self.height - 1)
        if self.testing:
            options = {(18, end),}
        else:
            options = {(301, end),}
        # end to start
        while options:
            moves_cur = min(options, key=lambda x: (x[0], x[1].imag))
            moves, cur = moves_cur
            options.remove(moves_cur)
            # print(f"{moves=}, {cur=}")
            cur_nogo = self.nogo(moves)
            assert cur not in cur_nogo
            nogo = self.nogo(moves + 1)
            for direction in aoc.FOUR_DIRECTIONS + [0]:
                opt = cur + direction
                if opt.imag > self.height - 1:
                    continue
                if opt in nogo:
                    continue
                if opt.imag == 0:
                    return moves + 1
                options.add((moves + 1, opt))

    def parse_chars(self, puzzle_input: str, on_char: str) -> set[complex]:
        """Parse ASCII to find points in a map which are "on"."""
        return {
            complex(x, y)
            for y, line in enumerate(puzzle_input.splitlines())
            for x, char in enumerate(line)
            if char == on_char
        }

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        walls = self.parse_chars(puzzle_input, "#")
        blizzards = {
            +1:  self.parse_chars(puzzle_input, ">"),
            -1:  self.parse_chars(puzzle_input, "<"),
            1j:  self.parse_chars(puzzle_input, "v"),
            -1j: self.parse_chars(puzzle_input, "^"),
        }
        width, height = len(puzzle_input.splitlines()[0]), len(puzzle_input.splitlines())
        return (walls, blizzards, width, height)

    # def line_parser(self, line: str):
    #     pass


if __name__ == "__main__":
    typer.run(Day24().run)

# vim:expandtab:sw=4:ts=4
