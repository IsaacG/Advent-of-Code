#!/bin/python
"""Advent of Code, Day 14: Parabolic Reflector Dish."""

from lib import aoc

SAMPLE = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

InputType = tuple[set[complex], set[complex]]
STEPS_P2 = 1000000000


class Day14(aoc.Challenge):
    """Day 14: Parabolic Reflector Dish."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=136),
        aoc.TestCase(inputs=SAMPLE, part=2, want=64),
    ]

    def part1(self, parsed_input: InputType) -> int:
        """Tilt the board north."""
        stationary, moving = parsed_input
        min_x, min_y, max_x, max_y = aoc.bounding_coords(stationary | moving)
        north = complex(0, -1)

        post_move = set(stationary)
        for rock in sorted(moving, key=lambda x: x.imag):
            while (new_pos := rock + north) not in post_move and rock.imag > 0:
                rock = new_pos
            post_move.add(rock)
        moving = post_move - stationary

        return int(sum(max_y + 1 - rock.imag for rock in moving))

    def cycle(self, moving, stationary):
        """Tilt the board in four directions."""
        min_x, min_y, max_x, max_y = aoc.bounding_coords(stationary | moving)
        north = complex(0, -1)
        west = complex(-1, 0)
        south = complex(0, 1)
        east = complex(+1, 0)

        # North
        post_move = set(stationary)
        for rock in sorted(moving, key=lambda x: x.imag, reverse=False):
            while (new_pos := rock + north) not in post_move and rock.imag > min_y:
                rock = new_pos
            post_move.add(rock)
        moving = post_move - stationary

        # West
        post_move = set(stationary)
        for rock in sorted(moving, key=lambda x: x.real, reverse=False):
            while (new_pos := rock + west) not in post_move and rock.real > min_x:
                rock = new_pos
            post_move.add(rock)
        moving = post_move - stationary

        # South
        post_move = set(stationary)
        for rock in sorted(moving, key=lambda x: x.imag, reverse=True):
            while (new_pos := rock + south) not in post_move and rock.imag < max_y:
                rock = new_pos
            post_move.add(rock)
        moving = post_move - stationary

        # East
        post_move = set(stationary)
        for rock in sorted(moving, key=lambda x: x.real, reverse=True):
            while (new_pos := rock + east) not in post_move and rock.real < max_x:
                rock = new_pos
            post_move.add(rock)
        moving = post_move - stationary

        return moving

    def part2(self, parsed_input: InputType) -> int:
        """Tilt the board in four directions for many cycles."""
        stationary, moving = parsed_input
        min_x, min_y, max_x, max_y = aoc.bounding_coords(stationary | moving)

        # Find a cycle in the rotation.
        cache = {}
        for step in range(STEPS_P2):
            moving = self.cycle(moving, stationary)

            frozen = frozenset(moving)
            if frozen in cache:
                cycle_size = (step - cache[frozen])
                remaining_steps = STEPS_P2 - step - 1
                remaining_steps %= cycle_size
                for _ in range(remaining_steps):
                    moving = self.cycle(moving, stationary)
                break
            cache[frozenset(moving)] = step

        return int(sum(max_y + 1 - rock.imag for rock in moving))

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return (
            aoc.parse_ascii_bool_map("#").parse(puzzle_input),
            aoc.parse_ascii_bool_map("O").parse(puzzle_input),
        )

# vim:expandtab:sw=4:ts=4
