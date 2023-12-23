#!/bin/python
"""Advent of Code, Day 23: A Long Walk."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#""",  # 6
]

LineType = int
InputType = list[LineType]


class Day23(aoc.Challenge):
    """Day 23: A Long Walk."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [False, True]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=94),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=154),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_ascii_char_map(lambda x: x)

    def part1(self, parsed_input: InputType) -> int:
        board = parsed_input
        min_x, min_y, max_x, max_y = aoc.bounding_coords(board)
        start = next(i for i, char in board.items() if i.imag == min_y and char == ".")
        end = next(i for i, char in board.items() if i.imag == max_y and char == ".")

        paths = {(start, frozenset({start}))}
        max_path = 0
        while paths:
            current, seen = paths.pop()
            if current == end:
                new_len = len(seen)
                if new_len > max_path:
                    max_path = new_len


            char = board[current]
            if char in aoc.ARROW_DIRECTIONS:
                next_pos = current + aoc.ARROW_DIRECTIONS[char]
                assert board[next_pos] != "#"
                if next_pos not in seen:
                    paths.add((next_pos, frozenset(seen | {next_pos})))
            else:
                for next_pos in aoc.neighbors(current):
                    if board.get(next_pos, "#") != "#" and next_pos not in seen:
                        paths.add((next_pos, frozenset(seen | {next_pos})))

        return max_path - 1

        assert len(completed) == len(set(completed))
        print([len(i) for i in completed])
        if False:
            for y in range(max_y + 1):
                line = []
                for x in range(max_x + 1):
                    pos = complex(x, y)
                    if pos in seen:
                        line.append("O")
                    else:
                        line.append(board[pos])
                print("".join(line))
            print()

        # Do not count start
        return 0


        print(f"{parsed_input!r}")
        return 0

    def part2(self, parsed_input: InputType) -> int:
        board = {pos for pos, char in parsed_input.items() if char != "#"}
        min_x, min_y, max_x, max_y = aoc.bounding_coords(board)
        start = next(i for i in board if i.imag == min_y)
        end = next(i for i in board if i.imag == max_y)

        forks = {coord for coord in board if len(set(aoc.neighbors(coord)) & board) > 2}
        forks.add(start)
        destinations = forks | {end}

        longest_dist = collections.defaultdict(lambda: collections.defaultdict(int))

        for coord in forks:
            neighbors = set(aoc.neighbors(coord)) & board

            for current in neighbors:
                steps = 1
                prior = coord

                while current not in destinations:
                    steps += 1
                    options = set(aoc.neighbors(current)) & board 
                    assert len(options) == 2
                    current, prior = next(i for i in options if i != prior), current

                dist = max(steps, longest_dist[coord][current])
                longest_dist[coord][current] = dist
                longest_dist[current][coord] = dist

        longest_dist = {start: dict(end) for start, end in longest_dist.items()}
        # print(longest_dist)

        max_path = 0
        paths = {(start, frozenset({start}), 0)}
        while paths:
            current, seen, steps = paths.pop()
            if current == end:
                if steps > max_path:
                    max_path = steps
                    print(f"{max_path=}, {len(paths)=}")
                continue

            for next_pos, distance in longest_dist[current].items():
                if next_pos not in seen:
                    paths.add((next_pos, frozenset(seen | {next_pos}), steps + distance))

        return max_path

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
