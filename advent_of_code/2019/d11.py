#!/bin/python
"""Advent of Code, Day 11: Space Police."""
import collections
import intcode
from lib import aoc


def solve(data: str, part: int) -> int | str:
    """Draw a call sign on the ship."""
    computer = intcode.Computer(data)
    position = complex()
    direction = complex(0, -1)
    painted: set[complex] = set()
    panels: dict[complex, int] = collections.defaultdict(int)
    panels[position] = 0 if part == 1 else 1

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
    if part == 1:
        return len(painted)
    white = {pos for pos, color in panels.items() if color}
    return aoc.OCR.from_point_set(white).as_string()


TESTS = list[tuple[int, int, int]]()
