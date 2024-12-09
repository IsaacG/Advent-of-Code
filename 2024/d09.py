#!/bin/python
"""Advent of Code, Day 9: Disk Fragmenter."""

import itertools
from lib import aoc

SAMPLE = "2333133121414131402"
HOLE = -1


class Day09(aoc.Challenge):
    """Day 9: Disk Fragmenter."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=1928),
        aoc.TestCase(part=2, inputs=SAMPLE, want=2858),
    ]

    def part1(self, puzzle_input: str) -> int:
        """Defragment a disk, one block at a time."""
        disk = []

        # Add a trailing 0 so we can read file and hole sizes in batches of 2 numbers.
        combined_sizes = (int(i) for i in puzzle_input + "0")
        for file_number, (file_size, hole_size) in enumerate(itertools.batched(combined_sizes, 2)):
            disk.extend([file_number] * file_size)
            disk.extend([HOLE] * hole_size)

        start, end = 0, len(disk) - 1
        while start < end:
            while disk[start] != HOLE:  # Find a hole to fill.
                start += 1
            while end > start and disk[end] == HOLE:  # Find a block to move.
                end -= 1
            disk[start], disk[end] = disk[end], disk[start]

        return sum(idx * val for idx, val in enumerate(disk) if val != HOLE)

    def part2(self, puzzle_input: str) -> int:
        """Defragment a disk, one file at a time."""
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
