#!/usr/bin/env python
"""Day 11. Ferry Seating Area a.k.a. Conway's Game of Life."""

import data as inputs
from lib import aoc


def solve(data: aoc.Map, part: int) -> int:
    """Determine how many seats are in use."""
    seats = data.coords.get("#", set()) | data.coords["L"]
    occupied = data.coords.get("#", set())
    board = set(data.chars.keys())
    limit = 4 if part == 1 else 5
    prior = {0}
    while prior != occupied:

        def look(pos, direction):
            x, y = pos
            dx, dy = direction
            x += dx
            y += dy
            if part == 1:
                return (x, y) in occupied
            while (x, y) in board:
                if (x, y) in occupied:
                    return True
                if (x, y) in seats:
                    return False
                x += dx
                y += dy
            return False

        new = set()
        for seat in seats:
            adjacent_occupied = sum(look(seat, d) for d in aoc.EIGHT_DIRECTIONS_T)
            if seat not in occupied:
                if adjacent_occupied == 0:
                    new.add(seat)
            else:
                if adjacent_occupied < limit:
                    new.add(seat)
        prior, occupied = occupied, new

    return len(occupied)


S1 = inputs.D11S1
S2 = inputs.D11S2
TESTS = [(1, S1[0], 37), (2, S2[0], 26)]
