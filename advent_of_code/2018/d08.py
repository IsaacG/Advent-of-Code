#!/bin/python
"""Advent of Code, Day 8: Memory Maneuver."""


def solve(data: list[int], part: int) -> int:
    """Return the sum of nodes."""
    reader = iter(data)

    def parser():
        child_count = next(reader)
        metadata_count = next(reader)
        if part == 1:
            # All nodes.
            children = sum((parser() for _ in range(child_count)), 0)
            metadata = sum((next(reader) for _ in range(metadata_count)), 0)
            return children + metadata
        else:
            # Root node.
            if child_count == 0:
                return sum((next(reader) for _ in range(metadata_count)), 0)
            children = [parser() for _ in range(child_count)]
            metadata = [next(reader) - 1 for _ in range(metadata_count)]
            return sum(children[i] for i in metadata if i < child_count)

    return parser()


SAMPLE = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
TESTS = [(1, SAMPLE, 138), (2, SAMPLE, 66)]
