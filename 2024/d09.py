#!/bin/python
"""Advent of Code, Day 9: Disk Fragmenter."""
from __future__ import annotations

import itertools
from lib import aoc

SAMPLE = '2333133121414131402'


class Day09(aoc.Challenge):
    """Day 9: Disk Fragmenter."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=1928),
        aoc.TestCase(part=2, inputs=SAMPLE, want=2858),
    ]

    def part1(self, puzzle_input: str) -> int:
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

    def part2(self, puzzle_input: str) -> int:
        is_file = True
        file_number = 0
        offset = 0
        sizes = dict(enumerate(int(i) for i in puzzle_input[::2]))
        holes = []
        starts = {}
        for digit in (int(i) for i in puzzle_input):
            if is_file:
                starts[file_number] = offset
                file_number += 1
            else:
                holes.append((offset, digit))
            is_file = not is_file
            offset += digit

        for file_number in range(file_number - 1, 1, -1):
            file_start = starts[file_number]
            file_size = sizes[file_number]
            def predicate(x):
                return x[1][0] < file_start
            hole_idx, location, size = next(
                (
                    (hole_idx, location, size)
                    for hole_idx, (location, size) in enumerate(holes)
                    if size >= file_size
                ), (None, None, None)
            )
            if location is None or location >= file_start:
                continue
            del holes[hole_idx]
            if new_size := size - file_size:
                holes.append((location + file_size, new_size))
            holes.sort()

            starts[file_number] = location
            
        return sum(file_number * (file_start + i) for file_number, file_start in starts.items() for i in range(sizes[file_number]))

# vim:expandtab:sw=4:ts=4
