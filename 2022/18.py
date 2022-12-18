#!/bin/python
"""Advent of Code, Day 18: Boiling Boulders."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

import typer
from lib import aoc

SAMPLE = ["1,1,1\n2,1,1",
    """\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5""",
]

LineType = int
InputType = list[LineType]


class Day18(aoc.Challenge):
    """Day 18: Boiling Boulders."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=10),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=64),
        aoc.TestCase(inputs=SAMPLE[1], part=2, want=58),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_re_findall_int(r"\d+")

    def part1(self, parsed_input: InputType) -> int:
        points = {tuple(i) for i in parsed_input}
        total = 0
        for x, y, z in points:
            for a, b, c in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
                p2 = (x + a, y + b, z + c)
                if p2 not in points:
                    total += 1
        return total
        while points:
            point = points.pop(0)
            x, y, z = point
            group = {point,}
            todo = {point,}
            while todo:
                p1 = todo.pop()
                move = []
                for p2 in points:
                    if sum(abs(i - j) for i, j in zip(p1, p2)) == 1:
                        move.append(p2)
                for p2 in move:
                    todo.add(p2)
                    group.add(p2)
                    points.remove(p2)
            for p1 in group:
                for a, b, c in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
                    p2 = (x + a, y + b, z + c)
            groups.append(group)

    def part2(self, parsed_input: InputType) -> int:
        points = list(sorted(tuple(i) for i in parsed_input))
        bounds = []
        for i in range(3):
            bounds.append((min(p[i] for p in points) - 1, max(p[i] for p in points) + 1))

        todo = {tuple(bounds[i][0] for i in range(3))}
        area = set()
        total = 0
        step = 0
        while todo:
            step += 1
            p1 = todo.pop()
            # if step % 10000 == 0:
                # print(step, p1)
            x, y, z = p1
            for a, b, c in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
                p2 = (x + a, y + b, z + c)
                if not all(
                    bounds[i][0] <= p2[i] <= bounds[i][1]
                    for i in range(3)
                ):
                    continue
                if p2 in area:
                    continue
                if p2 in points:
                    total += 1
                    continue
                area.add(p2)
                todo.add(p2)
        return total




        surfaces = set()
        for x, y, z in points:
            for a, b, c in itertools.product([-1, 0, 1], repeat=3):
                p2 = (x + a, y + b, z + c)
                if p2 not in points:
                    surfaces.add(p2)


        interiors = set()
        surface_groups = self.points_to_groups(surfaces)
        for sg in surface_groups:
            if all(
                min(p[i] for p in sg) >= bounds[i][0]
                and max(p[i] for p in sg) <= bounds[i][1]
                for i in range(3)
            ):
                interior.update(sg)
                print(group)
                print("Interior:", sg)

        total = 0
        for group in groups:
            print(f"{len(surface_groups)=} {(2,2,5) in surface_groups[0]}")
            print(group)
            interior = set()

            for x, y, z in group:
                total += 6
                for a, b, c in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
                    if (x + a, y + b, z + c) in group or (x + a, y + b, z + c) in interior:
                        total -= 1


        assert total != 13370
        return total

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

    # def line_parser(self, line: str):
    #     pass


if __name__ == "__main__":
    typer.run(Day18().run)

# vim:expandtab:sw=4:ts=4
