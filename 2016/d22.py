#!/bin/python
"""Advent of Code, Day 22: Grid Computing. Shuffle data around to access secrets."""

from lib import aoc

InputType = dict[tuple[int, int], tuple[int, int]]


class Day22(aoc.Challenge):
    """Day 22: Grid Computing."""

    TESTS = [
        aoc.TestCase(inputs="", part=1, want=aoc.TEST_SKIP),
        aoc.TestCase(inputs="", part=2, want=aoc.TEST_SKIP),
    ]

    def part1(self, parsed_input: InputType) -> int:
        count = 0
        for used, _ in parsed_input.values():
            if used == 0:
                continue
            for _, avail in parsed_input.values():
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

        Once in position, the hole can be used to slide the data across to the destination.
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
            for pos_y in range(max_y + 1):
                out = []
                for pos_x in range(max_x + 1):
                    if (pos_x, pos_y) == (0, 0):
                        out.append("!")
                    elif (pos_x, pos_y) == hole_pos:
                        out.append("H")
                    elif (pos_x, pos_y) == goal:
                        out.append("G")
                    elif (pos_x, pos_y) in fits:
                        out.append(".")
                    else:
                        assert (pos_x, pos_y) in oversized
                        out.append("#")
                self.debug("".join(out))
            self.debug(f"{step_counter=}\n")

        wall_left = min(x for x, y in oversized)
        wall_y = next(y for x, y in oversized)
        assert hole_pos[1] > wall_y, "Hole should be below wall"

        print_map("Initial")
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

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        data = {}
        for line in puzzle_input.splitlines()[2:]:
            # Filesystem (x, y)  Size  Used  Avail  Use%
            pos_x, pos_y, _, used, avail, _ = (int(i) for i in aoc.RE_INT.findall(line))
            data[pos_x, pos_y] = used, avail
        return data
