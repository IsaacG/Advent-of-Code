#!/bin/python
"""Advent of Code, Day 12: Garden Groups."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
AAAA
BBCD
BBCC
EEEC""",  # 0
    """\
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO""",  # 25
    """\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE""",  # 52
    """\
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE""",
    """\
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""
]

LineType = int
InputType = list[LineType]


class Day12(aoc.Challenge):
    """Day 12: Garden Groups."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=140),
        aoc.TestCase(part=1, inputs=SAMPLE[1], want=772),
        aoc.TestCase(part=1, inputs=SAMPLE[2], want=1930),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=80),
        aoc.TestCase(part=2, inputs=SAMPLE[3], want=236),
        aoc.TestCase(part=2, inputs=SAMPLE[4], want=368),
        aoc.TestCase(part=1, inputs=SAMPLE[2], want=1206),
    ]

    def part1(self, puzzle_input: InputType) -> int:
        regions = []
        coords = set(puzzle_input.chars)
        while coords:
            cur = coords.pop()
            todo = {cur}
            region = {cur}
            val = puzzle_input[cur]
            seen = {cur}
            while todo:
                cur = todo.pop()
                coords.discard(cur)
                region.add(cur)
                for n in aoc.neighbors(cur):
                    if n in seen:
                        continue
                    seen.add(n)
                    if puzzle_input.chars.get(n) == val:
                        region.add(n)
                        todo.add(n)
            regions.append((val, region))
                
        cost = 0
        for v, r in regions:
            area = len(r)
            perimeter = 0
            for cur in r:
                for n in aoc.neighbors(cur):
                    if n not in r:
                        perimeter += 1
            cost += area * perimeter
        return cost


    def part2(self, puzzle_input: InputType) -> int:
        regions = []
        coords = set(puzzle_input.chars)
        while coords:
            cur = coords.pop()
            todo = {cur}
            region = {cur}
            val = puzzle_input[cur]
            seen = {cur}
            while todo:
                cur = todo.pop()
                coords.discard(cur)
                region.add(cur)
                for n in aoc.neighbors(cur):
                    if n in seen:
                        continue
                    seen.add(n)
                    if puzzle_input.chars.get(n) == val:
                        region.add(n)
                        todo.add(n)
            regions.append((val, region))
                
        cost = 0
        for v, region in regions:
            area = len(region)
            # self.tprint(v, region)
            if area == 1:
                perimeter = 4
                cost += area * perimeter
                self.tprint(f"{v}: {area, perimeter=} => {cost}")
                continue

            unwalked_walls = {r for r in region if any(n not in region for n in aoc.neighbors(r))}
            while unwalked_walls:
                cur = next(r for r in unwalked_walls if any(n not in region for n in aoc.neighbors(r)))
                unwalked_walls.remove(cur)
                direction = next(d for d in aoc.FOUR_DIRECTIONS if cur + d not in region)
                while cur + direction not in region:
                    direction *= -1j
                assert cur + direction in region
                assert cur + direction * 1j not in region
                start_pos = cur
                start_dir = direction
                self.DEBUG = start_pos==(1+2j) and start_dir==(1-0j)
                self.tprint(f"Start {v} @ {start_pos=}, {start_dir=}")
                self.tprint(f"Start {v} w unwalked {unwalked_walls}")

                perimeter = 0
                while cur != start_pos or direction != start_dir or perimeter < 1:
                    unwalked_walls.discard(cur)
                    if perimeter > 100:
                        raise Exception
                    if cur + direction * 1j in region:
                        direction *= 1j
                        self.tprint(f"Able to turn, so turning => {direction}")
                        perimeter += 1
                        assert cur + direction in region
                    while cur + direction not in region:
                        self.tprint(f"Hit a wall. Turn: {direction} -> {direction * -1j}")
                        direction *= -1j
                        perimeter += 1
                    if cur == start_pos and direction == start_dir and perimeter:
                        break
                    if cur + direction in region:
                        self.tprint(f"Step: {cur} + {direction} => {cur + direction}; {perimeter=}")
                        cur += direction
                        unwalked_walls.discard(cur)
                        self.tprint(f"Step => {cur}")
                cost += area * perimeter
                self.tprint(f"{v}: {area, perimeter=} => {cost}")
        return cost

    # def solver(self, puzzle_input: InputType, part_one: bool) -> int | str:

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return super().input_parser(puzzle_input)
        return puzzle_input.splitlines()
        return puzzle_input
        return [int(i) for i in puzzle_input.splitlines()]
        mutate = lambda x: (x[0], int(x[1])) 
        return [mutate(line.split()) for line in puzzle_input.splitlines()]
        # Words: mixed str and int
        return [
            tuple(
                int(i) if i.isdigit() else i
                for i in line.split()
            )
            for line in puzzle_input.splitlines()
        ]
        # Regex splitting
        patt = re.compile(r"(.*) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.")
        return [
            tuple(
                int(i) if i.isdigit() else i
                for i in patt.match(line).groups()
            )
            for line in puzzle_input.splitlines()
        ]

# vim:expandtab:sw=4:ts=4
