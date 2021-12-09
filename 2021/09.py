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

    @staticmethod
    def neighbors(point: complex) -> list[complex]:
        """Return all the neighbors of a given point."""
        return [point + n for n in (1, -1, -1j, +1j)]

    @classmethod
    def lows(cls, depths: dict[complex, int]) -> list[complex]:
        """Return all the minimum points on the map."""
        return [
            point
            for point, depth in depths.items()
            if all(
                depth < depths[n] for n in cls.neighbors(point) if n in depths
            )
        ]

    def part1(self, lines: InputType) -> int:
        """Find all the low points on the map."""
        depths = lines
        return sum(depths[point] + 1 for point in self.lows(lines))

    def part2(self, lines: InputType) -> int:
        """Find the largest three basins.

        Simply remove 9's from the map and find the size of each island."""
        # Remove borders around the islands, i.e. points of height 9.
        unexplored = {point for point, depth in lines.items() if depth != 9}
        basin_sizes = []
        # Group points into islands. Pick any point and flood fill to neighboring points.
        while unexplored:
            in_basin = set()
            queue = set([unexplored.pop()])
            while queue:
                point = queue.pop()
                in_basin.add(point)
                for neighbor in self.neighbors(point):
                    if neighbor not in unexplored:
                        continue
                    queue.add(neighbor)
                    unexplored.remove(neighbor)
            basin_sizes.append(len(in_basin))

        return aoc.Helpers.mult(sorted(basin_sizes, reverse=True)[:3])

    def part2_slow(self, lines: InputType) -> int:
        """Find the largest three basins. Flood fill."""
        depths = lines
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

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data.

        Construct a map for coordinate -> depth.
        """
        grid = [[int(e) for e in line] for line in puzzle_input.splitlines()]
        depths = {x + y * 1j: grid[x][y] for x in range(len(grid)) for y in range(len(grid[0]))}
        return depths


if __name__ == "__main__":
    typer.run(Day09().run)
