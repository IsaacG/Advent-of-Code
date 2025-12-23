#!/bin/python
"""Advent of Code, Day 20: Race Condition."""

import queue
from lib import aoc

SAMPLE = """\
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""


class Day20(aoc.Challenge):
    """Day 20: Race Condition."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=5),
        aoc.TestCase(part=2, inputs=SAMPLE, want=41),
    ]

    def solver(self, puzzle_input: aoc.Map, part_one: bool) -> int:
        # I use tuples for walking the maze and complex for cheat logic.
        spaces = puzzle_input.coords["."] | puzzle_input.coords["E"] | puzzle_input.coords["S"]
        coords = puzzle_input.coords
        spaces = coords["."] | coords["E"] | coords["S"]
        end = coords["E"].pop()

        cheat_distance = 2 if part_one else 20
        threshold = (15 if part_one else 70) if self.testing else 100

        # Walk the maze from the end, computing the distance from any spot to the end.
        todo: queue.PriorityQueue[tuple[int, tuple[int, int]]] = queue.PriorityQueue()
        todo.put((0, end))
        seen = {end}
        distance_from_end = {}

        while not todo.empty():
            cost, pos = todo.get()
            distance_from_end[pos] = cost

            for neighbor in aoc.t_neighbors4(pos):
                if neighbor not in seen and neighbor in spaces:
                    seen.add(neighbor)
                    todo.put((cost + 1, neighbor))

        # Compute all the cheat offsets and how many steps those take.
        offsets = {
            (x, y): abs(x) + abs(y)
            for x in range(-cheat_distance, cheat_distance + 1)
            for y in range(-cheat_distance, cheat_distance + 1)
            if abs(x) + abs(y) <= cheat_distance
        }

        # For each start position, check where a cheat can take us and what the savings are.
        cheats = 0
        for cheat_from in spaces:
            for cheat_delta, cheat_cost in offsets.items():
                cheat_to = (cheat_from[0] + cheat_delta[0], cheat_from[1] + cheat_delta[1])
                if cheat_to in spaces:
                    saves = distance_from_end[cheat_from] - distance_from_end[cheat_to] - cheat_cost
                    if saves >= threshold:
                        cheats += 1

        return cheats

# vim:expandtab:sw=4:ts=4
