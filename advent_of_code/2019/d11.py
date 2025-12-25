#!/bin/python
"""Advent of Code, Day 11: Space Police."""

import collections

import intcode
from lib import aoc


class Day11(aoc.Challenge):
    """Day 11: Space Police."""

    TESTS = [
        aoc.TestCase(inputs="", part=1, want=aoc.TEST_SKIP),
        aoc.TestCase(inputs="", part=2, want=aoc.TEST_SKIP),
    ]

    def solver(self, program: str, part_one: bool) -> int | str:
        computer = intcode.Computer(program)
        position = complex()
        direction = complex(0, -1)
        painted: set[complex] = set()
        panels: dict[complex, int] = collections.defaultdict(int)
        panels[position] = 0 if part_one else 1

        computer.input.append(panels[position])
        computer.run()
        while not computer.stopped:
            painted.add(position)
            panels[position] = computer.output.popleft()
            rotation = computer.output.popleft()
            direction *= 1j if rotation else -1j
            position += direction
            computer.input.append(panels[position])
            computer.run()
        if part_one:
            return len(painted)
        white = {pos for pos, color in panels.items() if color}
        return aoc.OCR.from_point_set(white).as_string()

# vim:expandtab:sw=4:ts=4
