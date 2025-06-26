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

    def cycle(self, moving, stationary):
        """Tilt the board in four directions."""
        min_x, min_y, max_x, max_y = aoc.bounding_coords(stationary | moving)
        # This logic can be deduped by rotating the grid by 1j and looping 4x.
        # However, that seems to run 50% slower.
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

    def part1(self, puzzle_input: InputType) -> int:
        """Tilt the board north."""
        height, (stationary, moving) = puzzle_input.height, puzzle_input.get_coords("#O")
        north = complex(0, -1)

        post_move = set(stationary)
        for rock in sorted(moving, key=lambda x: x.imag):
            while (new_pos := rock + north) not in post_move and rock.imag > 0:
                rock = new_pos
            post_move.add(rock)
        moving = post_move - stationary

        return int(sum(height - rock.imag for rock in moving))

    def part2(self, puzzle_input: InputType) -> int:
        """Tilt the board in four directions for many cycles."""
        height, (stationary, moving) = puzzle_input.height, puzzle_input.get_coords("#O")

        # Find a cycle in the rotation.
        step_to_map = []
        map_to_step = {}
        for step in range(STEPS_P2):
            moving = self.cycle(moving, stationary)

            frozen = frozenset(moving)
            if frozen in map_to_step:
                cycle_size = (step - map_to_step[frozen])
                remaining_steps = STEPS_P2 - step - 1
                remaining_steps %= cycle_size
                moving = step_to_map[map_to_step[frozen] + remaining_steps]
                break
            map_to_step[frozen] = step
            step_to_map.append(frozen)

        return int(sum(height - rock.imag for rock in moving))

# vim:expandtab:sw=4:ts=4
