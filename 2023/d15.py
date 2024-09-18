#!/bin/python
"""Advent of Code, Day 15: Lens Library."""

import collections
from lib import aoc

SAMPLE = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"

class Day15(aoc.Challenge):
    """Day 15: Lens Library."""

    TESTS = [
        aoc.TestCase(inputs="HASH", part=1, want=52),
        aoc.TestCase(inputs=SAMPLE, part=1, want=1320),
        aoc.TestCase(inputs=SAMPLE, part=2, want=145),
    ]
    INPUT_PARSER = aoc.parse_one_str

    def hash(self, word: str) -> int:
        """Compute the HASH of a word."""
        value = 0
        for char in word:
            value = (value + ord(char)) * 17
        return value % 256

    def part1(self, puzzle_input: str) -> int:
        """Return summed hashes."""
        return sum(self.hash(word) for word in puzzle_input.split(","))

    def part2(self, puzzle_input: str) -> int:
        """Return which lenses are in the boxes."""
        boxes = collections.defaultdict(dict)
        
        def get_box(label):
            return boxes[self.hash(label)]

        for word in puzzle_input.split(","):
            if word.endswith("-"):
                label = word.removesuffix("-")
                get_box(label).pop(label, None)
            else:
                label, length = word.split("=")
                get_box(label)[label] = length

        # Sum up the lenses.
        result = 0
        for idx_box, lenses in boxes.items():
            for idx_lens, length in enumerate(lenses.values(), start=1):
                result += (idx_box + 1) * idx_lens * int(length)
        return result


# vim:expandtab:sw=4:ts=4
