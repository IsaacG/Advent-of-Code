#!/bin/python
"""Advent of Code, Day 23: Unstable Diffusion."""
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
..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
..............""",
    """\
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..""",
    """\
.....
..##.
..#..
.....
..##.
.....""",  # 3
]

LineType = int
InputType = list[LineType]

N, S, E, W = -1j, 1j, 1, -1


class Day23(aoc.Challenge):
    """Day 23: Unstable Diffusion."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=110),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=20),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]
    INPUT_PARSER = aoc.parse_ascii_bool_map("#")

    def part1(self, parsed_input: InputType) -> int:
        directions = [
            (N, (N + W, N, N + E)),
            (S, (S + W, S, S + E)),
            (W, (N + W, W, S + W)),
            (E, (N + E, E, S + E)),
        ]
        positions = parsed_input
        # print(positions)
        for step in range(10):
            proposed = collections.defaultdict(int)
            choices = {}
            for elf in positions:
                if not any(elf + direction in positions for direction in aoc.EIGHT_DIRECTIONS):
                    continue
                for option in range(4):
                    move, checks = directions[(step + option) % 4]
                    if all(elf + check not in positions for check in checks):
                        choice = elf + move
                        proposed[choice] += 1
                        choices[elf] = choice
                        break
            new_positions = set()
            for elf in positions:
                if elf in choices and proposed[choices[elf]] == 1:
                    new_positions.add(choices[elf])
                else:
                    new_positions.add(elf)
            positions = new_positions
            # print()
            # print(f"== End of Round {step + 1} ==")
            # print(aoc.render(positions, ".", "#"))
        min_x = min(elf.real for elf in positions)
        max_x = max(elf.real for elf in positions)
        min_y = min(elf.imag for elf in positions)
        max_y = max(elf.imag for elf in positions)
        print(max_x - min_x, max_y - min_y, len(positions))
        answer = int((max_x - min_x + 1) * (max_y - min_y + 1)) - len(positions)
        if not self.testing:
            assert answer < 7140, "Too high!"
        print(answer)
        return answer

    def part2(self, parsed_input: InputType) -> int:
        directions = [
            (N, (N + W, N, N + E)),
            (S, (S + W, S, S + E)),
            (W, (N + W, W, S + W)),
            (E, (N + E, E, S + E)),
        ]
        positions = parsed_input
        for step in range(1000000):
            proposed = collections.defaultdict(int)
            choices = {}
            for elf in positions:
                if not any(elf + direction in positions for direction in aoc.EIGHT_DIRECTIONS):
                    continue
                for option in range(4):
                    move, checks = directions[(step + option) % 4]
                    if all(elf + check not in positions for check in checks):
                        choice = elf + move
                        proposed[choice] += 1
                        choices[elf] = choice
                        break
            new_positions = set()
            for elf in positions:
                if elf in choices and proposed[choices[elf]] == 1:
                    new_positions.add(choices[elf])
                else:
                    new_positions.add(elf)
            if positions == new_positions:
                return step + 1
            positions = new_positions
        raise RuntimeError("Not found")



if __name__ == "__main__":
    typer.run(Day23().run)

# vim:expandtab:sw=4:ts=4
