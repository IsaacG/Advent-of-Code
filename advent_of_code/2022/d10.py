#!/bin/python
"""Advent of Code, Day 10: Cathode-Ray Tube.

Emulate a simple CPU and program with a cycle counter.
"""

from lib import aoc

def run_program(lines: list[tuple[int | str, ...]]) -> list[int]:
    """Run the program and store the `X` register value for each cycle."""
    regx = 1
    regx_values = []
    size = {"addx": 2, "noop": 1}
    for parts in lines:
        for _ in range(size[str(parts[0])]):
            regx_values.append(regx)
        if parts[0] == "addx":
            regx += int(parts[1])
    return regx_values


def solve(data: list[tuple[int | str, ...]], part: int) -> int:
    """Run a program."""
    regx_values = run_program(data)
    if part == 1:
        return sum(
            regx_values[cycle - 1] * cycle
            for cycle in range(20, 240, 40)
        )

    # Return the word drawn on the screen.
    pixels = []
    for cycle, regx in enumerate(regx_values):
        horizontal_position = cycle % 40
        pixels.append(abs(horizontal_position - regx) <= 1)

    # Split the output into 6 rows of 40 pixels each.
    rows = [pixels[i*40:(i+1)*40] for i in range(6)]
    return aoc.OCR(rows).as_string()


SAMPLE = """\
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""
TESTS = [(1, SAMPLE, 13140)]
