#!/bin/python
"""Advent of Code, Day 9: Disk Fragmenter."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = '2333133121414131402'

InputType = str


class Day09(aoc.Challenge):
    """Day 9: Disk Fragmenter."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=1928),
        aoc.TestCase(part=2, inputs=SAMPLE, want=2858),
        # aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_one_str
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
        is_file = True
        fileno = 0
        disk = []
        for digit in puzzle_input:
            if is_file:
                disk.extend([fileno] * int(digit))
                fileno += 1
            else:
                disk.extend([None] * int(digit))
            is_file = not is_file

        start, end = 0, len(disk) - 1
        while start < end:
            # print("".join([str(i) if i is not None else "." for i in disk]))
            while disk[start] is not None:
                start += 1
            while end >= 0 and disk[end] is None:
                end -= 1
            if start >= end:
                break
            disk[start], disk[end] = disk[end], disk[start]

        return sum(idx * val for idx, val in enumerate(disk) if val)

    def part2(self, puzzle_input: InputType) -> int:
        is_file = True
        fileno = 0
        disk = []
        filesizes = dict(enumerate(int(i) for i in puzzle_input[::2]))
        holes = {}
        files = {}
        for digit in puzzle_input:
            if is_file:
                files[int(digit)] = len(disk)
                disk.extend([fileno] * int(digit))
                fileno += 1
            else:
                holes[len(disk)] = int(digit)
                disk.extend([None] * int(digit))
            is_file = not is_file

        for fileno in sorted(filesizes, reverse=True)[:-1]:
            if fileno and not fileno % 500:
                print(fileno)
            # print("".join([str(i) if i is not None else "." for i in disk]))
            file_start = disk.index(fileno)
            file_size = filesizes[fileno]
            location, size = next(
                (
                    (location, size)
                    for location, size in sorted(holes.items())
                    if size >= file_size
                ), (None, None)
            )
            if fileno == 2:
                print(2, location, size)
            if location is None or location >= file_start:
                continue
            del holes[location]
            holes[location + file_size] = size - file_size

            for i in range(file_size):
                disk[location + i] = fileno
                disk[file_start + i] = None
            
        print("".join([str(i) if i is not None else "." for i in disk]))
        return sum(idx * val for idx, val in enumerate(disk) if val)

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
