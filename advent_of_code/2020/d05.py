#!/usr/bin/env python
"""AoC Day 5: Binary Boarding."""

# Translate F to 0, B to 1, L to 0 and R to 1.
transmap = str.maketrans('FBLR', '0101')


def solve(data: list[str], part: int) -> int:
    """Determine the ID of a seat."""
    # Translate to binary string then to int.
    seats = {int(s.translate(transmap), 2) for s in data}
    if part == 1:
        # Part one: max seat number
        return max(seats)

    # Part two: find a gap of one between two seats.
    for s in seats:
        if (s + 1) not in seats and (s + 2) in seats:
            return s + 1
    raise RuntimeError


PARSER = str.splitlines
TESTS = [
    (1, 'BFFFBBFRRR', 567),
    (1, 'FFFBBBFRRR', 119),
    (1, 'BBFFBBFRLL', 820),
]
