#!/bin/python
"""Advent of Code, Day 9: Disk Fragmenter."""

import heapq
import itertools

HOLE = -1


def build_lists(data: str) -> tuple[list[list[int]], dict[int, list[int]]]:
    """Parse the input and build part two data structures."""
    # Pad the input to be an even number of digits so we can iterate pairwise.
    if len(data) % 2:
        data += "0"

    files = []
    holes: dict[int, list[int]] = {i: [] for i in range(1, 10)}
    offset = 0

    # Create lists of the holes and files.
    combined_sizes = (int(i) for i in data)
    for number, (file_size, hole_size) in enumerate(itertools.batched(combined_sizes, 2)):
        if file_size:
            files.append([number, file_size, offset])
        offset += file_size
        if hole_size:
            heapq.heappush(holes[hole_size], offset)
        offset += hole_size

    # Check files from right to left.
    files.reverse()
    return files, holes


def solve(data: str, part: int) -> int:
    """Solve the parts."""
    return (part1 if part == 1 else part2)(data)


def part1(data: str) -> int:
    """Defragment a disk, one block at a time."""
    disk = []

    # Add a trailing 0 so we can read file and hole sizes in batches of 2 numbers.
    combined_sizes = (int(i) for i in data + "0")
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


def part2(data: str) -> int:
    """Defragment a disk, one file at a time."""
    files, holes = build_lists(data)
    for file_info in files:
        file_number, file_size, file_offset = file_info
        candidates = (
            (hole_size, hole_q)
            for hole_size, hole_q in holes.items()
            if hole_size >= file_size and hole_q and hole_q[0] < file_offset
        )
        hole_size, hole_q = min(candidates, key=lambda x: x[1][0], default=(None, None))
        if hole_q is not None and hole_size is not None:
            hole_offset = heapq.heappop(hole_q)
            file_info[2] = hole_offset
            if hole_size != file_size:
                heapq.heappush(holes[hole_size - file_size], hole_offset + file_size)

    return sum(
        file_number * (file_offset + i)
        for file_number, file_size, file_offset in files
        for i in range(file_size)
    )


TESTS = [(1, "2333133121414131402", 1928), (2, "2333133121414131402", 2858)]
# vim:expandtab:sw=4:ts=4
