#!/usr/bin/env python
"""Day 10: Monitoring Station

Determine the best place for an astroid station and figure out which
astroid is #200 to get evaporated by laser beam.
"""

import collections
import math
import typer
from typing import Dict, Set

import data
from lib import aoc

SAMPLE = data.D10


class Day10(aoc.Challenge):

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=8),
    aoc.TestCase(inputs=SAMPLE[1], part=1, want=33),
    aoc.TestCase(inputs=SAMPLE[2], part=1, want=35),
    aoc.TestCase(inputs=SAMPLE[3], part=1, want=41),
    aoc.TestCase(inputs=SAMPLE[4], part=1, want=210),
    aoc.TestCase(inputs=SAMPLE[4], part=2, want=802),
  )

  def count_by_angle(self, locations: Set[complex]) -> Dict[complex, int]:
    """Count the unique angles at which astroids can be seen for all astroids."""
    return {
      location: len(set(
        self.angle(location - x)
        for x in locations
        if x != location
      ))
      for location in locations
    }

  def part1(self, locations: Set[complex]) -> int:
    """Count the number of angles at which other astroids are seen from any given astroid."""
    return max(self.count_by_angle(locations).values())

  def part2(self, locations: Set[complex]) -> int:
    """Simulation blasting astroids with a laser and find which astroid is #200."""
    # Figure out which astroid is the laser base.
    counts = self.count_by_angle(locations)
    base = [loc for loc, count in counts.items() if count == max(counts.values())][0]

    angle_map = collections.defaultdict(list)
    for location in locations:
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

  def parse_input(self, puzzle_input: str) -> Set[complex]:
    """Convert the input lines to a set of astroid coordinates."""
    locations = set()
    for row, line in enumerate(puzzle_input.split('\n')):
      for col, val in enumerate(line):
        if val == '#':
          locations.add(col + (row * 1j))
    return locations


if __name__ == '__main__':
  typer.run(Day10().run)

# vim:ts=2:sw=2:expandtab
