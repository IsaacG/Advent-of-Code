#!/bin/python
"""Advent of Code, Day 19: A Series of Tubes."""
import itertools
import string
from lib import aoc

# Blocking pipes.
BLOCKING = {complex(0, 1): "-", complex(1, 0): "|"}
BLOCKING |= {-d: v for d, v in BLOCKING.items()}
# Possible directions after rotating.
ROTATE = {d: {d * 1j, d * -1j} for d in aoc.FOUR_DIRECTIONS}


def solve(data: aoc.MapC, part: int) -> int | str:
    """Walk the maze and track steps/letters."""
    maze = data.chars
    # Initialize
    direction = complex(0, 1)
    location = next(i for i in maze if i.imag == 0)
    result = []
    # Walk the maze.
    for step in itertools.count(1):
        # Track letters.
        cur_char = str(maze[location])
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
            return "".join(result) if part == 1 else step
    raise RuntimeError("No solution found.")


PARSER = aoc.CoordinatesParserC(ignore=" ")
SAMPLE = """\
     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+"""
TESTS = [
    (1, SAMPLE, "ABCDEF"),
    (2, SAMPLE, 38),
]
# vim:expandtab:sw=4:ts=4
