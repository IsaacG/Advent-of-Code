#!/bin/python
"""Advent of Code, Day 21: Step Counter."""

from lib import aoc

SAMPLE = """\
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""

# Size, starting position, garden
InputType = tuple[tuple[int, int], set[tuple[int, int]], set[tuple[int, int]]]


class Day21(aoc.Challenge):
    """Day 21: Step Counter."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=16),
        aoc.TestCase(inputs=SAMPLE, part=2, want=aoc.TEST_SKIP),
    ]

    def walk(self, start: set[tuple[int, int]], garden: set[tuple[int, int]], steps: int) -> int:
        """Return reachable coordinates after walking N steps from the start."""
        for _ in range(steps):
            new = set[tuple[int, int]]()
            # Expand all coordinates to their neighbors.
            for coord in start:
                new.update(aoc.t_neighbors4(coord))
            # Restrict to valid locations.
            start = new & garden
        return len(start)

    def part1(self, puzzle_input: InputType) -> int:
        """Return the number of reachable locations in 64 steps."""
        start, garden = puzzle_input.get_coords("S.")
        garden.update(start)
        steps = 64
        if self.testing:
            steps = 6
        return self.walk(start, garden, steps)

    def part2(self, puzzle_input: InputType) -> int:
        """Return the number of reachable locations in many steps."""
        size, (start, garden) = puzzle_input.size, puzzle_input.get_coords("S.")
        garden.update(start)
        steps = 26501365

        four_directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        half_size = (size - 1) // 2
        max_x = puzzle_input.max_x
        max_y = puzzle_input.max_y
        center = (half_size, half_size)  # This should be the start location.

        centered_edges = [(max_x, half_size), (half_size, 0), (0, half_size), (half_size, max_y)]
        corners = [(max_x, max_y), (max_x, 0), (0, 0), (0, max_y)]

        # Start at the middle of an edge and walk to the far side.
        tips = sum(self.walk({start}, garden, size - 1) for start in centered_edges)
        # Start at the middle of two edges.
        large_diag = sum(
            self.walk({centered_edges[i], centered_edges[(i + 1) % 4]}, garden, size - 1)
            for i in range(4)
        )
        # Start at a corner.
        short_diag = sum(self.walk({start}, garden, half_size - 1) for start in corners)
        interior_center = self.walk({center}, garden, size)
        interior_even = self.walk({center}, garden, size - 1)

        expansions = (steps - half_size) // size
        return (
            tips
            + (expansions - 1) * large_diag
            + expansions * short_diag
            + interior_center * (expansions - 1) ** 2
            + interior_even * expansions ** 2
        )

# vim:expandtab:sw=4:ts=4
