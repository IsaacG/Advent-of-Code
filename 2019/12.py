#!/usr/bin/env python
"""Day 12: The N-Body Problem.

Calculate the positions and velocities of N-bodies floating in space.
Determine how long a complete cycle takes.
"""

import itertools
import math
import typer
from typing import List, Tuple

from lib import aoc


SAMPLE = ["""\
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
""", """
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
""", """
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
"""]


class Moon:
  """Data wrapper around a "body"."""

  def __init__(self, pos):
    self.pos = list(pos)
    self.len = len(self.pos)
    self.vel = [0] * self.len

  def __str__(self):
    return (
      f'pos=<x={self.pos[0]:3d}, y={self.pos[1]:3d}, z={self.pos[2]:3d}>, '
      f'vel=<x={self.vel[0]:3d}, y={self.vel[1]:3d}, z={self.vel[2]:3d}>'
    )

  def apply_gravity(self, other):
    """Update the velocity of `self` based on the location of `other`."""
    for i in range(self.len):
      if self.pos[i] < other.pos[i]:
        v = 1
      elif self.pos[i] > other.pos[i]:
        v = -1
      else:
        v = 0
      self.vel[i] += v

  def apply_velocity(self):
    """Update position of `self` based on velocity."""
    for i in range(self.len):
      self.pos[i] += self.vel[i]

  def energy(self):
    """Total energy. Potential E * kinetic E."""
    return sum(abs(x) for x in self.pos) * sum(abs(x) for x in self.vel)


class Day12(aoc.Challenge):

  # Return a tuple of ints for each line.
  TRANSFORM = lambda _, s: tuple(int(p.split('=')[-1]) for p in s[1:-1].split(', '))

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=1940),
    aoc.TestCase(inputs=SAMPLE[1], part=2, want=2772),
    aoc.TestCase(inputs=SAMPLE[2], part=2, want=4686774924),
  )

  def part1(self, positions: List[Tuple[int]]) -> int:
    """Run the similation for N cycles and return total energy at the end."""
    moons = [Moon(position) for position in positions]
    lim = 100 if self.testing else 1000
    for step in range(lim):
      for a, b in itertools.permutations(moons, 2):
        a.apply_gravity(b)
      for a in moons:
        a.apply_velocity()
    return sum(m.energy() for m in moons)

  def part2(self, positions: List[Tuple[int]]) -> int:
    """Calculate how many cycles before looping back to the begining."""

    def fp(moons):
      """Fingerprint function used to convert the moons to a suitable `seen` object."""
      vals = []
      for m in moons:
        vals.extend(m.pos + m.vel)
      return tuple(vals)

    cycles = []
    # For each axis, count how many cycles until a repeat.
    for axis in range(len(positions[0])):
      seen = set()
      steps = 0
      moons = [Moon(position[axis:axis + 1]) for position in positions]
      fingerprint = fp(moons)
      perms = list(itertools.permutations(moons, 2))

      while fingerprint not in seen:
        seen.add(fingerprint)
        steps += 1
        for a, b in perms:
          a.apply_gravity(b)
        for a in moons:
          a.apply_velocity()
        fingerprint = fp(moons)

      cycles.append(steps)

    return math.lcm(*cycles)


if __name__ == '__main__':
  typer.run(Day12().run)

# vim:ts=2:sw=2:expandtab
