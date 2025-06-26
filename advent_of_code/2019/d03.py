#!/usr/bin/env python
"""2019 Day 3: Crossed Wires."""

from lib import aoc

DIRS = aoc.LETTER_DIRECTIONS

SAMPLES = [
    'R8,U5,L5,D3\nU7,R6,D4,L4',
    'R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83',
    'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7',
]


class Day03(aoc.Challenge):
    """Compute where wires cross and find the min cost of a crossing."""

    TESTS = (
        aoc.TestCase(inputs=SAMPLES[0], part=1, want=6),
        aoc.TestCase(inputs=SAMPLES[1], part=1, want=159),
        aoc.TestCase(inputs=SAMPLES[2], part=1, want=135),
        aoc.TestCase(inputs=SAMPLES[0], part=2, want=30),
        aoc.TestCase(inputs=SAMPLES[1], part=2, want=610),
        aoc.TestCase(inputs=SAMPLES[2], part=2, want=410),
    )

    def solve(self, puzzle_input: list[str], part: int) -> int:
        """Walk the two wires.

        For wire 1, save locations visited and steps.
        For wire two, on intersection, save `cost`.
        Return min cost.
        """
        spots = {}
        intersections = set()

        def save_steps(cur, steps):
            if cur not in spots:
                spots[cur] = steps

        def save_cost(cur, steps):
            if cur in spots:
                if part == 1:
                    # Manhatten distance.
                    cost = abs(int(cur.real)) + abs(int(cur.imag))
                else:
                    # Combined steps.
                    cost = spots[cur] + steps
                intersections.add(cost)

        def walk_wire(wire, func):
            steps = 0
            cur = 0
            for piece in wire:
                direction = DIRS[piece[0]]
                count = int(piece[1:])
                for _ in range(count):
                    steps += 1
                    cur += direction
                    func(cur, steps)

        walk_wire(puzzle_input[0], save_steps)
        walk_wire(puzzle_input[1], save_cost)
        return min(intersections)

    def part2(self, puzzle_input: list[str]) -> int:
        """Wire cross cost: combined step count."""
        return self.solve(puzzle_input, 2)

    def part1(self, puzzle_input: list[str]) -> int:
        """Wire cross cost: Manhatten distance."""
        return self.solve(puzzle_input, 1)

    def input_parser(self, puzzle_input: str):
        return [line.split(',') for line in puzzle_input.split('\n')]

# vim:ts=2:sw=2:expandtab
