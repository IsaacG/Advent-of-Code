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


class Day03(aoc.Challenge):
    """Day 3: Spiral Memory."""

    TESTS = [
        aoc.TestCase(inputs="1024", part=1, want=31),
        aoc.TestCase(inputs="747", part=2, want=806),
    ]

    def solver(self, puzzle_input: int, part_one: bool) -> int:
        """Fill out a spiral matrix until we get to the input number."""
        location = complex(0, 0)
        direction = complex(0, -1)
        number = 1

        matrix = {location: number}
        for number in range(2, puzzle_input + 1):
            if location + direction * ROTATE_LEFT not in matrix:
                direction *= ROTATE_LEFT
            location += direction
            if part_one:
                value = number
            else:
                value = sum(
                    matrix.get(location + offset, 0) for offset in aoc.EIGHT_DIRECTIONS)
            matrix[location] = value
            if not part_one and value > puzzle_input:
                return value

        return int(abs(location.real) + abs(location.imag))

# vim:expandtab:sw=4:ts=4
