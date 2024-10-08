#!/usr/bin/env python
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

from lib import aoc

SAMPLE = ["""\
F10
N3
F7
R90
F11
"""]


class Day12(aoc.Challenge):
  """Day 12."""

  DEBUG = False
  INPUT_PARSER = aoc.ParseOneWordPerLine(lambda l: (l[0], int(l[1:])))

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=25),
    aoc.TestCase(inputs=SAMPLE[0], part=2, want=286),
  )

  # Modifier to map EWNS or degrees to a complex rotation.
  MOD = aoc.COMPASS_DIRECTIONS

  def manhattan_dist(self, num: complex) -> int:
    """Manhattan distance of a complex number."""
    return int(abs(num.real) + abs(num.imag))

  def solve(self, puzzle_input: list[tuple[str, int]], waypoint: complex, part: int) -> int:
    """Track the ship's position - with a magical waypoint."""
    ship = 0 + 0j
    for instruction, num in puzzle_input:
      if instruction in 'NEWS':
        change = num * self.MOD[instruction]
        if part == 1:
          ship += change
        else:
          waypoint += change
      if instruction in 'LR':
        if instruction == 'R':
          num = 360 - num
        num //= 90
        waypoint *= 1j ** num
      if instruction == 'F':
        ship += num * waypoint
    return self.manhattan_dist(ship)

  def part1(self, puzzle_input: list[tuple[str, int]]) -> int:
    return self.solve(puzzle_input, 1, 1)

  def part2(self, puzzle_input: list[tuple[str, int]]) -> int:
    return self.solve(puzzle_input, (10 + 1j), 2)


# vim:ts=2:sw=2:expandtab
