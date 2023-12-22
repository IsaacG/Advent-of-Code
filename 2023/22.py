#!/bin/python
"""Advent of Code, Day 22: Sand Slabs."""

import collections
from lib import aoc

SAMPLE = """\
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""

InputType = dict[int, list[int]]


class Day22(aoc.Challenge):
    """Day 22: Sand Slabs."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=5),
        aoc.TestCase(inputs=SAMPLE, part=2, want=7),
    ]
    PARAMETERIZED_INPUTS = [False, True]

    def solver(self, parsed_input: InputType, param: bool) -> int:
        # Brick ID to coordinates.
        bricks = parsed_input

        # Track which bricks exist by x-y column for faster lookups.
        brick_by_x_y = collections.defaultdict(list)
        for num, (start_x, start_y, start_z, end_x, end_y, _) in bricks.items():
            for x_col in range(start_x, end_x + 1):
                for y_col in range(start_y, end_y + 1):
                    brick_by_x_y[x_col, y_col].append(num)

        # Track which other bricks a given brick is supporting.
        holding: dict[int, list[int]] = {brick: [] for brick in bricks}
        held_by: dict[int, list[int]] = {brick: [] for brick in bricks}
        # Drop bricks until all bricks have settled.
        settled: set[int] = set()
        # Sort bricks by lowest bottom, i.e. most likely to settle next.
        inflight = sorted(bricks, key=lambda x: bricks[x][2])

        while inflight:
            for brick in inflight:
                start_x, start_y, start_z, end_x, end_y, _ = bricks[brick]
                # Locate other bricks in the same column(s) as this brick but lower down.
                potential_tops = {
                    other for (x, y), others in brick_by_x_y.items()
                    if start_x <= x <= end_x and start_y <= y <= end_y for other in others
                }
                # Check if this brick is resting on top of any other bricks.
                landed = {other for other in potential_tops & settled if bricks[other][5] + 1 == start_z}
                if bricks[brick][2] == 1 or landed:
                    inflight.remove(brick)
                    settled.add(brick)
                    for other in landed:
                        holding[other].append(brick)
                    held_by[brick].extend(landed)
                else:
                    new_bottom = 1 + max(
                        (bricks[other][5] for other in potential_tops if bricks[other][5] < start_z),
                        default=0,
                    )
                    if new_bottom < start_z:
                        dist = start_z - new_bottom
                        bricks[brick][2] -= dist
                        bricks[brick][5] -= dist
                        break

        # Part 1: count the bricks which can safely be removed.
        # If a brick is not a sole support of any other brick, it can be removed.
        if not param:
            return sum(
                all(held_by[supported] != [brick] for supported in holding[brick])
                for brick in bricks
            )

        # Part 2: count how many bricks can be dropped by removing a support.
        count = 0
        original = holding
        # Try removing each brick. Count the chain reaction disintegration.
        for brick in bricks:
            holding = original.copy()
            # Track and process bricks which had a support removed.
            # Chain remove bricks which do not have any other supports.
            lost_support = set(holding.pop(brick))
            while lost_support:
                brick = lost_support.pop()
                for other in held_by[brick]:
                    if brick in holding.get(other, []):
                        # This brick has an alternate support.
                        break
                else:
                    # This brick does not have an alternate support. Disintegrate.
                    count += 1
                    lost_support.update(holding.pop(brick))

        return count

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        data = aoc.parse_re_findall_int(aoc.RE_INT).parse(puzzle_input)
        bricks = dict(enumerate(data))
        return bricks

# vim:expandtab:sw=4:ts=4
