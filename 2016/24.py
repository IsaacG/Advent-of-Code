#!/bin/python
"""Advent of Code, Day 24: Air Duct Spelunking.

Return the shortest path through a maze which hits certain points.
"""

import collections
import itertools
import string

from lib import aoc

SAMPLE = """\
###########
#0.1.....2#
#.#######.#
#4.......3#
###########"""

InputType = tuple[set[complex], dict[complex, int]]


class Day24(aoc.Challenge):
    """Day 24: Air Duct Spelunking."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=14),
        aoc.TestCase(inputs=SAMPLE, part=2, want=aoc.TEST_SKIP),
    ]

    def solver(self, parsed_input: InputType, param: bool) -> int:
        """Return the shortest path through a maze which hits certain points."""
        floor, wires = parsed_input

        # For each wire, use Dijkstra to find the shortest path to every other wire.
        distances: dict[int, dict[int, int]] = collections.defaultdict(dict)
        for start, wire in wires.items():
            todo: collections.deque[tuple[int, complex]] = collections.deque()
            seen = {start}
            todo.append((0, start))

            while todo:
                steps, position = todo.popleft()
                if position in wires:
                    other = wires[position]
                    if other in distances[wire]:
                        assert distances[wire][other] == steps
                    distances[wire][other] = steps
                    distances[other][wire] = steps  # Reverse checks for sanity checking.
                if len(distances[wire]) == len(wires):
                    # Stop exploring once all wire pairs are explored.
                    break

                next_steps = steps + 1
                for direction in aoc.FOUR_DIRECTIONS:
                    next_pos = position + direction
                    if next_pos in seen or next_pos not in floor:
                        continue
                    todo.append((next_steps, next_pos))
                    seen.add(next_pos)

        # Optionally append the start position to the end of the route.
        extra = (0,) if param else tuple()

        other_wires = set(wires.values()) - {0}
        # Find the shortest distrance that walks a specific wire path...
        shortest = min(
            sum(
                distances[a][b]
                for a, b in zip((0,) + path, path + extra)
            )
            # ... for all possible paths.
            for path in itertools.permutations(other_wires, len(other_wires))
        )

        return shortest

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        floor = {
            complex(x, y)
            for y, line in enumerate(puzzle_input.splitlines())
            for x, char in enumerate(line)
            if char != "#"
        }
        wires = {
            complex(x, y): int(char)
            for y, line in enumerate(puzzle_input.splitlines())
            for x, char in enumerate(line)
            if char in string.digits
        }
        return floor, wires
