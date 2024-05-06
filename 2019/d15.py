#!/bin/python
"""Advent of Code, Day 15: Oxygen System."""

import collections
import functools
import itertools

import intcode
from lib import aoc

DIRECTIONS = {
    complex(0, +1): 1,  # North
    complex(0, -1): 2,  # South
    complex(-1, 0): 3,  # West
    complex(+1, 0): 4,  # East
}
BOT_WALL  = 0
BOT_MOVED = 1
BOT_FOUND = 2


class Day15(aoc.Challenge):
    """Day 15: Oxygen System."""

    DEBUG = False
    PARAMETERIZED_INPUTS = [False, True]

    TESTS = [
        aoc.TestCase(inputs="", part=1, want=aoc.TEST_SKIP),
        aoc.TestCase(inputs="", part=2, want=aoc.TEST_SKIP),
    ]
    INPUT_PARSER = aoc.parse_one_str

    @functools.cache
    def explore(self, program: str) -> tuple[set[complex], set[complex], complex, int]:
        hall = {complex()}
        paths = {complex(): []}
        wall = set()
        q_i = collections.deque()
        q_o = collections.deque()
        oxygen = None
        oxygen_dist = None

        explored = hall | wall
        candidates = {
            (pos, direction) for pos in hall for direction in aoc.FOUR_DIRECTIONS
            if pos + direction not in explored
        }
        step = 0
        while candidates:
            step += 1
            if step and not step % 50:
                print(f"{step=}")
            new_paths = {}
            for pos, direction in candidates:
                computer = intcode.Computer(program, debug=self.DEBUG, input_q=q_i, output_q=q_o)
                new_pos = pos + direction
                path = paths[pos]
                for move in path:
                    q_i.append(DIRECTIONS[move])
                    computer.run()
                    q_o.popleft()
                    # assert q_o.popleft() == BOT_MOVED
                q_i.append(DIRECTIONS[direction])
                computer.run()
                got = q_o.popleft()
                if got == BOT_WALL:
                    wall.add(new_pos)
                else:
                    hall.add(new_pos)
                    new_paths[new_pos] = path + [direction]
                    if got == BOT_FOUND:
                        oxygen = new_pos
                        oxygen_dist = step
            paths = new_paths
            explored = hall | wall
            candidates = {
                (pos, direction) for pos in hall for direction in aoc.FOUR_DIRECTIONS
                if pos + direction not in explored
            }
        return hall, wall, oxygen, oxygen_dist

    def solver(self, parsed_input: str, param: bool) -> int:
        hall, wall, oxygen, oxygen_dist = self.explore(parsed_input)
        if not param:
            return oxygen_dist

        total_space = len(hall)
        filled = {oxygen}
        for step in itertools.count():
            if len(filled) == total_space:
                return step
            new = {
                pos + direction for pos in filled for direction in aoc.FOUR_DIRECTIONS
                if pos + direction not in wall
            }
            filled.update(new)

# vim:expandtab:sw=4:ts=4
