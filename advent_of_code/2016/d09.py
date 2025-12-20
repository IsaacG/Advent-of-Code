#!/bin/python
"""Advent of Code, Day 9: Explosives in Cyberspace. Compute the length of an encoded sequence."""


def solve(data: str, part: int) -> int:
    """Compute the length of an encoded sequence."""
    length = 0
    chars = list(reversed(data))

    while chars:
        char = chars.pop()
        if char != "(":
            length += 1
        else:
            buf = []
            while (char := chars.pop()) != ")":
                buf.append(char)
            sub_count, repeat = "".join(buf).split("x")
            sub_sequence = "".join(chars.pop() for _ in range(int(sub_count)))
            sub_length = solve(sub_sequence, part) if part == 2 else len(sub_sequence)
            length += int(repeat) * sub_length

    return length


SAMPLE1 = [
    ('ADVENT', 'ADVENT'),
    ('A(1x5)BC', 'ABBBBBC'),
    ('(3x3)XYZ', 'XYZXYZXYZ'),
    ('A(2x2)BCD(2x2)EFG', 'ABCBCDEFEFG'),
    ('(6x1)(1x3)A', '(1x3)A'),
    ('X(8x2)(3x3)ABCY', 'X(3x3)ABC(3x3)ABCY'),
]
SAMPLE2 = [
    ('(3x3)XYZ', len('XYZXYZXYZ')),
    ('X(8x2)(3x3)ABCY', len('XABCABCABCABCABCABCY')),
    ('(27x12)(20x12)(13x14)(7x10)(1x12)A', 241920),
    ('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN', 445),
]
TESTS = [
    (1, i[0], len(i[1])) for i in SAMPLE1
] + [
    (2, i[0], i[1]) for i in SAMPLE2
]
