#!/bin/python
"""Advent of Code, Day 21: Step Counter."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = """\
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""

InputType = tuple[set[complex], set[complex], set[complex]]


class Day21(aoc.Challenge):
    """Day 21: Step Counter."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=16),
        aoc.TestCase(inputs=SAMPLE, part=2, want=aoc.TEST_SKIP),
    ]

    def count(self, start, garden, steps):
        reach = start.copy()
        for s in range(steps):
            n = set()
            for p in reach:
                n.update(aoc.neighbors(p))
            reach = n & garden
        return len(reach)

    def walk(self, start, garden, rocks, steps):
        reach = start.copy()
        min_x, min_y, max_x, max_y = aoc.bounding_coords(garden)
        max_x += 1
        max_y += 1
        for s in range(steps):
            new = set()
            for p in reach:
                for n in aoc.neighbors(p):
                    if complex(n.real % max_x, n.imag % max_y) not in rocks:
                        new.add(n)
            reach = new
        return reach

    def part1(self, parsed_input: InputType) -> int:
        start, garden, _ = parsed_input
        steps = 64
        if self.testing:
            steps = 6
        return self.count(start, garden, steps)

    def test_p2(self, parsed_input: InputType) -> int:
        steps_count = [(6, 16), (10, 50), (50, 1594), (100, 6536)]
        steps_count = [(6, 16), (10, 50)]

        start, garden, rocks = self.input_parser(SAMPLE)
        for steps, want in steps_count:
            got = len(self.walk(start, garden, rocks, steps))
            assert got == want, f"{(steps, want, got)=}"

    def part2(self, parsed_input: InputType) -> int:
        start, garden, rocks = parsed_input
        start_p = list(start)[0]
        steps = 26501365

        min_x, min_y, max_x, max_y = aoc.bounding_coords(garden)
        print(f"{(min_x, min_y, max_x, max_y)=}")
        size = max_x - min_x + 1
        assert start_p.real == start_p.imag == max_x // 2
        half_size = int(start_p.real)

        assert (steps - half_size) % size == 0
        expansions = (steps - half_size) // size
        print(f"{(size, expansions)=}")

        interior_center_count = 1
        for i in range(2, expansions, 2):
            interior_center_count += i * 4

        interior_even_count = 0
        for i in range(0, expansions, 2):
            interior_even_count += (1 + i) * 4

        points = 5756 + 5764 + 5747 + 5755
        short_diag = 964 + 965 + 984 + 964
        large_diag = 6698 + 6703 + 6690 + 6694

        interior_center = 7637
        interior_even = 7650

        total = points + expansions * short_diag + (expansions - 1) * large_diag + interior_center * interior_center_count + interior_even * interior_even_count
        assert total >  552145547650224, total
        assert total >  552145547653987, total
        assert total != 626154626157772, total
        assert total != 625090573877572, total
        assert total != 626160044736474, total
        assert total != 625095992456274, total
        return total

        reach = start.copy()
        for i in range(7):
            for s in range(size if i else half_size):
                new = set()
                for p in reach:
                    for n in aoc.neighbors(p):
                        if complex(n.real % size, n.imag % size) not in rocks:
                            new.add(n)
                reach = new

            print("Expansion", i)
            rows = []
            for y in range(-i, i + 1):
                row = []
                top = size * y
                bottom = top + size
                for x in range(-i, i + 1):
                    left = size * x
                    right = left + size
                    num = len({p for p in reach if left <= p.real < right and top <= p.imag < bottom})
                    row.append(num)
                rows.append(row)
                print(" | ".join(f"{r:5}" for r in row))
            print(sorted(collections.Counter(r for row in rows for r in row).items()))
            print()

        print(rows)

        return


        circle = self.walk(start, garden, rocks, half_size + size + size)

        edges = {
            "C":   len({p for p in circle if    0 <= p.imag <  131 and    0 <= p.real <  131}),
            "LL":  len({p for p in circle if    0 <= p.imag <  131 and -262 <= p.real < -131}),
            "RR":  len({p for p in circle if    0 <= p.imag <  131 and  262 <= p.real <  393}),
            "UU":  len({p for p in circle if -262 <= p.imag < -131 and    0 <= p.real <  131}),
            "DD":  len({p for p in circle if  262 <= p.imag <  393 and    0 <= p.real <  131}),
            "UL":  len({p for p in circle if -131 <= p.imag <    0 and -131 <= p.real <    0}),
            "UR":  len({p for p in circle if -131 <= p.imag <    0 and  131 <= p.real <  262}),
            "DL":  len({p for p in circle if  131 <= p.imag <  262 and -131 <= p.real <    0}),
            "DR":  len({p for p in circle if  131 <= p.imag <  262 and  131 <= p.real <  262}),
            "UUL": len({p for p in circle if -262 <= p.imag < -131 and -131 <= p.real <    0}),
            "ULL": len({p for p in circle if -131 <= p.imag <    0 and -262 <= p.real < -131}),
            "DDL": len({p for p in circle if  262 <= p.imag <  393 and -131 <= p.real <    0}),
            "DLL": len({p for p in circle if  131 <= p.imag <  262 and -262 <= p.real < -131}),
            "UUR": len({p for p in circle if -262 <= p.imag < -131 and  131 <= p.real <  262}),
            "URR": len({p for p in circle if -131 <= p.imag <    0 and  262 <= p.real <  393}),
            "DDR": len({p for p in circle if  262 <= p.imag <  393 and  131 <= p.real <  262}),
            "DRR": len({p for p in circle if  131 <= p.imag <  262 and  262 <= p.real <  393}),
        }
        print(f"{edges=}")
        assert all(edges[a] == edges[b] for a, b in [("UUL", "ULL"), ("DDL", "DLL"), ("UUR", "URR"), ("DDR", "DRR")])

        a, b = self.count(start, garden, size), self.count(start, garden, size + 1)
        print(f"{(a, b)=}")

        points = sum(edges[i] for i in ["LL", "RR", "UU", "DD"])
        diag_short = expansions * sum(edges[i] for i in ["UUR", "UUL", "DDR", "DDL"])
        diag_long = (expansions - 1) * sum(edges[i] for i in ["UR", "UL", "DR", "DL"])
        full_count = sum(i * 4 for i in range(expansions))
        full = b * full_count
        total = points + diag_short + diag_long + edges["C"] + full 

        assert total >  552145547650224, total
        assert total >  552145547653987, total
        assert total != 626154626157772, total
        assert total != 625090573877572, total
        assert total != 626160044736474, total
        assert total != 625095992456274, total
        return total

    def part2a(self, parsed_input: InputType) -> int:
        self.test_p2(parsed_input)

        start, garden, rocks = parsed_input
        start_p = list(start)[0]
        steps = 26501365

        min_x, min_y, max_x, max_y = aoc.bounding_coords(garden)
        print(f"{(min_x, min_y, max_x, max_y)=}")
        size = max_x - min_x + 1
        assert start_p.real == start_p.imag == max_x // 2
        half_size = int(start_p.real)

        assert (steps - half_size) % size == 0
        expansions = (steps - half_size) // size
        print(f"{(size, expansions)=}")

        circle = self.walk(start, garden, rocks, half_size + size + size)

        edges = {
            "C":   len({p for p in circle if    0 <= p.imag <  131 and    0 <= p.real <  131}),
            "LL":  len({p for p in circle if    0 <= p.imag <  131 and -262 <= p.real < -131}),
            "RR":  len({p for p in circle if    0 <= p.imag <  131 and  262 <= p.real <  393}),
            "UU":  len({p for p in circle if -262 <= p.imag < -131 and    0 <= p.real <  131}),
            "DD":  len({p for p in circle if  262 <= p.imag <  393 and    0 <= p.real <  131}),
            "UL":  len({p for p in circle if -131 <= p.imag <    0 and -131 <= p.real <    0}),
            "UR":  len({p for p in circle if -131 <= p.imag <    0 and  131 <= p.real <  262}),
            "DL":  len({p for p in circle if  131 <= p.imag <  262 and -131 <= p.real <    0}),
            "DR":  len({p for p in circle if  131 <= p.imag <  262 and  131 <= p.real <  262}),
            "UUL": len({p for p in circle if -262 <= p.imag < -131 and -131 <= p.real <    0}),
            "ULL": len({p for p in circle if -131 <= p.imag <    0 and -262 <= p.real < -131}),
            "DDL": len({p for p in circle if  262 <= p.imag <  393 and -131 <= p.real <    0}),
            "DLL": len({p for p in circle if  131 <= p.imag <  262 and -262 <= p.real < -131}),
            "UUR": len({p for p in circle if -262 <= p.imag < -131 and  131 <= p.real <  262}),
            "URR": len({p for p in circle if -131 <= p.imag <    0 and  262 <= p.real <  393}),
            "DDR": len({p for p in circle if  262 <= p.imag <  393 and  131 <= p.real <  262}),
            "DRR": len({p for p in circle if  131 <= p.imag <  262 and  262 <= p.real <  393}),
        }
        print(f"{edges=}")
        assert all(edges[a] == edges[b] for a, b in [("UUL", "ULL"), ("DDL", "DLL"), ("UUR", "URR"), ("DDR", "DRR")])

        a, b = self.count(start, garden, size), self.count(start, garden, size + 1)
        print(f"{(a, b)=}")

        points = sum(edges[i] for i in ["LL", "RR", "UU", "DD"])
        diag_short = expansions * sum(edges[i] for i in ["UUR", "UUL", "DDR", "DDL"])
        diag_long = (expansions - 1) * sum(edges[i] for i in ["UR", "UL", "DR", "DL"])
        full_count = sum(i * 4 for i in range(expansions))
        full = b * full_count
        total = points + diag_short + diag_long + edges["C"] + full 

        assert total >  552145547650224, total
        assert total >  552145547653987, total
        assert total != 626154626157772, total
        assert total != 625090573877572, total
        assert total != 626160044736474, total
        assert total != 625095992456274, total
        return total

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        start = aoc.parse_ascii_bool_map("S").parse(puzzle_input)
        garden = aoc.parse_ascii_bool_map(".").parse(puzzle_input) | start
        rocks = aoc.parse_ascii_bool_map("#").parse(puzzle_input)
        return start, garden, rocks

# vim:expandtab:sw=4:ts=4
