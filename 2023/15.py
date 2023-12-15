#!/bin/python
"""Advent of Code, Day 15: Lens Library."""

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

    def part1(self, parsed_input: str) -> int:
        """Return summed hashes."""
        return sum(self.hash(word) for word in parsed_input.split(","))

    def part2(self, parsed_input: str) -> int:
        """Return which lenses are in the boxes."""
        boxes = [[] for _ in range(256)]

        for word in parsed_input.split(","):
            if word.endswith("-"):
                label = word.removesuffix("-")
                box = self.hash(label)
                # Remove lenses with a matching label.
                boxes[box] = [
                    (lens_label, lens_length)
                    for lens_label, lens_length in boxes[box]
                    if lens_label != label
                ]
            else:
                label, length = word.split("=")
                box = self.hash(label)
                if any(lens_label == label for lens_label, _ in boxes[box]):
                    # Label already exists; update the length.
                    boxes[box] = [
                        (lens_label, length if lens_label == label else lens_length)
                        for lens_label, lens_length in boxes[box]
                    ]
                else:
                    # Add a new lens.
                    boxes[box].append((label, length))

        # Sum up the lenses.
        result = 0
        for idx_box, lenses in enumerate(boxes, start=1):
            for idx_lens, (_, length) in enumerate(lenses, start=1):
                result += idx_box * idx_lens * int(length)
        return result


# vim:expandtab:sw=4:ts=4
