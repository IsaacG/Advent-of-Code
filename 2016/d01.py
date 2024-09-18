#!/bin/python
"""Advent of Code, Day 1: No Time for a Taxicab. Compute how far we travelled."""

from lib import aoc

SAMPLE = [
    'R2, L3',
    'R2, R2, R2',
    'R5, L5, R5, R3',
    'R8, R4, R4, R8',
]

LineType = list[str]
InputType = list[LineType]


class Day01(aoc.Challenge):
    """Day 1: No Time for a Taxicab."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=5),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=2),
        aoc.TestCase(inputs=SAMPLE[2], part=1, want=12),
        aoc.TestCase(inputs=SAMPLE[3], part=2, want=4),
    ]
    INPUT_PARSER = aoc.parse_re_findall_str(r"[LR]\d+")

    def solver(self, puzzle_input: InputType, part_one: bool) -> int:
        """Compute how far we walked."""
        p2 = not part_one
        cur = complex(0, 0)
        seen = {cur}
        heading = complex(0, 1)

        for instruction in puzzle_input[0]:
            rot, dist = instruction[0], int(instruction[1:])
            heading *= {"R": -1j, "L": +1j}[rot]
            for _ in range(dist):
                cur += heading
                if p2 and cur in seen:
                    return int(abs(cur.real) + abs(cur.imag))
                seen.add(cur)

        return int(abs(cur.real) + abs(cur.imag))
