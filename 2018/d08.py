#!/bin/python
"""Advent of Code, Day 8: Memory Maneuver."""

from lib import aoc

SAMPLE = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
InputType = list[int]


class Day08(aoc.Challenge):
    """Day 8: Memory Maneuver."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=138),
        aoc.TestCase(inputs=SAMPLE, part=2, want=66),
    ]
    INPUT_PARSER = aoc.parse_multi_int_per_line

    def part1(self, puzzle_input: InputType) -> int:
        """Return the sum of all nodes."""
        reader = iter(puzzle_input[0])

        def parser():
            child_count = next(reader)
            metadata_count = next(reader)
            children = sum((parser() for _ in range(child_count)), 0)
            metadata = sum((next(reader) for _ in range(metadata_count)), 0)
            return children + metadata

        return parser()

    def part2(self, puzzle_input: InputType) -> int:
        """Return the value of the root node."""
        reader = iter(puzzle_input[0])

        def parser():
            child_count = next(reader)
            metadata_count = next(reader)
            if child_count == 0:
                return sum((next(reader) for _ in range(metadata_count)), 0)
            children = [parser() for _ in range(child_count)]
            metadata = [next(reader) - 1 for _ in range(metadata_count)]
            return sum(children[i] for i in metadata if i < child_count)

        return parser()
