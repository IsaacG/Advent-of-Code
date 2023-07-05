#!/bin/python
"""Advent of Code, Day 22: Grid Computing."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import queue
import re

from lib import aoc

SAMPLE = """\
root@ebhq-gridcenter# df -h
Filesystem            Size  Used  Avail  Use%
/dev/grid/node-x0-y0   10T    8T     2T   80%
/dev/grid/node-x0-y1   11T    6T     5T   54%
/dev/grid/node-x0-y2   32T   28T     4T   87%
/dev/grid/node-x1-y0    9T    7T     2T   77%
/dev/grid/node-x1-y1    8T    0T     8T    0%
/dev/grid/node-x1-y2   11T    7T     4T   63%
/dev/grid/node-x2-y0   10T    6T     4T   60%
/dev/grid/node-x2-y1    9T    8T     1T   88%
/dev/grid/node-x2-y2    9T    6T     3T   66%
"""

LineType = int
InputType = list[LineType]


class Day22(aoc.Challenge):
    """Day 22: Grid Computing."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=aoc.TEST_SKIP),
        aoc.TestCase(inputs=SAMPLE, part=2, want=aoc.TEST_SKIP),
    ]

    def part1(self, parsed_input: InputType) -> int:
        count = 0
        for node_a, (used, _) in parsed_input.items():
            if used == 0:
                continue
            for node_b, (_, avail) in parsed_input.items():
                if used <= avail:
                    count += 1

        return count

    def part2(self, parsed_input: InputType) -> int:
        """Move the goal data into the 0, 0 position.

        This is an "8-puzzle" where there is one "hole" we can slide around
        to move blocks of data. There are some "large" blocks which do not fit
        and cannot be moved. All other blocks have larger disk sizes (min_size)
        than the largest block of data which we move (max_used).

        Looking at the output, the hole starts out at the bottom, blocked by a wall
        of large blocks. The hole needs to move around the wall then to the top right.
        """
        step_counter = 0
        # This is the empty "hole" used to move data.
        hole_pos, hole_size = next(
            (i, avail) for i, (used, avail) in parsed_input.items()
            if used == 0
        )
        max_x = max(x for x, y in parsed_input)
        max_y = max(y for x, y in parsed_input)
        # This is the goal data we want to read.
        goal = (max_x, 0)
        # These are disks small enough to be used.
        fits = {
            pos for pos, (used, avail) in parsed_input.items()
            if used <= hole_size
        }
        # These are unmoveable blocks.
        oversized = {
            pos for pos, (used, avail) in parsed_input.items()
            if used > hole_size
        }
        # Validate all the "fits" blocks are useable.
        max_used = max(
            used for pos, (used, avail) in parsed_input.items()
            if pos in fits
        )
        min_size = min(
            used + avail for pos, (used, avail) in parsed_input.items()
            if pos in fits
        )
        assert min_size >= max_used, f"{min_size=}, {max_used=}"
        # Validate the goal is moveable.
        assert goal in fits

        def print_map(msg):
            if not self.DEBUG:
                return
            self.debug(msg)
            for y in range(max_y + 1):
                out = []
                for x in range(max_x + 1):
                    if (x, y) == (0, 0):
                        out.append("!")
                    elif (x, y) == hole_pos:
                        out.append("H")
                    elif (x, y) == goal:
                        out.append("G")
                    elif (x, y) in fits:
                        out.append(".")
                    else:
                        assert (x, y) in oversized
                        out.append("#")
                self.debug("".join(out))
            self.debug(f"{step_counter=}\n")

        print_map("Initial")

        wall_left = min(x for x, y in oversized)
        wall_y = next(y for x, y in oversized)
        assert hole_pos[1] > wall_y, "Hole should be below wall"
        # Walk the hole horizontally to the left of the wall.
        step_counter += hole_pos[0] - wall_left + 1
        hole_pos = (wall_left - 1, hole_pos[1])
        print_map("Hole left of wall")
        # Walk the hole vertically to the y=0 row.
        step_counter += hole_pos[1]
        hole_pos = (hole_pos[0], 0)
        print_map("Hole to top of board")
        # Walk the hole vertically to the goal position.
        # This shifts the goal data one spot towards the destination.
        step_counter += goal[0] - wall_left + 1
        hole_pos = goal
        goal = (goal[0] - 1, goal[1])
        print_map("Hole to top right, behind goal")
        # Moving the data over requires 4 steps to move the hole around the data
        # plus a fifth step for the actual swap.
        step_counter += 5 * goal[0]
        return step_counter


    def part2_ugh(self, parsed_input: InputType) -> int:
        max_x = max(x for x, y in parsed_input)
        max_y = max(y for x, y in parsed_input)
        want_x, want_y, steps = max_x, 0, 0
        score = want_x + want_y + steps

        todo = queue.PriorityQueue()
        todo.put((score, steps, want_x, want_y, frozenset(parsed_input.items())))
        seen = {frozenset(parsed_input.items())}
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while todo:
            _, steps, want_x, want_y, data = todo.get()
            data = dict(data)
            next_steps = steps + 1
            print(steps, want_x, want_y)
            print(len(seen))
            if len(seen) > 1000:
                return
            
            if want_x == 0 and want_y == 0:
                return steps

            for (a_x, a_y), (used_a, avail_a) in data.items():
                if used_a == 0:
                    continue
                for d_x, d_y in directions:
                    b_x, b_y = a_x + d_x, a_y + d_y
                    if not (0 <= b_x <= max_x and 0 <= b_y <= max_y):
                        continue
                    used_b, avail_b = data[b_x, b_y]
                    if avail_b < used_a:
                        continue

                    new_state = data.copy()
                    new_state[a_x, a_y] = (0, used_a + avail_a)
                    new_state[b_x, b_y] = (used_a + used_b, avail_b - used_a)

                    new_state_f = frozenset(new_state.items())
                    if new_state_f in seen:
                        continue
                    seen.add(new_state_f)

                    next_want_x, next_want_y = want_x, want_y
                    if a_x == want_x and a_y == want_y:
                        next_want_x, next_want_y = a_x, a_y

                    score = next_steps + next_want_x + next_want_y
                    todo.put((score, next_steps, next_want_x, next_want_y, new_state_f))
        raise NotImplementedError

    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        raise NotImplementedError

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        data = {}
        for line in puzzle_input.splitlines()[2:]:
            pos_x, pos_y, size, used, avail, _ = (int(i) for i in aoc.RE_INT.findall(line))
            data[pos_x, pos_y] = used, avail
        return data


# vim:expandtab:sw=4:ts=4
