#!/bin/python
"""Advent of Code, Day 18: RAM Run."""
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
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0""",  # 4
]

LineType = int
InputType = list[LineType]


class Day18(aoc.Challenge):
    """Day 18: RAM Run."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=22),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want="6,1"),
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

    def part1(self, puzzle_input: InputType) -> int:
        fallen = set(complex(*i) for i in puzzle_input[:12 if self.testing else 1024])
        size = 7 if self.testing else 71
        spaces = {complex(x, y) for x in range(size) for y in range(size)}
        spaces -= fallen

        start = complex(0)
        end = complex(size - 1, size - 1)

        todo = queue.PriorityQueue()
        todo.put((0, start.real, start.imag))
        seen = set()
        while not todo.empty():
            cost, x, y = todo.get()
            p = complex(x, y)
            if p == end:
                return cost
            for n in aoc.neighbors(p):
                if n in seen or n not in spaces:
                    continue
                seen.add(n)
                todo.put((cost + 1, n.real, n.imag))

                  
        raise RuntimeError("Not solved")

    def runmaze(self, puzzle_input: InputType, steps) -> int:
        fallen = set(complex(*i) for i in puzzle_input[:steps])
        size = 7 if self.testing else 71
        spaces = {complex(x, y) for x in range(size) for y in range(size)}
        spaces -= fallen

        start = complex(0)
        end = complex(size - 1, size - 1)

        todo = queue.PriorityQueue()
        todo.put((0, start.real, start.imag))
        seen = set()
        while not todo.empty():
            cost, x, y = todo.get()
            p = complex(x, y)
            if p == end:
                return cost
            for n in aoc.neighbors(p):
                if n in seen or n not in spaces:
                    continue
                seen.add(n)
                todo.put((cost + 1, n.real, n.imag))

        return None

    def part2(self, puzzle_input: InputType) -> int:
        low = 12 if self.testing else 1024
        high = len(puzzle_input)

        count = 0
        cur = 0
        while low < high - 1:
            print(f"cur = (high + low) // 2 = ({high} + {low}) // 2 = {(high + low) // 2}")
            cur = (high + low) // 2
            count += 1
            if count > 100: break
            if self.runmaze(puzzle_input, cur) is None:
                print(f"Set {high=} to {cur-1}")
                high = cur - 1
            else:
                print(f"Set {low=} to {cur}")
                low = cur
            print(low, high, cur)
        got = ",".join(str(i) for i in puzzle_input[high])
        assert got != "40,62"
        assert got != "46,25"
        assert got != "29,46"
        return got




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
