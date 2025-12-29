#!/usr/bin/env python
"""Day 10: Monitoring Station

Determine the best place for an astroid station and figure out which
astroid is #200 to get evaporated by laser beam.
"""

import collections
import math
import data as input_data


def compute_angle(c: complex) -> complex:
    """Return the angle given by a complex number."""
    return c / math.gcd(int(c.real), int(c.imag))


def count_by_angle(locations: set[complex]) -> dict[complex, int]:
    """Count the unique angles at which astroids can be seen for all astroids."""
    return {
        location: len(set(
            compute_angle(location - x)
            for x in locations
            if x != location
        ))
        for location in locations
    }


def solve(data: set[complex], part: int) -> int:
    """Simulation blasting astroids with a laser and find which astroid is #200."""
    if part == 1:
        # Count the number of angles at which other astroids are seen from any given astroid.
        return max(count_by_angle(data).values())

    # Figure out which astroid is the laser base.
    counts = count_by_angle(data)
    base = [loc for loc, count in counts.items() if count == max(counts.values())][0]

    angle_map = collections.defaultdict(list)
    for location in data:
        if location == base:
            continue
        # Rotate and flip the map so `atan` aligns with the laser's operating arc.
        rl = (location - base) * 1j
        rl = -1 * rl.real + 1j * rl.imag
        angle_map[math.atan2(int(rl.imag), int(rl.real))].append(location)

    # Sort the astroids found along each angle.
    for a in angle_map.values():
        a.sort(key=abs)

    # Count off 200 laser blasts.
    shot = 0
    while angle_map:
        angles = sorted(angle_map.keys(), reverse=True)
        for angle in angles:
            shot += 1
            astroid = angle_map[angle].pop(0)
            if shot == 200:
                return int(100 * astroid.real + astroid.imag)
    raise ValueError


def input_parser(data: str) -> set[complex]:
    """Convert the input lines to a set of astroid coordinates."""
    locations = set()
    for row, line in enumerate(data.split('\n')):
        for col, val in enumerate(line):
            if val == '#':
                locations.add(col + (row * 1j))
    return locations


SAMPLE = input_data.D10
TESTS = [
    (1, SAMPLE[0], 8),
    (1, SAMPLE[1], 33),
    (1, SAMPLE[2], 35),
    (1, SAMPLE[3], 41),
    (1, SAMPLE[4], 210),
    (2, SAMPLE[4], 802),
]
