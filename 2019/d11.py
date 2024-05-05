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
    INPUT_PARSER = aoc.parse_one_str
    PARAMETERIZED_INPUTS = [0, 1]

    def solver(self, program: str, initial: int) -> int | str:
        q_in, q_out = collections.deque(), collections.deque()
        computer = intcode.Computer(program, input_q=q_in, output_q=q_out, debug=self.DEBUG)
        position = complex()
        direction = complex(0, -1)
        painted: set[complex] = set()
        panels: dict[complex, int] = collections.defaultdict(int)
        panels[position] = initial

        q_in.append(panels[position])
        computer.run()
        while not computer.stopped:
            painted.add(position)
            panels[position] = q_out.popleft()
            rotation = q_out.popleft()
            direction *= 1j if rotation else -1j
            position += direction
            computer.input.append(panels[position])
            computer.run()
        if initial == 0:
            return len(painted)
        white = {pos for pos, color in panels.items() if color}
        return aoc.OCR.from_point_set(white).as_string()

# vim:expandtab:sw=4:ts=4
