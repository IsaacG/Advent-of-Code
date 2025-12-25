#!/bin/python
"""Advent of Code, Day 13: Mine Cart Madness. Move carts around a track, handling collisions."""

from lib import aoc

SAMPLE = [
    """\
|
v
|
|
|
^
|""",
# ==============
r"""/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   """,
# ==============
r"""/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/""",
]

InputType = tuple[
    dict[complex, dict[complex, complex]],
    set[complex],
    dict[complex, tuple[complex, int]],
]

ROT_LEFT = complex(0, -1)
ROT_STRAIGHT = complex(1, -0)
ROT_RIGHT = complex(0, 1)
ROTATIONS = [ROT_LEFT, ROT_STRAIGHT, ROT_RIGHT]
UP, DOWN, RIGHT, LEFT = aoc.FOUR_DIRECTIONS

DIRECTIONS = aoc.ARROW_DIRECTIONS
CORNERS = {
    "/": {UP: RIGHT, LEFT: DOWN, RIGHT: UP, DOWN: LEFT},
    "\\": {UP: LEFT, LEFT: UP, RIGHT: DOWN, DOWN: RIGHT},
}



TESTS = [(1, SAMPLE[0], "0,3"), (1, SAMPLE[1], "7,3"), (2, SAMPLE[2], "6,4")]

def solve(data: InputType, part: int) -> str:
    """Simulate wagons driving a track."""
    turns, junctions, wagons = data

    for _ in range(20000):
        # Part 2: Return the location of the last cart.
        if len(wagons) == 1:
            location = list(wagons)[0]
            return f"{int(location.real)},{int(location.imag)}"

        for location in aoc.reading_order(wagons):
            # A wagon may be removed due to a collision.
            if location not in wagons:
                continue

            direction, rotation = wagons[location]
            new_location = location + direction
            del wagons[location]

            # Rotate the wagon at corners and junctions.
            if new_location in junctions:
                direction *= ROTATIONS[rotation % 3]
                rotation += 1
            elif new_location in turns:
                direction = turns[new_location][direction]

            # Collisions detection.
            if new_location in wagons:
                # Part 1: return the location of the first collision.
                if part == 1:
                    return f"{int(new_location.real)},{int(new_location.imag)}"
                del wagons[new_location]
            else:
                wagons[new_location] = (direction, rotation)

    raise RuntimeError("Failed to solve.")

def input_parser(data: str) -> InputType:
    """Parse the input."""
    parsed = aoc.CoordinatesParserC().parse(data)
    junctions = parsed.coords.get("+", set())
    turns = {coord: CORNERS[char] for char in "/\\" for coord in parsed.coords.get(char, [])}
    wagons_directions = {coord: direction for char, direction in DIRECTIONS.items() for coord in parsed.coords.get(char, [])}
    wagons = {location: (direction, 0) for location, direction in wagons_directions.items()}
    return (turns, junctions, wagons)
