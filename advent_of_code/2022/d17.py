#!/bin/python
"""Advent of Code, Day 17: Pyroclastic Flow. Compute the height of a Tetris-like rock pile after rocks have landed."""

import collections
import itertools

from lib import aoc

ROCKS = """
    ####

    .#.
    ###
    .#.

    ..#
    ..#
    ###

    #
    #
    #
    #

    ##
    ##
    """
GRAVITY = complex(0, -1)


def build_rocks() -> None:
    """Parse the rock shapes from ASCII art."""
    rocks = []
    parser = aoc.CoordinatesParserC()
    for block in ROCKS.strip().split("\n\n"):
        block = block.replace(" ", "")
        # Flip rocks upside down so Y increases from the bottom to the top.
        # Most my parsing assumes Y increases as you move down through text.
        block = "\n".join(reversed(block.splitlines()))
        rocks.append(parser.parse(block)["#"])
    rock_heights = [int(max(i.imag for i in r)) for r in rocks]
    return rocks, rock_heights


def solve(data: str, part: int) -> int:
    """Compute the height of the tower after n rocks have fallen."""
    # Rounds to run, part 1 vs part 2.
    target_rock_count = 2022 if part == 1 else 1000000000000
    rocks, rock_heights = build_rocks()
    stream = data
    stream_size = len(stream)
    # Wind directions, translated to a number.
    wind_direction = [aoc.ARROW_DIRECTIONS[i] for i in stream]
    # Index counter which wraps around.
    wind_idx_iter = itertools.cycle(range(stream_size))

    # All the state we need to track.
    landed = set()
    tower_height = 0
    seen = {}
    height_deltas = []

    # Drop rocks.
    for rock_cnt in range(target_rock_count):
        rock_shape = rocks[rock_cnt % 5]
        # Rocks materialize at this offset.
        bottom_left_corner = complex(2, tower_height + 4)

        # Apply wind then gravity until it hits rock bottom.
        while True:
            # Apply wind when it doesn't blow into rock.
            wind_idx = next(wind_idx_iter)
            wind = wind_direction[wind_idx]
            new_corner = wind + bottom_left_corner
            new_rock_positions = {r + new_corner for r in rock_shape}
            if all(0 <= r.real < 7 for r in new_rock_positions) and landed.isdisjoint(new_rock_positions):
                bottom_left_corner = new_corner

            # Apply gravity or stop moving.
            new_corner = GRAVITY + bottom_left_corner
            new_rock_positions = {r + new_corner for r in rock_shape}
            if all(0 < r.imag for r in new_rock_positions) and landed.isdisjoint(new_rock_positions):
                bottom_left_corner = new_corner
            else:
                break

        # Update data.
        landed.update({bottom_left_corner + r for r in rock_shape})
        next_height = max(tower_height, int(bottom_left_corner.imag) + rock_heights[rock_cnt%5])
        # Store the heights to replay N steps after applying cyclic growth.
        height_deltas.append(next_height - tower_height)
        tower_height = next_height

        # Mark this setup to detect a repeat for cycle detection.
        fingerprint = (wind_idx, rock_cnt % 5, int(bottom_left_corner.real))
        # Wait at least 50 rocks for the board to get into a steady state.
        if rock_cnt > 50 and fingerprint in seen:
            prior_rock_cnt, prior_height = seen[fingerprint]
            cycle_size = rock_cnt - prior_rock_cnt
            height_diff = tower_height - prior_height

            # Apply N cycles of changes plus the remainder of rocks needed.
            cycle_count, remaining = divmod(target_rock_count - rock_cnt, cycle_size)
            tower_height += cycle_count * height_diff
            tower_height += sum(height_deltas[prior_rock_cnt + 1:prior_rock_cnt + remaining])
            return tower_height
        seen[fingerprint] = (rock_cnt, tower_height)

    # Part 1.
    if rock_cnt + 1 == target_rock_count:
        return tower_height
    raise RuntimeError("Not found")


SAMPLE = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'
TESTS = [(1, SAMPLE, 3068), (2, SAMPLE, 1514285714288)]
