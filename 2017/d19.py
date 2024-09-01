#!/bin/python
"""Advent of Code, Day 19: A Series of Tubes."""

import itertools
import string

from lib import aoc

SAMPLE = """\
     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+"""

# Blocking pipes.
BLOCKING = {complex(0, 1): "-", complex(1, 0): "|"}
BLOCKING |= {-d: v for d, v in BLOCKING.items()}
# Possible directions after rotating.
ROTATE = {d: {d * 1j, d * -1j} for d in aoc.FOUR_DIRECTIONS}


class Day19(aoc.Challenge):
    """Day 19: A Series of Tubes."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want="ABCDEF"),
        aoc.TestCase(part=2, inputs=SAMPLE, want=38),
    ]

    INPUT_PARSER = aoc.parse_ascii_char_map(lambda x: None if x == " " else x)
    PARAMETERIZED_INPUTS = [False, True]

    def solver(self, parsed_input: dict[complex, str], param: bool) -> int | str:
        """Walk the maze and track steps/letters."""
        maze = parsed_input
        # Initialize
        direction = complex(0, 1)
        location = next(i for i in maze if i.imag == 0)
        result = []
        # Walk the maze.
        for step in itertools.count(1):
            # Track letters.
            cur_char = maze[location]
            if cur_char in string.ascii_letters:
                result.append(cur_char)
            # Check if we need to rotate, ie on a + and the next location is a perpendicular pipe.
            next_location = location + direction
            blocking = BLOCKING[direction]
            if cur_char == "+" and maze.get(next_location, blocking) == blocking:
                # Rotate in a direction where the next step would not be blocked.
                rot_blocking = BLOCKING[direction * 1j]
                direction = next(
                    d for d in ROTATE[direction]
                    if maze.get(location + d, rot_blocking) != rot_blocking
                )
            # Step forward.
            location += direction
            # Check if we fell off the maze.
            if location not in maze:
                return step if param else "".join(result)
        raise RuntimeError("No solution found.")

# vim:expandtab:sw=4:ts=4
