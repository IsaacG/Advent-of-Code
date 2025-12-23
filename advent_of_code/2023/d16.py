#!/bin/python
"""Advent of Code, Day 16: The Floor Will Be Lava."""
import typing
from lib import aoc
UP, DOWN, RIGHT, LEFT = (0, -1), (0, 1), (1, 0), (-1, 0)


def energized(
    board: dict[tuple[int, int], str],
    start_pos: tuple[int, int],
    start_dir: tuple[int, int],
) -> int:
    """Compute the number of energized tiles."""
    seen = set[tuple[tuple[int, int], tuple[int, int]]]()
    beams = {(start_pos, start_dir)}
    while beams:
        new_beams = set()
        for pos, direction in beams:
            pos = (pos[0] + direction[0], pos[1] + direction[1])
            if (char := board.get(pos, None)) is None:
                # Off the map.
                pass
            elif char == ".":
                # Pass through empty space and pointy side of splitters.
                new_beams.add((pos, direction))
            elif char == "|":
                if direction in (UP, DOWN):
                    new_beams.add((pos, direction))
                else:
                    # Split.
                    new_beams.add((pos, UP))
                    new_beams.add((pos, DOWN))
            elif char == "-":
                if direction in (RIGHT, LEFT):
                    new_beams.add((pos, direction))
                else:
                    # Split.
                    new_beams.add((pos, RIGHT))
                    new_beams.add((pos, LEFT))
            elif char == "/":
                # Rotate.
                if direction in (RIGHT, LEFT):
                    new_beams.add((pos, aoc.rotate_clockwise(*direction)))
                else:
                    new_beams.add((pos, aoc.rotate_counterclockwise(*direction)))
            elif char == "\\":
                # Rotate.
                if direction in (RIGHT, LEFT):
                    new_beams.add((pos, aoc.rotate_counterclockwise(*direction)))
                else:
                    new_beams.add((pos, aoc.rotate_clockwise(*direction)))
        # Ignore already-handled beams (loop detection).
        beams = new_beams - seen
        seen.update(new_beams)

    return len({position for position, direction in seen})


def solve(data: aoc.Map, part: int) -> int:
    """Return the number of energized tiles."""
    char_map = typing.cast(dict[tuple[int, int], str], data.chars)
    min_x, min_y, max_x, max_y = data.edges
    if part == 1:
        return energized(char_map, (-1, 0), RIGHT)

    return max(
        # Left edge.
        max(
            energized(char_map, (min_x - 1, y), RIGHT)
            for y in range(min_y, max_y + 1)
        ),
        # Right edge.
        max(
            energized(char_map, (max_x + 1, y), LEFT)
            for y in range(min_y, max_y + 1)
        ),
        # Top.
        max(
            energized(char_map, (x, min_y - 1), DOWN)
            for x in range(min_x, max_x + 1)
        ),
        # Bottom.
        max(
            energized(char_map, (x, max_y + 1), UP)
            for x in range(min_x, max_x + 1)
        ),
    )


SAMPLE = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""
TESTS = [(1, SAMPLE, 46), (2, SAMPLE, 51)]
# vim:expandtab:sw=4:ts=4
