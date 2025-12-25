#!/bin/python
"""Advent of Code, Day 23: Unstable Diffusion. Spread elves out across a field to plant trees."""

from typing import cast, Optional

from lib import aoc


N, S, E, W = -1j, 1j, 1, -1
DIRECTIONS = [
    (N, (N + W, N, N + E)),
    (S, (S + W, S, S + E)),
    (W, (N + W, W, S + W)),
    (E, (N + E, E, S + E)),
]
PARSER = aoc.CoordinatesParserC()


def simulate(positions: set[complex], step: int) -> set[complex]:
    """Simulate cycles of elves spreading out."""
    # Propose moves, check for conflicts.
    proposed = set()
    conflicted = set()
    choices = {}
    choice: Optional[complex]
    for elf in positions:
        # Check if the elf is stationary due to no neighbors.
        for direction in aoc.EIGHT_DIRECTIONS:
            if elf + direction in positions:
                break
        else:
            continue
        for option in (0, 1, 2, 3):  # a bit faster than range(4)
            move, checks = DIRECTIONS[(step + option) % 4]
            if (
                elf + checks[0] not in positions
                and elf + checks[1] not in positions
                and elf + checks[2] not in positions
            ):  # unroll to avoid calling all() or any() repeatedly.
                choice = elf + move
                if choice in proposed:
                    conflicted.add(choice)
                else:
                    proposed.add(choice)
                    choices[elf] = choice
                break
    # Execute moves when no conflict.
    new_positions = set()
    for elf in positions:
        choice = choices.get(elf)
        if choice is not None and choice not in conflicted:
            new_positions.add(choices[elf])
        else:
            new_positions.add(elf)

    # print()
    # print(f"== End of Round {step + 1} ==")
    # print(aoc.render(positions, ".", "#"))

    return new_positions


def solve(data: aoc.MapC, part: int) -> int:
    """Return the number of moves until the pattern is stable."""
    positions = cast(set[complex], data.coords["#"])
    for step in range(1500):
        new_positions = simulate(positions, step)
        if positions == new_positions:
            return step + 1
        positions = new_positions
        if part == 1 and step == 9:
            min_x, min_y, max_x, max_y = aoc.bounding_coords(positions)
            return int((max_x - min_x + 1) * (max_y - min_y + 1)) - len(positions)

    raise RuntimeError("Not found")

SAMPLE = """\
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""
TESTS = [(1, SAMPLE, 110), (2, SAMPLE, 20)]
