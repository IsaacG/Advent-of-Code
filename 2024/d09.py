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
        if len(puzzle_input) % 2:
            puzzle_input += "0"

        files = []
        holes = []
        offset = 0

        combined_sizes = (int(i) for i in puzzle_input)
        for file_number, (file_size, hole_size) in enumerate(itertools.batched(combined_sizes, 2)):
            files.append([file_number, file_size, offset])
            offset += file_size
            holes.append((offset, hole_size))
            offset += hole_size

        largest_file = max(file_size for _, file_size, _ in files)
        files.reverse()

        smallest_file = 0
        for hole_offset, hole_size in holes:
            smallest_seen = largest_file
            if hole_size < smallest_file:
                continue
            for idx, (file_number, file_size, file_offset) in enumerate(files):
                if hole_size < smallest_file:
                    break
                if file_size <= hole_size and hole_offset < file_offset:
                    files[idx][2] = hole_offset
                    hole_offset += file_size
                    hole_size -= file_size
                elif hole_offset < file_offset:
                    smallest_seen = min(smallest_seen, file_size)
            else:
                smallest_file = smallest_seen

        return sum(file_number * (file_offset + i) for file_number, file_size, file_offset in files for i in range(file_size))

# vim:expandtab:sw=4:ts=4
