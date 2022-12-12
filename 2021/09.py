#!/bin/python
"""Advent of Code: Day 09."""

import typer

from lib import aoc

InputType = dict[complex, int]

SAMPLE = ["""\
2199943210
3987894921
9856789892
8767896789
9899965678
"""]


class Day09(aoc.Challenge):
    """Find low points and basins in a topographic map."""

    DEBUG = True

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=15),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=1134),
    )

    @classmethod
    def lows(cls, depths: aoc.Board) -> list[complex]:
        """Return all the minimum points on the map."""
        return [
            point
            for point, depth in depths.items()
            if all(
                depth < v for v in depths.neighbors(point).values()
            )
        ]

    def part1(self, parsed_input: InputType) -> int:
        """Find all the low points on the map."""
        depths = parsed_input
        return sum(depths[point] + 1 for point in self.lows(parsed_input))

    def part2(self, parsed_input: InputType) -> int:
        """Find the largest three basins.

        Simply remove 9's from the map and find the size of each island."""
        # Remove borders around the islands, i.e. points of height 9.
        unexplored = {point for point, depth in parsed_input.items() if depth != 9}
        basin_sizes = []
        # Group points into islands. Pick any point and flood fill to neighboring points.
        while unexplored:
            in_basin = set()
            queue = set([unexplored.pop()])
            while queue:
                point = queue.pop()
                in_basin.add(point)
                for neighbor in parsed_input.neighbors(point):
                    if neighbor not in unexplored:
                        continue
                    queue.add(neighbor)
                    unexplored.remove(neighbor)
            basin_sizes.append(len(in_basin))

        return aoc.Helpers.mult(sorted(basin_sizes, reverse=True)[:3])

    def part2_slow(self, parsed_input: InputType) -> int:
        """Find the largest three basins. Flood fill."""
        depths = parsed_input
        basin_sizes = []
        # For each minimum, explore the basin.
        for lowpoint in self.lows(depths):
            in_basin = set()
            # Djiksta's algorithm.
            todo = set([lowpoint])
            while todo:
                # Flood fill, lowest depths to highest.
                point = sorted(todo, key=lambda x: depths[x])[0]
                todo.remove(point)
                # Examine all neighboring spots that are not yet added to the basin.
                neighbors = [n for n in self.neighbors(point) if n in depths and n not in in_basin]
                # If this spot is lower/equal to all unflooded neighbors, add it to the basin.
                if all(depths[n] >= depths[point] for n in neighbors):
                    in_basin.add(point)
                    # Add all neighbors as possible basic members. Do not include 9's.
                    todo.update(n for n in neighbors if depths[n] != 9)
            basin_sizes.append(len(in_basin))

        return aoc.Helpers.mult(sorted(basin_sizes, reverse=True)[:3])

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return aoc.Board.from_int_block(puzzle_input, diagonal=False)


if __name__ == "__main__":
    typer.run(Day09().run)
