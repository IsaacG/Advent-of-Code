#!/bin/python
"""Advent of Code, Day 17: Pyroclastic Flow. Compute the height of a Tetris-like rock pile after rocks have landed."""

import collections
import itertools

import typer
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
SAMPLE = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'
GRAVITY = complex(0, -1)
InputType = str


class Day17(aoc.Challenge):
    """Day 17: Pyroclastic Flow."""

    DEBUG = False
    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=3068),
        aoc.TestCase(inputs=SAMPLE, part=2, want=1514285714288),
    ]
    INPUT_PARSER = aoc.parse_one_str
    PARAMETERIZED_INPUTS = [2022, 1000000000000]

    def pre_run(self, parsed_input: InputType) -> None:
        """Parse the rock shapes from ASCII art."""
        rocks = []
        parser = aoc.parse_ascii_bool_map("#")
        for block in ROCKS.strip().split("\n\n"):
            block = block.replace(" ", "")
            # Flip rocks upside down so Y increases from the bottom to the top.
            # Most my parsing assumes Y increases as you move down through text.
            block = "\n".join(reversed(block.splitlines()))
            rocks.append(parser.parse(block))
        self.rocks = rocks
        self.rock_heights = [int(max(i.imag for i in r)) for r in rocks]

    def solver(self, parsed_input: InputType, target_rock_count: int) -> int:
        """Compute the height of the tower after n rocks have fallen."""
        rocks = self.rocks
        stream = parsed_input
        if len(stream) < 50:
            stream *= 3 * 5 * 7
        stream_size = len(stream)

        landed = set()
        tower_height = 0
        seen2 = collections.defaultdict[list]
        seen = {}
        landing_position = collections.deque(maxlen=10)
        height_deltas = []

        # Index counter which wraps around.
        wind_idx_iter = itertools.cycle(range(stream_size))

        # My input luckily gives flat tops every so often.
        # I rely on flat tops to avoid parsing topologies.
        # TODO: stop relying on this property.
        def top_is_flat() -> bool:
            """Return if the top is flat."""
            return all(complex(x, tower_height) in landed for x in range(7))

        # Drop rocks.
        for rock_cnt in range(min(5000, target_rock_count)):
            rock_shape = rocks[rock_cnt % 5]
            bottom_left_corner = complex(2, tower_height + 4)

            # Apply wind then gravity until it hits rock bottom.
            while True:
                # Apply wind when it doesn't blow into rock.
                wind_idx = next(wind_idx_iter)
                wind = -1 if stream[wind_idx] == "<" else +1
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
            next_height = max(tower_height, int(bottom_left_corner.imag) + self.rock_heights[rock_cnt%5])
            height_delta = next_height - tower_height
            # Used to track the position of the last N rocks which landed, for cycle detection.
            landing_position.append(height_delta * 7 + int(bottom_left_corner.real))
            # Store the heights to replay N steps after applying cyclic growth.
            height_deltas.append(next_height - tower_height)
            tower_height = next_height

            # Mark this setup to detect a repeat for cycle detection.
            fingerprint = (wind_idx, rock_cnt % 5, tuple(landing_position))
            # We have b
            if fingerprint in seen:
                prior_rock_cnt, prior_height = seen[fingerprint]
                cycle_size = rock_cnt - prior_rock_cnt
                # if cycle_size < 1500: continue

                self.debug(f"Cycle found {prior_rock_cnt, prior_height} -> {rock_cnt, tower_height} {rock_cnt - prior_rock_cnt, tower_height - prior_height})")

                height_diff = tower_height - prior_height

                # Apply N cycles of changes plus the remainder of rocks needed.
                cycle_count, remaining = divmod(target_rock_count - rock_cnt, cycle_size)
                tower_height += cycle_count * height_diff
                tower_height += sum(height_deltas[prior_rock_cnt + 1:prior_rock_cnt + remaining])
                return tower_height
            seen[fingerprint] = (rock_cnt, tower_height)

        if rock_cnt + 1 == target_rock_count:
            return tower_height
        return 0


if __name__ == "__main__":
    typer.run(Day17().run)

# vim:expandtab:sw=4:ts=4
