#!/bin/python
"""Advent of Code, Day 23: Unstable Diffusion. Spread elves out across a field to plant trees."""

import collections

import typer
from lib import aoc

SAMPLE = """\
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""


InputType = set[complex]

N, S, E, W = -1j, 1j, 1, -1
DIRECTIONS = [
    (N, (N + W, N, N + E)),
    (S, (S + W, S, S + E)),
    (W, (N + W, W, S + W)),
    (E, (N + E, E, S + E)),
]


class Day23(aoc.Challenge):
    """Day 23: Unstable Diffusion."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=110),
        aoc.TestCase(inputs=SAMPLE, part=2, want=20),
    ]
    INPUT_PARSER = aoc.parse_ascii_bool_map("#")
    PARAMETERIZED_INPUTS = [1, 2]

    def solver(self, parsed_input: InputType, part: int) -> int:
        """Simulate cycles of elves spreading out."""
        positions = parsed_input
        for step in range(1000000):
            # Propose moves, check for conflicts.
            proposed: dict[complex, int] = collections.defaultdict(int)
            choices = {}
            for elf in positions:
                if not any(elf + direction in positions for direction in aoc.EIGHT_DIRECTIONS):
                    continue
                for option in range(4):
                    move, checks = DIRECTIONS[(step + option) % 4]
                    if all(elf + check not in positions for check in checks):
                        choice = elf + move
                        proposed[choice] += 1
                        choices[elf] = choice
                        break
            # Execute moves when no conflict.
            new_positions = set()
            for elf in positions:
                if elf in choices and proposed[choices[elf]] == 1:
                    new_positions.add(choices[elf])
                else:
                    new_positions.add(elf)

            # print()
            # print(f"== End of Round {step + 1} ==")
            # print(aoc.render(positions, ".", "#"))

            if part == 1 and step == 9:
                min_x = min(elf.real for elf in positions)
                max_x = max(elf.real for elf in positions)
                min_y = min(elf.imag for elf in positions)
                max_y = max(elf.imag for elf in positions)
                answer = int((max_x - min_x + 1) * (max_y - min_y + 1)) - len(positions)
                return answer
            if part == 2 and positions == new_positions:
                return step + 1

            positions = new_positions

        raise RuntimeError("Not found")


if __name__ == "__main__":
    typer.run(Day23().run)

# vim:expandtab:sw=4:ts=4
