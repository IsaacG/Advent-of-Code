#!/bin/python
"""Advent of Code, Day 18: Boiling Boulders. Compute the surface area of 3D bubbles."""

from lib import aoc

SAMPLE = [
    "1,1,1\n2,1,1",
    """\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5""",
]


class Day18(aoc.Challenge):
    """Day 18: Boiling Boulders."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=10),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=64),
        aoc.TestCase(inputs=SAMPLE[1], part=2, want=58),
    ]
    INPUT_PARSER = aoc.ParseChain([
        aoc.ParseOneWordPerLine(lambda line: tuple(int(i) for i in line.split(","))),
        aoc.ParseOneWord(set),
    ])

    def part1(self, puzzle_input: set[tuple[int, int, int]]) -> int:
        """Return the number of lava surfaces which are not touching another lava."""
        points = puzzle_input
        directions = aoc.n_dim_directions(3)
        return sum(
            (x + a, y + b, z + c) not in points
            for x, y, z in points
            for a, b, c in directions
        )

    def part2(self, puzzle_input: set[tuple[int, int, int]]) -> int:
        """Return the number of exterior lava surfaces. Flood fill everything."""
        points = puzzle_input
        directions = aoc.n_dim_directions(3)

        # Create a bounding box around all of the lava.
        bounds = []
        for i in range(3):
            bounds.append((min(p[i] for p in points) - 1, max(p[i] for p in points) + 1))

        # Start in a corner.
        todo = {tuple(bounds[i][0] for i in range(3))}
        exterior = set()
        surfaces = 0
        # Flood fill.
        while todo:
            x, y, z = todo.pop()
            for a, b, c in directions:
                p2 = (x + a, y + b, z + c)
                # Check for bounding box.
                if not all(
                    bounds[i][0] <= p2[i] <= bounds[i][1]
                    for i in range(3)
                ):
                    continue
                if p2 in exterior:
                    continue
                if p2 in points:
                    surfaces += 1
                    continue
                exterior.add(p2)
                todo.add(p2)
        return surfaces
