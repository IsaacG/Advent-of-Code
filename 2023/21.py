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

# Size, starting position, rocks
InputType = tuple[tuple[int, int], set[complex], set[complex]]


class Day21(aoc.Challenge):
    """Day 21: Step Counter."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=16),
        aoc.TestCase(inputs=SAMPLE, part=2, want=1),
    ]
    # Get coordinates of start, rocks.
    INPUT_PARSER = aoc.CharCoordinatesParser("S#")

    def walk(self, size, start, rocks, steps):
        """Return reachable coordinates after walking N steps from the start."""
        for _ in range(steps):
            new = set()
            for coord in start:
                for neighbor in aoc.neighbors(coord):
                    if complex(neighbor.real % size, neighbor.imag % size) not in rocks:
                        new.add(neighbor)
            start = new
        return start

    def part1(self, parsed_input: InputType) -> int:
        """Return the number of reachable locations in 64 steps."""
        (size, _), start, rocks = parsed_input
        steps = 64
        if self.testing:
            steps = 6
        return len(self.walk(size, start, rocks, steps))

    def test_p2(self, parsed_input: InputType) -> int:
        """Run the part 2 tests."""
        steps_count = [(6, 16), (10, 50), (50, 1594), (100, 6536)]

        (size, _), start, rocks = parsed_input
        for steps, want in steps_count:
            got = len(self.walk(size, start, rocks, steps))
            assert got == want, f"{(steps, want, got)=}"
        return 1

    def part2(self, parsed_input: InputType) -> int:
        """Return the number of reachable locations in many steps."""
        if self.testing:
            return self.test_p2(parsed_input)
        (size, _), start, rocks = parsed_input
        steps = 26501365

        half_size = (size - 1) // 2
        expansions = (steps - half_size) // size

        # Explore the garden for 2 garden lengths to compute garden values.
        # Those garden values are then used to multiply and compute the expanded version
        # since they expand in a reliable pattern.
        # See notes.
        manual_expansions = 2
        reach = self.walk(size, start, rocks, half_size + manual_expansions * size)

        # Chunk up the reachable locations into a grid of gardens.
        rows = []
        for offset_y in range(-manual_expansions, manual_expansions + 1):
            row = []
            top = size * offset_y
            bottom = top + size
            for offset_x in range(-manual_expansions, manual_expansions + 1):
                left = size * offset_x
                right = left + size
                num = len(
                    {
                        coord for coord in reach
                        if left <= coord.real < right and top <= coord.imag < bottom
                    }
                )
                row.append(num)
            rows.append(row)
            self.debug(" | ".join(f"{r:5}" for r in row))
        self.debug("")

        # The pointy tips. Top/bottom center and extreme right/right.
        tips = rows[0][2] + rows[-1][2] + rows[2][0] + rows[2][-1]
        # The edges have two types of gardens: 1/4 filled and 3/4 filled.
        short_diag = rows[0][1] + rows[0][3] + rows[-1][1] + rows[-1][3]
        large_diag = rows[1][1] + rows[1][3] + rows[3][1] + rows[3][3]
        # Interior gardens alternate.
        interior_center = rows[2][2]
        interior_even = rows[2][1]

        return (
            tips
            + (expansions - 1) * large_diag
            + expansions * short_diag
            + interior_center * (expansions - 1) ** 2
            + interior_even * expansions ** 2
        )

# vim:expandtab:sw=4:ts=4
