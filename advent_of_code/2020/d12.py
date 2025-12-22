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

PARSER = lambda x: [(line[0], int(line[1:])) for line in x.splitlines()]
# Modifier to map EWNS or degrees to a complex rotation.
MOD = aoc.COMPASS_DIRECTIONS


def solve(data: list[tuple[str, int]], part: int) -> int:
    """Track the ship's position - with a magical waypoint."""
    ship = 0 + 0j
    waypoint = complex(1, 0) if part == 1 else complex(10, 1)
    for instruction, num in data:
        if instruction in 'NEWS':
            change = num * MOD[instruction]
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
    return int(abs(ship.real) + abs(ship.imag))


SAMPLE = "F10 N3 F7 R90 F11".replace(" ", "\n")
TESTS = [(1, SAMPLE, 25), (2, SAMPLE, 286)]
