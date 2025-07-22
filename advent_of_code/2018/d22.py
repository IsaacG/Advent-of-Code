#!/bin/python
"""Advent of Code, Day 22: Mode Maze."""
from __future__ import annotations

import collections
import functools
import itertools
import logging
import math
import queue
import re

from lib import aoc


def log(*args, **kwargs) -> None:
    logging.info(*args, **kwargs)

class PriorityOnceQ(queue.PriorityQueue):

    def __init__(self, target_x, target_y):
        self.target_x = target_x
        self.target_y = target_y
        self.seen = {}
        return super().__init__()

    def put(self, delay, old_time, x, y, item):
        # Only add once
        new_time = old_time + delay
        fp = (x, y, item)
        if fp in self.seen and self.seen[fp] <= new_time:
            return
        self.seen[fp] = new_time

        rank = new_time + abs(self.target_x - x) + abs(self.target_y - y)
        super().put((rank, new_time, x, y, item))

    def get(self):
        self.got = super().get()[1:]
        return self.got

    def equip(self, item):
        assert item != self.got[-1]
        self.put(7, *self.got[:-1], item)

    def move(self, x, y):
        self.put(1, self.got[0], x, y, self.got[-1])


class Day22(aoc.Challenge):
    """Day 22: Mode Maze."""

    TESTS = [
        aoc.TestCase(part=1, inputs="depth: 510\n target: 10,10", want=114),
        aoc.TestCase(part=2, inputs="depth: 510\n target: 10,10", want=45),
    ]
    INPUT_PARSER = aoc.parse_ints

    def solver(self, puzzle_input: list[list[int]], part_one: bool) -> int:
        (depth,), (target_x, target_y) = puzzle_input

        @functools.cache
        def geo_idx(x, y):
            if x == target_x and y == target_y:
                return 0
            if x == 0:
                return y * 48271
            if y == 0:
                return x * 16807
            return erosion(x - 1, y) * erosion(x, y - 1)

        @functools.cache
        def erosion(x, y):
            return (geo_idx(x, y) + depth) % 20183

        @functools.cache
        def terrain(x, y):
            return erosion(x, y) % 3

        if part_one:
            got = sum(terrain(x, y) for x in range(target_x + 1) for y in range(target_y + 1))
            if not self.testing:
                assert got == 7299
            return got

        CLIMBING, TORCH, NEITHER = range(3)
        names = ["Climbing", "Torch", "Neither"]
        ITEMS = {CLIMBING, TORCH, NEITHER}
        INVALID = [NEITHER, TORCH, CLIMBING]
        VALID = [ITEMS - {i} for i in INVALID]
        MUTUAL_VALID = {
            (a, b): (VALID[a] & VALID[b]).pop()
            for a in range(3)
            for b in range(3)
            if a != b
        }

        # backtrack = {}
        q = PriorityOnceQ(target_x, target_y)
        q.put(0, 0, 0, 0, TORCH)
        while not q.empty():
            time, x, y, item = q.get()
            cur_type = terrain(x, y)
            if x == target_x and y == target_y:
                if item == TORCH:
                    if not self.testing:
                        assert time < 1018, time
                    break
                else:
                    q.equip(TORCH)
                    # backtrack[time + 7, x, y, TORCH] = (time, x, y, item, f"Equip {names[TORCH]}")
                    continue
            for n_x, n_y in aoc.t_neighbors4((x, y)):
                if n_x < 0 or n_y < 0:
                    continue
                n_type = terrain(n_x, n_y)
                if item == INVALID[n_type]:
                    n_item = MUTUAL_VALID[cur_type, n_type]
                    q.equip(n_item)
                    # backtrack[time + 7, x, y, n_item] = (time, x, y, item, f"Equip {names[n_item]}")
                else:
                    q.move(n_x, n_y)
                    # backtrack[time + 1, n_x, n_y, item] = (time, x, y, item, f"Move {(x, y)} to {(n_x, n_y)}")

        if False:
            trail = []
            t, x, y, i = time, x, y, item
            while x or y:
                a, b, c, d, e = backtrack[t, x, y, i]
                trail.append(e)
                t, x, y, i = a, b, c, d
            print("\n".join(reversed(trail)))

        return time


# vim:expandtab:sw=4:ts=4
