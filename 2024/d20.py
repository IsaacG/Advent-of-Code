#!/bin/python
"""Advent of Code, Day 20: Race Condition."""
from __future__ import annotations

import collections
import functools
import queue
import itertools
import math
import re

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

LineType = int
InputType = list[LineType]


class Day20(aoc.Challenge):
    """Day 20: Race Condition."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=5),
        aoc.TestCase(part=2, inputs=SAMPLE, want=41),
    ]

    def part1(self, puzzle_input: InputType) -> int:
        spaces = puzzle_input["."] | puzzle_input["E"] | puzzle_input["S"]
        start = puzzle_input["S"].pop()
        end = puzzle_input["E"].pop()

        todo = queue.PriorityQueue()
        todo.put((0, start.real, start.imag))
        seen = {start}
        distance_from_start = {}

        while not todo.empty():
            cost, pos_x, pos_y = todo.get()
            pos = complex(pos_x, pos_y)
            assert pos not in distance_from_start
            distance_from_start[pos] = cost

            if pos == end:
                print("End", pos, cost)
                base_cost = cost
            for n in aoc.neighbors(pos):
                if n not in seen and n in spaces:
                    seen.add(n)
                    todo.put((cost + 1, n.real, n.imag))

        todo = queue.PriorityQueue()
        todo.put((0, end.real, end.imag))
        seen = {end}
        distance_from_end = {}

        while not todo.empty():
            cost, pos_x, pos_y = todo.get()
            pos = complex(pos_x, pos_y)
            assert pos not in distance_from_end
            distance_from_end[pos] = cost

            if pos == start:
                print("End", pos, cost)
                assert base_cost == cost
            for n in aoc.neighbors(pos):
                if n not in seen and n in spaces:
                    seen.add(n)
                    todo.put((cost + 1, n.real, n.imag))

        offsets = {m for n in aoc.neighbors(complex(0)) for m in aoc.neighbors(n)}
        # offsets = {o for n in aoc.neighbors(complex(0)) for m in aoc.neighbors(n) for o in aoc.neighbors(m)}
        offsets = {sum(i) for i in itertools.product(aoc.FOUR_DIRECTIONS, repeat=2)}
        offsets = {p: int(abs(p.real) + abs(p.imag)) for p in offsets}
        
        gotcosts = set()
        for cheat_from in spaces:
            for n in aoc.neighbors(cheat_from):
                if n in spaces:
                    total = distance_from_start[cheat_from] + distance_from_end[n] + 1
                    gotcosts.add(total)
        m = min(gotcosts)
        assert m == base_cost, f"{m}, {base_cost}"

        threshold = 15 if self.testing else 100
        cheats = set()
        saves = []
        for cheat_from in spaces:
            for cheat_delta, cheat_cost in offsets.items():
                cheat_to = cheat_from + cheat_delta
                if cheat_to in spaces:
                    total = distance_from_start[cheat_from] + distance_from_end[cheat_to] + cheat_cost
                    if base_cost - total >= threshold:
                        cheats.add((cheat_from, cheat_to))
                    if base_cost > total:
                        saves.append(base_cost - total)

        # print(cheats_val)
        print(dict(sorted(collections.Counter(saves).items())))
        got = len(cheats)
        assert got != 1382
        return got

    def part2(self, puzzle_input: InputType) -> int:
        spaces = puzzle_input["."] | puzzle_input["E"] | puzzle_input["S"]
        start = puzzle_input["S"].pop()
        end = puzzle_input["E"].pop()

        todo = queue.PriorityQueue()
        todo.put((0, start.real, start.imag))
        seen = {start}
        distance_from_start = {}

        while not todo.empty():
            cost, pos_x, pos_y = todo.get()
            pos = complex(pos_x, pos_y)
            assert pos not in distance_from_start
            distance_from_start[pos] = cost

            if pos == end:
                print("End", pos, cost)
                base_cost = cost
            for n in aoc.neighbors(pos):
                if n not in seen and n in spaces:
                    seen.add(n)
                    todo.put((cost + 1, n.real, n.imag))

        todo = queue.PriorityQueue()
        todo.put((0, end.real, end.imag))
        seen = {end}
        distance_from_end = {}

        while not todo.empty():
            cost, pos_x, pos_y = todo.get()
            pos = complex(pos_x, pos_y)
            assert pos not in distance_from_end
            distance_from_end[pos] = cost

            if pos == start:
                print("End", pos, cost)
                assert base_cost == cost
            for n in aoc.neighbors(pos):
                if n not in seen and n in spaces:
                    seen.add(n)
                    todo.put((cost + 1, n.real, n.imag))

        print("Compute offset")
        offsets = {}
        for x in range(-20, 21):
            for y in range(-20, 21):
                c = abs(x) + abs(y)
                if abs(x) + abs(y) <= 20:
                    offsets[complex(x, y)] = c
        print("Got offsets", len(offsets))

        if False:
            offsets = {sum(i) for i in itertools.product(aoc.FOUR_DIRECTIONS, repeat=20)}
            # offsets = {o for n in aoc.neighbors(complex(0)) for m in aoc.neighbors(n) for o in aoc.neighbors(m)}
            offsets = {p: int(abs(p.real) + abs(p.imag)) for p in offsets}
            offsets = {a: b for a, b in offsets.items() if b == 20}
        
        gotcosts = set()
        for cheat_from in spaces:
            for n in aoc.neighbors(cheat_from):
                if n in spaces:
                    total = distance_from_start[cheat_from] + distance_from_end[n] + 1
                    gotcosts.add(total)
        m = min(gotcosts)
        assert m == base_cost, f"{m}, {base_cost}"

        threshold = 70 if self.testing else 100
        cheats = set()
        saves = []
        for cheat_from in spaces:
            for cheat_delta, cheat_cost in offsets.items():
                cheat_to = cheat_from + cheat_delta
                if cheat_to in spaces:
                    total = distance_from_start[cheat_from] + distance_from_end[cheat_to] + cheat_cost
                    if base_cost - total >= threshold:
                        cheats.add((cheat_from, cheat_to))
                    if base_cost > total:
                        saves.append(base_cost - total)

        # print(cheats_val)
        print(dict(sorted(collections.Counter(saves).items())))
        got = len(cheats)
        assert got != 1382
        return got

    def not_part_1(self, puzzle_input: InputType) -> int:
        spaces = puzzle_input["."] | puzzle_input["E"]
        start = puzzle_input["S"].pop()
        end = puzzle_input["E"].pop()
        todo = queue.PriorityQueue()
        todo.put((0, start.real, start.imag))
        seen = {start}
        while not todo.empty():
            cost, pos_x, pos_y = todo.get()
            pos = complex(pos_x, pos_y)
            if pos == end:
                print("End", pos, cost)
                break
            for n in aoc.neighbors(pos):
                if n not in seen and n in spaces:
                    seen.add(n)
                    todo.put((cost + 1, n.real, n.imag))
        base_cost = cost

        offsets = {o for n in aoc.neighbors(complex(0)) for m in aoc.neighbors(n) for o in aoc.neighbors(m)}
        offsets = {m for n in aoc.neighbors(complex(0)) for m in aoc.neighbors(n)}
        offsets = {p: int(abs(p.real) + abs(p.imag)) for p in offsets}
        cheats = set()
        good_cheats = set()

        threshold = 15 if self.testing else 100
        todo = queue.PriorityQueue()
        no_cheat = (-1, -1, -1, -1)
        todo.put((0, 0, start.real, start.imag, no_cheat))
        seen = {(start, no_cheat)}

        def score(pos):
            return int(abs(end.real - pos.real) + abs(end.imag - pos.imag))

        while not todo.empty():
            rank, cost, pos_x, pos_y, cheated = todo.get()
            if cheated != no_cheat and cheated in cheats:
                continue
            pos = complex(pos_x, pos_y)
            if pos == end:
                if cheated != no_cheat:
                    cheats.add(cheated)
                    # print("Got to the end with cheat,", cheated, base_cost - cost)
                if base_cost - cost > threshold:
                    assert cheated != no_cheat
                    good_cheats.add((cheated, base_cost - cost))
            for n in aoc.neighbors(pos):
                if (n, cheated) not in seen and n in spaces:
                    seen.add((n, cheated))
                    todo.put((score(n) + cost, cost + 1, n.real, n.imag, cheated))
            if cheated == no_cheat:
                for d, c in offsets.items():
                    n = pos + d
                    cheated = pos.real, pos.imag, n.real, n.imag
                    if (n, cheated) not in seen and n in spaces:
                        seen.add((n, cheated))
                        todo.put((score(n) + cost, cost + c, n.real, n.imag, cheated))

        # print(cheats)
        print({a: b for a, b in good_cheats if b > 20})
        return len(good_cheats)


    # def solver(self, puzzle_input: InputType, part_one: bool) -> int | str:


# vim:expandtab:sw=4:ts=4
