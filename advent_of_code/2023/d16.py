#!/bin/python
"""Advent of Code, Day 16: The Floor Will Be Lava."""

from lib import aoc

UP, DOWN, RIGHT, LEFT = (0, -1), (0, 1), (1, 0), (-1, 0)
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


class Day16(aoc.Challenge):
    """Day 16: The Floor Will Be Lava."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=46),
        aoc.TestCase(inputs=SAMPLE, part=2, want=51),
    ]

    def energized(self, edges: tuple[int, int, int, int], board: dict[tuple[int, int], str], start_pos: tuple[int, int], start_dir: tuple[int, int]) -> int:
        """Compute the number of energized tiles."""
        min_x, min_y, max_x, max_y = edges
        seen = set()
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

    def part1(self, puzzle_input: dict[tuple[int, int], str]) -> int:
        """Return the number of energized tiles, assuming a given start."""
        return self.energized(puzzle_input.edges, puzzle_input.chars, (-1, 0), RIGHT)

    def part2(self, puzzle_input: dict[tuple[int, int], str]) -> int:
        """Return the number of energized tiles, across all starts."""
        char_map = puzzle_input.chars
        min_x, min_y, max_x, max_y = puzzle_input.edges

        return max(
            # Left edge.
            max(
                self.energized(puzzle_input.edges, char_map, (min_x - 1, y), RIGHT)
                for y in range(min_y, max_y + 1)
            ),
            # Right edge.
            max(
                self.energized(puzzle_input.edges, char_map, (max_x + 1, y), LEFT)
                for y in range(min_y, max_y + 1)
            ),
            # Top.
            max(
                self.energized(puzzle_input.edges, char_map, (x, min_y - 1), DOWN)
                for x in range(min_x, max_x + 1)
            ),
            # Bottom.
            max(
                self.energized(puzzle_input.edges, char_map, (x, max_y + 1), UP)
                for x in range(min_x, max_x + 1)
            ),
        )

# vim:expandtab:sw=4:ts=4
