#!/bin/python
"""Advent of Code, Day 10: Cathode-Ray Tube.

Emulate a simple CPU and program with a cycle counter.
"""

from lib import aoc

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

InputType = list[tuple[int | str, ...]]


class Day10(aoc.Challenge):
    """Day 10: Cathode-Ray Tube."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=13140),
        aoc.TestCase(inputs=SAMPLE, part=2, want=aoc.TEST_SKIP),
    ]
    INPUT_PARSER = aoc.parse_multi_mixed_per_line

    def run_program(self, lines: InputType) -> list[int]:
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

    def part1(self, parsed_input: InputType) -> int:
        """Return the X value at various cycles."""
        regx_values = self.run_program(parsed_input)
        out = 0
        for cycle in range(20, 240, 40):
            out += regx_values[cycle - 1] * cycle
        return out

    def part2(self, parsed_input: InputType) -> str:
        """Return the word drawn on the screen."""
        regx_values = self.run_program(parsed_input)

        pixels = []
        for cycle, regx in enumerate(regx_values):
            horizontal_position = cycle % 40
            pixels.append(abs(horizontal_position - regx) <= 1)

        # Split the output into 6 rows of 40 pixels each.
        rows = [pixels[i*40:(i+1)*40] for i in range(6)]
        return aoc.OCR(rows).as_string()
