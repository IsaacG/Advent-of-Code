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
UP = complex(0, -1)
DOWN = complex(0, 1)
LEFT = complex(-1, 0)
RIGHT = complex(1, 0)

DIRECTIONS = {"^": UP, "v": DOWN, "<": LEFT, ">": RIGHT}
CORNERS = {
    "/": {UP: RIGHT, LEFT: DOWN, RIGHT: UP, DOWN: LEFT},
    "\\": {UP: LEFT, LEFT: UP, RIGHT: DOWN, DOWN: RIGHT},
}


class Day13(aoc.Challenge):
    """Day 13: Mine Cart Madness."""

    PARAMETERIZED_INPUTS = [False, True]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want="0,3"),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want="7,3"),
        aoc.TestCase(inputs=SAMPLE[2], part=2, want="6,4"),
    ]

    def solver(self, parsed_input: InputType, param: bool) -> str:
        """Simulate wagons driving a track."""
        turns, junctions, wagons = parsed_input

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
                    if not param:
                        return f"{int(new_location.real)},{int(new_location.imag)}"
                    del wagons[new_location]
                else:
                    wagons[new_location] = (direction, rotation)

        raise RuntimeError("Failed to solve.")

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        # tracks = aoc.parse_ascii_bool_map("/\-|+^v<>").parse(puzzle_input)
        junctions = aoc.parse_ascii_bool_map("+").parse(puzzle_input)
        turns = aoc.parse_ascii_char_map(lambda x: CORNERS.get(x, None)).parse(puzzle_input)
        wagons_directions = aoc.parse_ascii_char_map(
            lambda x: DIRECTIONS.get(x, None)
        ).parse(puzzle_input)
        wagons = {location: (direction, 0) for location, direction in wagons_directions.items()}
        return (turns, junctions, wagons)
