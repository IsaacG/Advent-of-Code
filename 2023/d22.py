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
        footprints = {
            brick: [
                (x_col, y_col)
                for x_col in range(start_x, end_x + 1)
                for y_col in range(start_y, end_y + 1)
            ] for brick, (start_x, start_y, start_z, end_x, end_y, _) in bricks.items()
        }
        brick_by_x_y = collections.defaultdict(set)
        for brick, footprint in footprints.items():
            for coord in footprint:
                brick_by_x_y[coord].add(brick)
        brick_overlaps = collections.defaultdict(set)
        for brick, footprint in footprints.items():
            for coord in footprint:
                brick_overlaps[brick].update(brick_by_x_y[coord])

        # Track which other bricks a given brick is supporting.
        holding: dict[int, list[int]] = {brick: [] for brick in bricks}
        held_by: dict[int, list[int]] = {brick: [] for brick in bricks}
        # Drop bricks until all bricks have settled; this is the updated brick list.
        settled: set[int] = set()
        settled_bricks: dict[int, list[int]] = {}
        # Sort bricks by lowest bottom, i.e. the order in which they land.
        landing_order = sorted(bricks, key=lambda x: bricks[x][2])

        for brick in landing_order:
            start_x, start_y, start_z, end_x, end_y, end_z = bricks[brick]
            # Locate settled bricks in the same column(s) as this brick.
            potential_tops = brick_overlaps[brick] & settled
            # Find the highest point beneath the current brick.
            lands_at_height = max(
                (settled_bricks[other][5] for other in potential_tops if settled_bricks[other][5] < start_z),
                default=0,
            )
            
            # Add the brick in it's final position to the settled data.
            drop_distance = start_z - lands_at_height - 1
            start_z -= drop_distance
            end_z -= drop_distance
            settled_bricks[brick] = (start_x, start_y, start_z, end_x, end_y, end_z)
            settled.add(brick)

            # Which bricks will be the support?
            lands_on_bricks = {other for other in potential_tops if settled_bricks[other][5] == lands_at_height}
            for other in lands_on_bricks:
                holding[other].append(brick)
            held_by[brick].extend(lands_on_bricks)

        bricks = settled_bricks

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
        return {idx: tuple(values) for idx, values in enumerate(data)}

# vim:expandtab:sw=4:ts=4
