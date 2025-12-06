#!/bin/python
"""Advent of Code, Day 9: Explosives in Cyberspace. Compute the length of an encoded sequence."""

from lib import aoc

SAMPLE = [
    ('ADVENT', 'ADVENT'),
    ('A(1x5)BC', 'ABBBBBC'),
    ('(3x3)XYZ', 'XYZXYZXYZ'),
    ('A(2x2)BCD(2x2)EFG', 'ABCBCDEFEFG'),
    ('(6x1)(1x3)A', '(1x3)A'),
    ('X(8x2)(3x3)ABCY', 'X(3x3)ABC(3x3)ABCY'),
    ('(3x3)XYZ', len('XYZXYZXYZ')),
    ('X(8x2)(3x3)ABCY', len('XABCABCABCABCABCABCY')),
    ('(27x12)(20x12)(13x14)(7x10)(1x12)A', 241920),
    ('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN', 445),
]


class Day09(aoc.Challenge):
    """Day 9: Explosives in Cyberspace."""

    TESTS = [
        aoc.TestCase(inputs=i[0], part=1, want=len(i[1])) for i in SAMPLE[:6]
    ] + [
        aoc.TestCase(inputs=i[0], part=2, want=i[1]) for i in SAMPLE[6:]
    ]

    def solver(self, puzzle_input: str, part_one: bool) -> int:
        """Compute the length of an encoded sequence."""
        length = 0
        data = list(reversed(puzzle_input))

        while data:
            char = data.pop()
            if char != "(":
                length += 1
            else:
                buf = []
                while (char := data.pop()) != ")":
                    buf.append(char)
                sub_count, repeat = "".join(buf).split("x")
                sub_sequence = "".join(data.pop() for _ in range(int(sub_count)))
                sub_length = self.solver(sub_sequence, part_one) if not part_one else len(sub_sequence)
                length += int(repeat) * sub_length

        return length
