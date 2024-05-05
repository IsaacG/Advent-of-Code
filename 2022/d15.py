#!/bin/python
"""Advent of Code, Day 15: Beacon Exclusion Zone. Locate a beacon based on knowing where it is not."""

import itertools

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


def flatten_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Flatten a list of ranges into a set of non-overlapping ranges."""
    out = []
    ranges = sorted(ranges)
    start_a, end_a = ranges[0]
    for start_b, end_b in ranges[1:]:
        if end_b < start_a:
            # Distinct ranges, range b occurs before range a.
            raise RuntimeError("Ranges not sorted!")
        if start_b > end_a:
            # Distinct ranges, range b occurs after range a.
            out.append((start_a, end_a))
            start_a, end_a = start_b, end_b
        else:
            # Ranges overlap. Combine ranges.
            start_a = min(start_a, start_b)
            end_a = max(end_a, end_b)
    out.append((start_a, end_a))
    return out


class Day15(aoc.Challenge):
    """Day 15: Beacon Exclusion Zone."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=26),
        aoc.TestCase(inputs=SAMPLE, part=2, want=aoc.TEST_SKIP),
        # aoc.TestCase(inputs=SAMPLE, part=2, want=56000011),
    ]

    def part1(self, parsed_input: InputType) -> int:
        """Return the number of coordinates on a given row which cannot contain the beacon.

        Collect a bunch of intervals for each sensor then aggregate them at the end into
        combined ranges. Return sum size of ranges.
        """
        row = 10 if self.testing else 2000000

        ranges = []
        for sensor_x, sensor_y, sensor_range in parsed_input:
            y_dist = abs(row - sensor_y)
            if y_dist > sensor_range:
                continue
            start = sensor_x - (sensor_range - y_dist)
            end = sensor_x + (sensor_range - y_dist)
            ranges.append((start, end))

        covered_points = sum(end - start for start, end in flatten_ranges(ranges))
        return covered_points

    def part2_line_intersections(self, sensors: InputType):
        """Use line intersections to locate the distress beacon.

        * For each (sorted) sensor combination, check if their distance is one more
          than their combined range, i.e. they have space for exactly one unit of space
          between them.
        * Based on the relative `y` positions, this is either a 45 degree line
          up-and-right or down-and-right. The slope is either `+1` or `-1`.
          These lines can be stored as `y = mx + b` or just `b`
          if using two containers for the different slopes.
        * For each combination of `m = +1` and `m = -1` lines, compute the intersection.
          Filter out intersections outside the bounding box, `(0, 4,000,000) x (0, 4,000,000)`
          (optional if there are multiple lines).
        * The intersection gives the coordinates of the distress beacon.
        """

        x_intersects: dict[int, set[int]] = {+1: set(), -1: set()}
        # Find sensor pairs with borders 2 units apart.
        for pairs in itertools.combinations(sensors, 2):
            sensor_a_x, sensor_a_y, sensor_a_range = pairs[0]
            sensor_b_x, sensor_b_y, sensor_b_range = pairs[1]
            sensor_dist = abs(sensor_a_x - sensor_b_x) + abs(sensor_a_y - sensor_b_y)
            # Check the distance between sensor range edges.
            if sensor_dist != sensor_a_range + sensor_b_range + 2:
                continue

            # Compute and store the slope-intersect values.
            slope = +1 if sensor_a_y > sensor_b_y else -1
            b = sensor_a_x + sensor_a_range + 1 + (-slope * sensor_a_y)
            x_intersects[slope].add(b)

        self.debug(x_intersects)

        # For all intersecting lines, compute the intersection point.
        candidate_points = set()
        for ur, dr in itertools.product(x_intersects[1], x_intersects[-1]):
            diff = (dr - ur)
            if diff % 2 == 1:
                continue
            x_intersect = (dr + ur) // 2
            y_intersect = diff // 2
            # Ignore points out of bounds.
            if not all(0 <= intersect <= 4000000 for intersect in (x_intersect, y_intersect)):
                continue
            candidate_points.add((x_intersect, y_intersect))

        # Return the answer.
        if len(candidate_points) != 1:
            raise RuntimeError("Want one point, found {len(candidate_points)}")
        x_intersect, y_intersect = candidate_points.pop()
        return x_intersect * 4000000 + y_intersect

    def ranges(self, sensors: InputType) -> tuple[tuple[int, int], tuple[int, int]]:
        """Return the bounding box drawn by sensors with exactly one unit of uncovered space between them.

        Used to half the runtime of the line sweep approach.
        """
        x_edges = set()
        y_edges = set()
        # Find sensor pairs with borders 2 units apart.
        for sensor_a_x, sensor_a_y, sensor_a_range in sensors:
            for sensor_b_x, sensor_b_y, sensor_b_range in sensors:
                sensor_dist = abs(sensor_a_x - sensor_b_x) + abs(sensor_a_y - sensor_b_y)
                if sensor_dist == sensor_a_range + sensor_b_range + 2:
                    x_edges.add(sensor_a_x)
                    y_edges.add(sensor_a_y)

        x_start, x_end = min(x_edges), max(x_edges)
        y_start, y_end = min(y_edges), max(y_edges)
        return (x_start, x_end + 1), (y_start, y_end + 1)

    def part2_linesweep(self, parsed_input: InputType) -> int:
        """Locate the distress beacon.

        For each row, start a cursor at the left.
        Iterate through sensors in order, and move the cursor to just past the right
        edge of the sensor (if the cursor is within sensor range).
        When all sensors were applied, if the cursor is within the boundaries of the board,
        that is where the distress beacon is located.
        """
        sensors = parsed_input

        x_range, y_range = self.ranges(sensors)
        # Test each row until we find the beacon.
        for candidate_y in range(*y_range):
            candidate_x = x_range[0]
            # For each sensor, move the cursor to just past the right end, if it is in sensor range.
            for sensor_x, sensor_y, sensor_range in sensors:
                y_dist = abs(sensor_y - candidate_y)
                point_dist = abs(sensor_x - candidate_x) + y_dist
                if point_dist <= sensor_range:
                    candidate_x = sensor_x + sensor_range - y_dist + 1
            if candidate_x < x_range[1]:
                self.debug(f"Solved! {candidate_x, candidate_y}")
                return candidate_x * 4000000 + candidate_y
        raise RuntimeError("Beacon was not found.")

    def part2(self, parsed_input: InputType) -> int:
        """Locate the distress beacon."""
        return self.part2_line_intersections(parsed_input)
        # return self.part2_linesweep(parsed_input)

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse a line into a tuple of sensor's coordinates and range."""
        data = []
        for line in puzzle_input.splitlines():
            # Sensor (x, y) and beacon(x, y)
            a, b, c, d = (int(i) for i in aoc.RE_INT.findall(line))
            # Sensor (x, y) and sensor range (distance to beacon).
            data.append((a, b, abs(a - c) + abs(b - d)))
        # Sort sensors, left to right.
        data.sort()
        return data
