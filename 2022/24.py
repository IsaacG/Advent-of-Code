#!/bin/python
"""Advent of Code, Day 24: Blizzard Basin. Navigate across a basic, avoiding storms."""
from __future__ import annotations

import dataclasses
import queue

import typer
from lib import aoc

SAMPLE = """\
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""
MAX_STEPS = 1000


@dataclasses.dataclass
class Basin:
    """Map a basic and the storm patterns."""

    walls: set[complex]
    blizzards: dict[complex, set[complex]]
    width: int
    height: int

    def __post_init__(self) -> None:
        """Compute storm patterns and entrance/exit."""
        self.entrance = complex(1, 0)
        self.exit_pos = complex(self.width - 2, self.height - 1)
        self.blocked = self.compute_blocked()

    def compute_blocked(self) -> list[set[complex]]:
        """Compute MAX_STEPS iterations of the blizzard."""
        blizzards = self.blizzards
        blocked = []

        for _ in range(MAX_STEPS):
            next_blizzards = {}
            for direction, storms in blizzards.items():
                new_storms = set()
                for storm in storms:
                    storm += direction
                    if storm.real == self.width - 1:
                        storm = complex(1, storm.imag)
                    elif storm.real == 0:
                        storm = complex(self.width - 2, storm.imag)
                    elif storm.imag == 0:
                        storm = complex(storm.real, self.height - 2)
                    elif storm.imag == self.height - 1:
                        storm = complex(storm.real, 1)
                    new_storms.add(storm)
                next_blizzards[direction] = new_storms
            blizzards = next_blizzards
            blocked.append(set.union(self.walls, *blizzards.values()))
        return blocked

    @classmethod
    def input_parser(cls, puzzle_input: str) -> Basin:
        """Build a Basin from the input."""
        positions: dict[str, set[complex]] = {char: set() for char in "#><v^"}
        width = len(puzzle_input.splitlines()[0])
        height = len(puzzle_input.splitlines())
        # Map coordinates to chars.
        for y_pos, line in enumerate(puzzle_input.splitlines()):
            for x_pos, char in enumerate(line):
                if char == ".":
                    continue
                positions[char].add(complex(x_pos, y_pos))
        char_to_dir = {">": 1, "<": -1, "v": 1j, "^": -1j}
        blizzards = {direction: positions[char] for char, direction in char_to_dir.items()}
        return cls(
            walls=positions["#"],
            blizzards=blizzards,
            width=width,
            height=height,
        )


class Day24(aoc.Challenge):
    """Day 24: Blizzard Basin."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=18),
        aoc.TestCase(inputs=SAMPLE, part=2, want=54),
    ]
    DEBUG = False
    INPUT_PARSER = aoc.ParseOneWord(Basin.input_parser)
    PARAMETERIZED_INPUTS = [1, 3]

    def navigate(self, basin: Basin, reverse: bool, init_steps: int) -> int:
        """Return move count after navigating from one side of the basin to the other."""
        blocked = basin.blocked
        start, end = basin.entrance, basin.exit_pos
        if reverse:
            start, end = end, start

        to_explore: queue.Queue[tuple[float, int, float, float]] = queue.PriorityQueue()
        to_explore.put((0, init_steps, start.real, start.imag))
        cur = start
        seen = set()
        with self.context_timer("Compute path"):
            # A-star exploration.
            # Heuristic: moves taken + Manhattan distance to the end.
            while cur != end:
                _, moves, cur_x, cur_y = to_explore.get()
                # complex values cannot be compared so store them by component.
                cur = complex(cur_x, cur_y)
                for direction in aoc.FOUR_DIRECTIONS + [0]:
                    next_pos = cur + direction
                    # Do not allow moving outside the basin.
                    if next_pos.imag < 0 or next_pos.imag >= basin.height:
                        continue
                    if next_pos in blocked[moves]:
                        continue
                    if (moves + 1, next_pos) in seen:
                        continue
                    seen.add((moves + 1, next_pos))
                    distance_to_end = abs(next_pos.real - end.real) + abs(next_pos.imag - end.imag)
                    to_explore.put(
                        (moves + distance_to_end, moves + 1, next_pos.real, next_pos.imag)
                    )
        return moves

    def solver(self, parsed_input: Basin, trip_count: int) -> int:
        """Solve for n trips across the basin."""
        moves = 0
        for i in range(trip_count):
            moves = self.navigate(parsed_input, bool(i % 2), moves)
            self.debug(f"{i}: {moves=}")
        return moves


if __name__ == "__main__":
    typer.run(Day24().run)

# vim:expandtab:sw=4:ts=4
