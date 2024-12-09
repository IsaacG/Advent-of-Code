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

    def build_lists(self, puzzle_input: str) -> tuple[list[list[int]], list[tuple[int, int, int]]]:
        """Parse the input and build part two data structures."""
        # Pad the input to be an even number of digits so we can iterate pairwise.
        if len(puzzle_input) % 2:
            puzzle_input += "0"

        files = []
        holes = []
        offset = 0

        # Create lists of the holes and files.
        combined_sizes = (int(i) for i in puzzle_input)
        for number, (file_size, hole_size) in enumerate(itertools.batched(combined_sizes, 2)):
            files.append([number, file_size, offset])
            offset += file_size
            holes.append((number, offset, hole_size))
            offset += hole_size

        # Check files from right to left.
        files.reverse()
        return files, holes

    def part2(self, puzzle_input: str) -> int:
        """Defragment a disk, one file at a time."""
        files, holes = self.build_lists(puzzle_input)
        smallest_file = 1
        for hole_number, hole_offset, hole_size in holes:
            smallest_seen = 9
            for file_info in files:
                if hole_size < smallest_file:
                    break
                file_number, file_size, file_offset = file_info
                if file_size <= hole_size and hole_offset < file_offset:
                    # Move files into the hole.
                    file_info[2] = hole_offset
                    hole_offset += file_size
                    hole_size -= file_size
                elif hole_offset < file_offset:
                    # Only count right to the right of the hole.
                    smallest_seen = min(smallest_seen, file_size)
                if file_number < hole_number:
                    # Stop when the remaining files are all to the left of the hole.
                    smallest_file = smallest_seen
                    break

        return sum(
            file_number * (file_offset + i)
            for file_number, file_size, file_offset in files
            for i in range(file_size)
        )

# vim:expandtab:sw=4:ts=4
