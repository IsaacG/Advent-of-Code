#!/bin/python
"""Advent of Code, Day 15: Beacon Exclusion Zone. Locate a beacon based on knowing where it is not."""

import re

import typer
from lib import aoc

SAMPLE = """\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

InputType = list[tuple[int, int, int]]


class Day15(aoc.Challenge):
    """Day 15: Beacon Exclusion Zone."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=26),
        aoc.TestCase(inputs=SAMPLE, part=2, want=56000011),
    ]

    def part1(self, parsed_input: InputType) -> int:
        """Return the number of coordinates on a given row which cannot contain the beacon.

        For each sensor, find the x-range the sensor covers on the given row.
        """
        row = 10 if self.testing else 2000000

        x_positions = set()
        for sensor_x, sensor_y, sensor_range in parsed_input:
            y_dist = abs(row - sensor_y)
            if y_dist > sensor_range:
                continue
            covered_x_range_start = sensor_x - (sensor_range - y_dist)
            covered_x_range_end = sensor_x + (sensor_range - y_dist)
            x_positions.update(range(covered_x_range_start, covered_x_range_end))
        return len(x_positions)

    def part2(self, parsed_input: InputType) -> int:
        """Locate the distress beacon.

        For each row, start a cursor at the left.
        Iterate through sensors in order, and move the cursor to just past the right
        edge of the sensor (if the cursor is within sensor range).
        When all sensors were applied, if the cursor is within the boundaries of the board,
        that is where the distress beacon is located.
        """
        dims = 20 if self.testing else 4000000
        sensor_tuples = parsed_input
        # Sort sensors, left to right.
        sensor_tuples.sort()

        # Test each row until we find the beacon.
        for candidate_y in range(dims + 1):
            candidate_x = 0
            # For each sensor, move the cursor to just past the right end, if it is in sensor range.
            for sensor_x, sensor_y, sensor_range in sensor_tuples:
                y_dist = abs(sensor_y - candidate_y)
                point_dist = abs(sensor_x - candidate_x) + y_dist
                if point_dist <= sensor_range:
                    candidate_x = sensor_x + sensor_range - y_dist + 1
            if candidate_x <= dims:
                self.debug(f"Solved!!! {candidate_x, candidate_y}")
                return candidate_x * 4000000 + candidate_y

    def line_parser(self, line: str) -> tuple[int, int, int]:
        """Parse a line into a tuple of sensor's coordinates and range."""
        a, b, c, d = (int(i) for i in aoc.RE_INT.findall(line))
        return a, b, abs(a - c) + abs(b - d)


if __name__ == "__main__":
    typer.run(Day15().run)

# vim:expandtab:sw=4:ts=4
