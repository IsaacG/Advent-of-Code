#!/bin/python
"""Advent of Code, Day 22: Mode Maze."""

import functools
import queue
from lib import aoc


class PriorityOnceQ(queue.PriorityQueue):
    """Priority queue that avoids adding repeated items."""

    def __init__(self, target_x: int, target_y: int):
        self.target_x = target_x
        self.target_y = target_y
        self.seen = {}
        super().__init__()

    def put(self, delay: int, old_time: int, x: int, y: int, item: int) -> None:
        # Only add once
        new_time = old_time + delay
        fp = (x, y, item)
        if fp in self.seen and self.seen[fp] <= new_time:
            return
        self.seen[fp] = new_time

        # A-star with the Manhatten distance.
        rank = new_time + abs(self.target_x - x) + abs(self.target_y - y)
        super().put((rank, new_time, x, y, item))

    def get(self) -> tuple[int, int, int, int]:
        """Return an item from the queue -- and keep a copy."""
        self.got = super().get()[1:]
        return self.got

    def equip(self, item: int) -> None:
        """Equip an item; takes 7 minutes."""
        self.put(7, *self.got[:-1], item)

    def move(self, x: int, y: int) -> None:
        """Move to a new location; takes 1 minute."""
        self.put(1, self.got[0], x, y, self.got[-1])


class Day22(aoc.Challenge):
    """Day 22: Mode Maze."""

    TESTS = [
        aoc.TestCase(part=1, inputs="depth: 510\n target: 10,10", want=114),
        aoc.TestCase(part=2, inputs="depth: 510\n target: 10,10", want=45),
    ]
    INPUT_PARSER = aoc.parse_ints

    def solver(self, puzzle_input: list[list[int]], part_one: bool) -> int:
        """Solve the puzzle."""
        (depth,), (target_x, target_y) = puzzle_input

        def geo_idx(x: int, y: int) -> int:
            """Return the geologic index for a location."""
            if x == target_x and y == target_y:
                return 0
            if x == 0:
                return y * 48271
            if y == 0:
                return x * 16807
            return erosion(x - 1, y) * erosion(x, y - 1)

        @functools.cache
        def erosion(x: int, y: int) -> int:
            """Return the erosion for a location."""
            return (geo_idx(x, y) + depth) % 20183

        @functools.cache
        def terrain(x: int, y: int) -> int:
            """Return the terrain type for a location."""
            return erosion(x, y) % 3

        if part_one:
            return sum(terrain(x, y) for x in range(target_x + 1) for y in range(target_y + 1))

        CLIMBING, TORCH, NEITHER = range(3)
        ITEMS = {CLIMBING, TORCH, NEITHER}
        INVALID = [NEITHER, TORCH, CLIMBING]
        VALID = [ITEMS - {i} for i in INVALID]
        MUTUAL_VALID = {
            (a, b): (VALID[a] & VALID[b]).pop()
            for a in range(3)
            for b in range(3)
            if a != b
        }

        q = PriorityOnceQ(target_x, target_y)
        q.put(0, 0, 0, 0, TORCH)
        while not q.empty():
            time, x, y, item = q.get()
            cur_type = terrain(x, y)
            if x == target_x and y == target_y:
                if item == TORCH:
                    return time
                q.equip(TORCH)
                continue
            for n_x, n_y in aoc.t_neighbors4((x, y)):
                if n_x < 0 or n_y < 0:
                    continue
                n_type = terrain(n_x, n_y)
                if item == INVALID[n_type]:
                    q.equip(MUTUAL_VALID[cur_type, n_type])
                else:
                    q.move(n_x, n_y)
        raise RuntimeError("Not solved")

# vim:expandtab:sw=4:ts=4
