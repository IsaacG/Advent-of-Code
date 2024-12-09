#!/bin/python
"""Advent of Code, Guard Gallivant."""

from lib import aoc

SAMPLE = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""



class Day06(aoc.Challenge):
    """Guard Gallivant: simulate a guard walking a floor."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=41),
        aoc.TestCase(part=2, inputs=SAMPLE, want=6),
    ]

    def walk(
        self, all_spots: set[complex], blocked: set[complex], pos: complex, direction: complex
    ) -> tuple[set[complex], bool]:
        """Walk the map until hitting the edge or entering a loop."""
        spots: set[complex] = set()
        seen: set[complex] = set()
        while pos in all_spots:
            spots.add(pos)
            if pos + direction in blocked:
                if pos in seen:
                    return spots, True
                seen.add(pos)
                while pos + direction in blocked:
                    direction *= 1j
            pos += direction
        return spots, False

    def solver(self, puzzle_input: aoc.Map, part_one: bool) -> int:
        all_spots = puzzle_input.all_coords
        blocked = puzzle_input.coords["#"]
        start_pos, start_dir = next(
            (puzzle_input.coords[arrow].copy().pop(), aoc.ARROW_DIRECTIONS[arrow])
            for arrow in "<>v^"
            if arrow in puzzle_input.coords
        )

        spots, _ = self.walk(all_spots, blocked, start_pos, start_dir)
        # Part one: return the length of the path until the edge.
        if part_one:
            return len(spots)

        # Part two: count how many loops can be made by adding one obstable.
        return sum(
            self.walk(all_spots, blocked | {option}, start_pos, start_dir)[1]
            for option in spots - {start_pos}
        )

# vim:expandtab:sw=4:ts=4
