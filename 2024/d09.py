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

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=1928),
        aoc.TestCase(part=2, inputs=SAMPLE, want=2858),
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
        file_number = 0
        offset = 0
        sizes = dict(enumerate(int(i) for i in puzzle_input[::2]))
        holes = {}
        starts = {}
        for digit in (int(i) for i in puzzle_input):
            if is_file:
                starts[file_number] = offset
                file_number += 1
            else:
                holes[offset] = digit
            is_file = not is_file
            offset += digit

        self.tprint(starts)
        self.tprint(holes)

        for file_number in sorted(sizes, reverse=True)[:-1]:
            file_start = starts[file_number]
            file_size = sizes[file_number]
            location, size = next(
                (
                    (location, size)
                    for location, size in sorted(holes.items())
                    if size >= file_size
                ), (None, None)
            )
            if location is None or location >= file_start:
                continue
            del holes[location]
            holes[location + file_size] = size - file_size

            starts[file_number] = location
            
        return sum(file_number * (file_start + i) for file_number, file_start in starts.items() for i in range(sizes[file_number]))

# vim:expandtab:sw=4:ts=4
