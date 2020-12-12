#!/bin/pypy3

import aoc
from typing import List

SAMPLE = ["""\
F10
N3
F7
R90
F11
"""]


class Day12(aoc.Challenge):
  """Ship coordinates and movement.

  The x, y position can be mapped to the complex plane[1] using a complex number.
  Python got built-in language support for comlex numbers which is handy.

  Also recall polar coordinates[2]. Multiplying a complex number by a complex number
  can affect it's angle. (1+2j) * -1 = (-1-2j) -- which is a 180 degree rotation.
  Multiplying by a real number does not affect the angle. Multiplying by an imaginary
  number affects only the angle:
  z * 1 == z == rot(360deg). z * -1 == rot(180). z * (1j) == rot(90).
  (1+2j) * 1j == (-2+1j) == rot(90).

  Kudos to github.com/mstksg aka jle for the refresher.

  Also recall, (n+360)deg == (n)deg. R(n) == L(-n) == L(360-n).
  In order to keep 0 <= bearing < 360, bearing = (bearing + n) % 360.

  [1] https://en.wikipedia.org/wiki/Complex_plane
  [2] https://en.wikipedia.org/wiki/Polar_coordinate_system
  """

  # Parse the input at load time. Split into char + num.
  TRANSFORM = lambda _, l: (l[0], int(l[1:]))
  DEBUG = False

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=25),
    aoc.TestCase(inputs=SAMPLE[0], part=2, want=286),
  )

  # Modifier to map EWNS or degrees to a complex rotation.
  MOD = {
    'E': 1, 'N': 1j, 'W': -1, 'S': -1j,
      0: 1,  90: 1j, 180: -1, 270: -1j,
  }

  def manhattan_dist(self, z: complex) -> int:
    return int(abs(z.real) + abs(z.imag))

  def part1(self, lines: List[str]) -> int:
    """Track the ship's position."""
    ship = 0 + 0j
    heading = 0
    for instruction, num in lines:
      if instruction in 'NEWS':
        ship += num * self.MOD[instruction]
      if instruction in 'LR':
        if instruction == 'R':
          num = 360 - num
        heading = (heading + num) % 360
      if instruction == 'F':
        ship += num * self.MOD[heading]
    return self.manhattan_dist(ship)

  def part2(self, lines: List[str]) -> int:
    """Track the ship's position - with a magical waypoint."""
    ship = 0 + 0j
    waypoint = 10 + 1j
    for instruction, num in lines:
      if instruction in 'NEWS':
        waypoint += num * self.MOD[instruction]
      if instruction in 'LR':
        if instruction == 'R':
          num = 360 - num
        for _ in range(0, num, 90):
          waypoint *= 1j
      if instruction == 'F':
        ship += num * waypoint
    return self.manhattan_dist(ship)


if __name__ == '__main__':
  Day12().run()

# vim:ts=2:sw=2:expandtab
