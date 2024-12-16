#!/bin/python
"""Advent of Code, Day 16: Reindeer Maze."""

import queue
from lib import aoc

SAMPLE = [
    """\
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############""",
    """\
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################""",
]


class Day16(aoc.Challenge):
    """Day 16: Reindeer Maze."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=7036),
        aoc.TestCase(part=1, inputs=SAMPLE[1], want=11048),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=45),
        aoc.TestCase(part=2, inputs=SAMPLE[1], want=64),
    ]

    def solver(self, puzzle_input: aoc.Map, part_one: bool) -> int:
        """Find the cheapest paths through a maze."""
        starts = puzzle_input.coords["S"]
        ends = puzzle_input.coords["E"]
        open_space = puzzle_input.coords["."] | starts | ends

        start = starts.pop()
        end = ends.pop()

        def score(p: complex) -> int:
            """Score a position -- distance to the end. A* heuristic."""
            return int(abs(end.real - p.real) + abs(end.imag - p.imag))

        # Track the lowest cost to get to a location -- and how you get there.
        lowest: dict[tuple[complex, complex], tuple[int, set[tuple[complex, complex]]]] = {(start, complex(1)): (0, set())}
        # Track what paths to explore next, cheapest first.
        todo: queue.PriorityQueue[tuple[int, int, float, float, float, float]] = queue.PriorityQueue()
        # Start at the start facing easy -- complex(1, 0).
        todo.put((score(start), 0, start.real, start.imag, 1, 0))

        while not todo.empty():
            # Pop the next option to explore.
            rank, cost, pos_x, pos_y, dir_x, dir_y = todo.get()
            pos = complex(pos_x, pos_y)
            direction = complex(dir_x, dir_y)
            if pos == end:
                if part_one:
                    return cost
                # Part two: walk the path backwards from the end to find seats.
                to_explore = {(end, direction)}
                good_seats = set()
                while to_explore:
                    p, d = to_explore.pop()
                    good_seats.add(p)
                    to_explore.update(lowest[p, d][1])
                return len(good_seats)

            # Options always include rotation and sometimes include moving forward.
            options = [(pos, direction * 1j, cost + 1000), (pos, direction * -1j, cost + 1000)]
            if (next_pos := pos + direction) in open_space:
                options.append((next_pos, direction, cost + 1))

            for next_pos, next_dir, next_cost in options:
                if (next_pos, next_dir) not in lowest:
                    lowest[(next_pos, next_dir)] = (next_cost, {(pos, direction)})
                    rank = score(next_pos) + next_cost
                    todo.put((rank, next_cost, next_pos.real, next_pos.imag, next_dir.real, next_dir.imag))
                elif lowest[(next_pos, next_dir)][0] == next_cost:
                    lowest[(next_pos, next_dir)][1].add((pos, direction))
        raise RuntimeError("Did not solve.")

# vim:expandtab:sw=4:ts=4
