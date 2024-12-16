#!/bin/python
"""Advent of Code, Day 16: Reindeer Maze."""
from __future__ import annotations

import collections
import functools
import queue
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############""",  # 5
    """\
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################""",  # 33
    """\
#################
#...#...#...#..""",  # 34
    """\
#
#.#.#.#.#.#.#.#""",  # 35
    """\
#
#.#.#.#...#...#""",  # 36
    """\
#
#.#.#.#.###.#.#""",  # 37
    """\
#
#""",  # 38
    '#.#.#.....#',  # 39
    """\
#
#""",  # 40
    '#',  # 41
    '#.#.#.#####',  # 42
    """\
#
#""",  # 43
    '#',  # 44
    '..#.#.#',  # 45
    """\
#
#""",  # 46
    '#',  # 47
    '#####.#',  # 48
    """\
###.#
#""",  # 49
    '#',  # 50
    '#..',  # 51
    """\
#...#
#""",  # 52
    '#',  # 53
    '###',  # 54
    """\
#####.###
#""",  # 55
    '#',  # 56
    '#',  # 57
    """\
#.....#.#
#""",  # 58
    '#',  # 59
    '#',  # 60
    """\
#####.###.#
#""",  # 61
    '#',  # 62
    '#',  # 63
    """\
........#.#
#""",  # 64
    '#',  # 65
    '#',  # 66
    """\
#########.#
#S#""",  # 67
    """\
..........#
#################""",  # 68
]

LineType = int
InputType = list[LineType]


class Day16(aoc.Challenge):
    """Day 16: Reindeer Maze."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=7036),
        aoc.TestCase(part=1, inputs=SAMPLE[1], want=11048),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=45),
        aoc.TestCase(part=2, inputs=SAMPLE[1], want=64),
        # aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    # INPUT_PARSER = aoc.parse_one_str
    # INPUT_PARSER = aoc.parse_one_str_per_line
    # INPUT_PARSER = aoc.parse_multi_str_per_line
    # INPUT_PARSER = aoc.parse_one_int
    # INPUT_PARSER = aoc.parse_one_int_per_line
    # INPUT_PARSER = aoc.parse_ints_one_line
    # INPUT_PARSER = aoc.parse_ints_per_line
    # INPUT_PARSER = aoc.parse_re_group_str(r"(a) .* (b) .* (c)")
    # INPUT_PARSER = aoc.parse_re_findall_str(r"(a|b|c)")
    # INPUT_PARSER = aoc.parse_multi_mixed_per_line
    # INPUT_PARSER = aoc.parse_re_group_mixed(r"(foo) .* (\d+)")
    # INPUT_PARSER = aoc.parse_re_findall_mixed(r"\d+|foo|bar")
    # INPUT_PARSER = aoc.ParseBlocks([aoc.parse_one_str_per_line, aoc.parse_re_findall_int(r"\d+")])
    # INPUT_PARSER = aoc.ParseOneWord(aoc.Board.from_int_block)
    # INPUT_PARSER = aoc.CoordinatesParser(chars=None, origin_top_left=True)
    # ---
    # (width, height), start, garden, rocks = puzzle_input
    # max_x, max_y = width - 1, height - 1

    def solver(self, puzzle_input: InputType, part_one: bool) -> int:
        open_space = puzzle_input["."]
        starts, ends = puzzle_input["SE"]
        start = starts.pop()
        end = ends.pop()
        open_space.add(end)
        open_space.add(start)

        pos = start
        direction = complex(1)
        lowest = {(start, direction): (0, set())}
        todo = queue.PriorityQueue()
        print(f"{start=}, {end=}")

        def score(p):
            return abs(end.real - p.real) + abs(end.imag - p.imag)

        todo.put((score(pos), 0, pos.real, pos.imag, direction.real, direction.imag))

        while not todo.empty():
            rank, cost, pos_x, pos_y, dir_x, dir_y = todo.get()
            pos = complex(pos_x, pos_y)
            direction = complex(dir_x, dir_y)
            # print(f"Exploring {pos} {direction} {cost=} {rank=}")
            if pos == end:
                if part_one:
                    return cost
                to_explore = {(end, direction)}
                good_seats = set()
                while to_explore:
                    p, d = to_explore.pop()
                    good_seats.add(p)
                    to_explore.update(lowest[p, d][1])
                return len(good_seats)

            next_pos = pos + direction
            options = [(pos, direction * 1j, cost + 1000), (pos, direction * -1j, cost + 1000)]
            if next_pos in open_space:
                options.append((next_pos, direction, cost + 1))
            for next_pos, next_dir, next_cost in options:
                if (
                    (next_pos, next_dir) not in lowest or
                    lowest[(next_pos, next_dir)][0] > next_cost
                ):
                    lowest[(next_pos, next_dir)] = (next_cost, {(pos, direction)})
                    rank = score(next_pos) + next_cost
                    todo.put((rank, next_cost, next_pos.real, next_pos.imag, next_dir.real, next_dir.imag))
                    # print(f"Push {next_pos} {next_dir} {next_cost=}, {rank=}")
                elif lowest[(next_pos, next_dir)][0] == next_cost:
                    lowest[(next_pos, next_dir)][1].add((pos, direction))
        return None

    # def part2(self, puzzle_input: InputType) -> int:

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
