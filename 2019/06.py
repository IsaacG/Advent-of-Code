#!/usr/bin/env pypy
"""2019 Day 6: Universal Orbit Map.

Count orbits and steps from one orbit to another.
"""

import collections
import itertools
import typer
from typing import List

from lib import aoc

SAMPLE = [
  'COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L\n',
  'COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L\nK)YOU\nI)SAN',
]


class Day06(aoc.Challenge):

  TRANSFORM = lambda _, s: s.split(')')

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=42),
    aoc.TestCase(inputs=SAMPLE[1], part=2, want=4),
  )

  def part1(self, lines: List[List[str]]) -> int:
    """Count total orbits."""
    # Build graph edges from COM outwards.
    orbits = collections.defaultdict(set)
    for a, b in lines:
      orbits[a].add(b)

    # Walk the tree forwards, level by level.
    # For each level, for all items, count the depths.
    depth = 0
    answer = 0
    todo = ['COM']
    while todo:
      answer += depth * len(todo)
      depth += 1
      # Expand the list to the next level.
      todo = list(itertools.chain.from_iterable(orbits[i] for i in todo))

    return answer

  def part2(self, lines: List[List[str]]) -> int:
    """Count steps from YOU to SANta."""
    # Build a forward and reverse map between orbits.
    forward = collections.defaultdict(set)
    reverse = dict()
    for a, b in lines:
      forward[a].add(b)
      reverse[b] = a

    cache = {}

    def contains(node) -> bool:
      """Check if a node contains SANta. Use dynamic programming."""
      if node not in cache:
        if not forward[node]:
          cache[node] = False
        elif 'SAN' in forward[node]:
          cache[node] = True
        else:
          cache[node] = any(contains(i) for i in forward[node])
      return cache[node]

    # Walk backwards from YOU to a node containing SANta.
    steps = 0
    cur = reverse['YOU']
    while not contains(cur):
      steps += 1
      cur = reverse[cur]

    # Walk backwards from SANta to the common node.
    common, cur = cur, reverse['SAN']
    while cur != common:
      steps += 1
      cur = reverse[cur]

    return steps


if __name__ == '__main__':
  typer.run(Day06().run)

# vim:ts=2:sw=2:expandtab