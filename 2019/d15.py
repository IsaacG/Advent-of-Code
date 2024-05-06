#!/bin/python
"""Advent of Code, Day 15: Oxygen System."""

import functools
import itertools

import intcode
from lib import aoc

DIRECTIONS = {
    complex(0, +1): 1,  # North
    complex(0, -1): 2,  # South
    complex(-1, 0): 3,  # West
    complex(+1, 0): 4,  # East
}
BOT_WALL = 0
BOT_MOVED = 1
BOT_FOUND = 2
# Based on benchmarking
BACKTRACK_LIMIT = 24


class Day15(aoc.Challenge):
    """Day 15: Oxygen System."""

    TESTS = [
        aoc.TestCase(inputs="", part=1, want=aoc.TEST_SKIP),
        aoc.TestCase(inputs="", part=2, want=aoc.TEST_SKIP),
    ]
    INPUT_PARSER = aoc.parse_one_str
    PARAMETERIZED_INPUTS = [False, True]

    @functools.cache
    def explore(self, program: str) -> tuple[set[complex], set[complex], complex]:
        """Explore the map by moving around, backtracking at dead ends."""
        # Track discovered hallways, walls and oxygen.
        hall = {complex()}
        wall: set[complex] = set()
        oxygen: complex | None = None
        # Track pathways from the start to any given location.
        # May not be the shortest path.
        # Potential optimization: compute shortest known path on the fly.
        paths: dict[complex, list[complex]] = {complex(): []}

        # Explore until we explored the entire map.
        while True:
            explored = hall | wall
            # Find any positions with unexplored adjacencies.
            candidates = {
                pos for pos in hall
                if any(pos + direction not in explored for direction in DIRECTIONS)
            }
            # All locations were explored.
            if not candidates:
                assert oxygen is not None
                return hall, wall, oxygen

            computer = intcode.Computer(program, debug=self.DEBUG)

            def move(direction: complex) -> int:
                computer.input.append(DIRECTIONS[direction])
                computer.run()
                return computer.output.popleft()

            direction: complex | None
            # Select a location and navigate to it.
            pos = candidates.pop()
            path = paths[pos]
            for direction in path:
                move(direction)

            # From this location, explore the area.
            # When there are no explored adjacencies, backtrack.
            backtrack_limit = BACKTRACK_LIMIT
            while backtrack_limit:
                # Find the next unexplored adjacency.
                while direction := next(
                    (direction for direction in DIRECTIONS if pos + direction not in explored),
                    None,
                ):
                    backtrack_limit = BACKTRACK_LIMIT
                    new_pos = pos + direction
                    explored.add(new_pos)
                    candidates.discard(new_pos)
                    got = move(direction)
                    # If we hit a wall, record it and continue.
                    if got == BOT_WALL:
                        wall.add(new_pos)
                        continue
                    # Not a wall? New location discovered. Track it. Update state.
                    if got == BOT_FOUND:
                        oxygen = new_pos
                    hall.add(new_pos)
                    path = path + [direction]
                    paths[new_pos] = path
                    pos = new_pos
                # Got to a dead end. Backtrack when possible.
                if not path:
                    break
                backtrack_limit -= 1
                direction = path[-1]
                path = path[:-1]
                pos -= direction
                move(-direction)

    def solver(self, parsed_input: str, param: bool) -> int:
        """Return the steps needed to find the oxygen or for the oxygen to fill the room."""
        hall, wall, oxygen = self.explore(parsed_input)
        start = complex()

        total_space = len(hall)
        filled = {oxygen}
        # Breadth first expand from the oxygen location until either
        # (part one) we reach the start, which gives the steps, or
        # (part two) we fill all possible space.
        for step in itertools.count():
            if len(filled) == total_space:
                return step
            if not param and start in filled:
                return step
            new = {
                pos + direction for pos in filled for direction in DIRECTIONS
                if pos + direction not in wall
            }
            filled.update(new)
        raise RuntimeError("Not found")

# vim:expandtab:sw=4:ts=4
