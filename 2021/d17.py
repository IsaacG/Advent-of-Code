#!/bin/python
"""Advent of Code: Day 17."""

from lib import aoc

SAMPLE = "target area: x=20..30, y=-10..-5"
InputType = list[int]


class Day17(aoc.Challenge):
    """Determine what initial velocities will allow the probe to hit the target."""

    TESTS = (
        aoc.TestCase(inputs=SAMPLE, part=1, want=45),
        aoc.TestCase(inputs=SAMPLE, part=2, want=112),
    )
    INPUT_PARSER = aoc.parse_re_group_int(r"target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)")

    def part1(self, puzzle_input: InputType) -> int:
        """Compute the highest height that can be reached while hitting the target."""
        y_max = max(y for x, y in self.find_velocities(*puzzle_input[0]))
        # At an upwards speed of y and a constant deceleration of 1,
        # the height after each step is [y, y + (y-1), y + (y-1) + (y-2), ...]
        # until y-velocity = 0. The distance travelled is sum(1..y). This is also
        # y * (y + 1) / 2
        return int(y_max * (y_max + 1) // 2)

    def part2(self, puzzle_input: InputType) -> int:
        """Compute how many velocities would work to hit the target."""
        return len(self.find_velocities(*puzzle_input[0]))

    @staticmethod
    def find_velocities(x0, x1, y0, y1) -> list[tuple[int, int]]:
        """Return velocities that can hit the target."""
        velocities = []
        assert y0 < 0, "The target must be negative."

        # The x-velocity decreases by 1 every step. In order to hit the target,
        # sum(x-velocities from v0_x to 0) >= x0.
        min_x = 0
        while (min_x * (min_x + 1)) // 2 < x0:
            min_x += 1

        # Try all intial x-velocities from min_x to target's x1.
        # Anything lower than min_x will never hit the target.
        # Anything over x1 will overshoot the target on the first step.
        for x in range(min_x, x1 + 1):
            # Try all initial y-velocities.
            # Anything lower than y0 will immediately drop below the target.
            # For high y values, by the time they arch up and return to the y=0 line,
            # they will have y-velocity == -(initial y-velocity) due to constant
            # acceleration. The same logic about not overshooting immediately as
            # soon as it passes below y=0 applies to this bound.
            for y in range(y0, -y0 + 1):
                v_x, v_y = x, y
                pos_x, pos_y = 0, 0
                # Track the flight until the projectile passes the target's far edge.
                while pos_x <= x1 and pos_y >= y0:
                    # Update the position.
                    pos_x += v_x
                    pos_y += v_y
                    # Apply drag, slowing down the x-velocity.
                    if v_x > 0:
                        v_x -= 1
                    # Apply gravity, reducing the y-velocity.
                    v_y -= 1

                    # If we hit the target, record the max height and stop.
                    if x0 <= pos_x <= x1 and y0 <= pos_y <= y1:
                        velocities.append((x, y))
                        break

        return velocities
