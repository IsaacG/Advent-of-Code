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
InputType = tuple[tuple[int, int], set[complex], set[complex]]


class Day21(aoc.Challenge):
    """Day 21: Step Counter."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=16),
        aoc.TestCase(inputs=SAMPLE, part=2, want=aoc.TEST_SKIP),
    ]
    TIMEOUT = 60
    # Get coordinates of start, garden.
    INPUT_PARSER = aoc.CharCoordinatesParser("S.")

    def walk(self, start: set[complex], garden: set[complex], steps: int) -> int:
        """Return reachable coordinates after walking N steps from the start."""
        for _ in range(steps):
            new: set[complex] = set()
            # Expand all coordinates to their neighbors.
            for coord in start:
                new.update(aoc.neighbors(coord))
            # Restrict to valid locations.
            start = new & garden
        return len(start)

    def part1(self, puzzle_input: InputType) -> int:
        """Return the number of reachable locations in 64 steps."""
        _, start, garden = puzzle_input
        garden.update(start)
        steps = 64
        if self.testing:
            steps = 6
        return self.walk(start, garden, steps)

    def part2(self, puzzle_input: InputType) -> int:
        """Return the number of reachable locations in many steps."""
        (size, _), start, garden = puzzle_input
        garden.update(start)
        steps = 26501365

        four_directions = [complex(1, 0), complex(0, -1), complex(-1, 0), complex(0, 1)]
        half_size = (size - 1) // 2
        center = complex(half_size, half_size)  # This should be the start location.

        centered_edges = [center + half_size * direction for direction in four_directions]
        corners = [center + center * direction for direction in four_directions]

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
