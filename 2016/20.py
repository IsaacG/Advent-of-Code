#!/bin/python
"""Advent of Code, Day 20: Firewall Rules. Find valid IPs between blacklisted ranges."""

from lib import aoc

SAMPLE = "5-8\n0-2\n4-7"
LineType = tuple[int, int]
InputType = list[LineType]


class Day20(aoc.Challenge):
    """Day 20: Firewall Rules."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=3),
        aoc.TestCase(inputs=SAMPLE, part=2, want=2),
    ]

    def solver(self, parsed_input: InputType, param: bool) -> int:
        """Find valid IPs between blacklisted ranges."""
        # Set the upper limit.
        if self.testing:
            parsed_input.append((10, 10))
        else:
            parsed_input.append((4294967296, 4294967296))

        cur = 0
        allowed = 0
        for low, high in parsed_input:
            if low <= cur <= high:
                cur = high + 1
            elif cur < low:
                # Part 1: return the first allowed IP.
                if not param:
                    return cur
                # Part 2: count valid IPS.
                allowed += low - cur
                cur = high + 1
        return allowed

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return sorted(tuple(int(i) for i in line.split("-")) for line in puzzle_input.splitlines())
