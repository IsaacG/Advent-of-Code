#!/bin/python
"""Advent of Code, Day 3: Spiral Memory.

I was debating two approaches for p1.
I got lucky in picking the one that worked better for p2 so p2 was pretty simple.

I was thinking for p1 I could compute the solution without actually filling a
full spiral matrix by walking the diagonals.
1^2, 3^2, 5^2, 7^2, etc until the right "ring" then walking the "ring"
until I found the number.
But that wouldn't have helped for p2.

Instead, I went with the approach that I thought might be less efficient
but simpler to write: actually fill out a matrix.
I was able to reuse that p1 code for p2.
"""
from lib import aoc
ROTATE_LEFT = 1j


def solve(data: int, part: int) -> int:
    """Fill out a spiral matrix until we get to the input number."""
    location = complex(0, 0)
    direction = complex(0, -1)
    number = 1

    matrix = {location: number}
    for number in range(2, data + 1):
        if location + direction * ROTATE_LEFT not in matrix:
            direction *= ROTATE_LEFT
        location += direction
        if part == 1:
            value = number
        else:
            value = sum(
                matrix.get(location + offset, 0) for offset in aoc.EIGHT_DIRECTIONS)
        matrix[location] = value
        if part == 2 and value > data:
            return value

    return int(abs(location.real) + abs(location.imag))


TESTS = [(1, "1024", 31), (2, "747", 806)]
# vim:expandtab:sw=4:ts=4
