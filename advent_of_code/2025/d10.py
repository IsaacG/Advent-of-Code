#!/bin/python
"""Advent of Code, Day 10: Factory."""

import itertools

import z3  # type: ignore

from lib import aoc

SAMPLE = """\
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""

InputType = list[tuple[int, list[int], list[list[int]], list[int]]]


class Day10(aoc.Challenge):
    """Day 10: Factory."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=7),
        aoc.TestCase(part=2, inputs=SAMPLE, want=33),
    ]

    def part1(self, puzzle_input: InputType) -> int:
        """Return the min number of buttons that need to be pressed to light up the needed lights."""

        def get_steps(target: int, buttons: list[int]) -> int:
            """Return the steps for one light. Try increasing combinations of buttons."""
            for steps in range(0, len(buttons)):
                for combo in itertools.combinations(buttons, steps):
                    result = 0
                    for button in combo:
                        result ^= button
                    if result == target:
                        return steps
            raise RuntimeError("No solution found.")

        return sum(get_steps(target, buttons) for target, buttons, *_ in puzzle_input)

    def part2(self, puzzle_input: InputType) -> int:
        """Return the min number of buttons that need to be pressed to get the target joltage."""
        total = 0
        for *_, buttons, joltage in puzzle_input:
            button_pushes = [z3.Int(f"b{idx}") for idx in range(len(buttons))]
            optimizer = z3.Optimize()
            # Buttons cannot be pushed less than 0 times.
            for b in button_pushes:
                optimizer.add(b >= 0)
            # For each target jolt, the sum pushes of button affecting that meter must match the target jolt.
            for jolt_idx, jolts in enumerate(joltage):
                total_pushes = z3.Sum([pushes for button, pushes in zip(buttons, button_pushes) if jolt_idx in button])
                optimizer.add(total_pushes == jolts)
            # The answer is the sum button pushes. Minimize that value.
            ans = z3.Int("ans")
            optimizer.add(ans == z3.Sum(button_pushes))
            optimizer.minimize(ans)
            assert optimizer.check() == z3.sat
            total += optimizer.model()[ans].as_long()  # pylint: disable=E1101

        return total

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        lines = []
        for line in puzzle_input.splitlines():
            lights_, *buttons_, joltage_ = [i[1:-1] for i in line.split()]
            # Convert the lights to an int, each light being a bit.
            lights = 0
            for i in lights_[::-1]:
                lights <<= 1
                if i == "#":
                    lights |= 1
            buttons = [[int(i) for i in b.split(",")] for b in buttons_]
            # Buttons to bits for p1. This lets us use bitwise XOR to combine buttons.
            bits = [sum(1 << i for i in b) for b in buttons]
            joltage = [int(i) for i in joltage_.split(",")]
            lines.append((lights, bits, buttons, joltage))
        return lines

# vim:expandtab:sw=4:ts=4
