#!/bin/python
"""Advent of Code: Day 20."""

import collections
import functools
import math
import re
import textwrap

import typer
from lib import aoc

SAMPLE = ["""
##.##.#..###....##..##.#.##...#..#..##.####..##...###.....##.####.##.##.##...####.######..#.###.#.##..###.#..#####...#.##.#..#.#.#..######..###.##.#..##.#..##..##..#...###.##..####.#..#....#####.#.###..##.....#...#.##.#####.###.###....#.#..###.##.##.#..##.##.#.##..##.##.##..###.#.#....#.##..###.###.#.##......#.##..#..#.#...##.##.....###...#..#...###..##.####..#..##..#.#..###......#.#####....#####..###..####...###.#.####..#.##..#.#####..##...##.#.#.#...##.#...#.##.##..#.#.##....##.####.#.#..#.##.#.#..#..#.#.

#

""","""
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
""","""
#..............................................................................................#................................................................................................................................................................#...............................................................................................................................................................................................................................................................

#
"""]
InputType = list[int]


class Day20(aoc.Challenge):

    DEBUG = True
    SUBMIT = {1: True, 2: False}

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[2], part=1, want=1),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=35),
        # aoc.TestCase(inputs=SAMPLE[1], part=2, want=0),
    )

    def neighbors(self, point):
        px, py = point
        return [(px + x, py + y) for y in (-1, 0, 1) for x in (-1, 0, 1)]

    def show(self, board):
        min_x, max_x = int(min(p.real for p in board)), int(max(p.real for p in board))
        min_y, max_y = int(min(p.imag for p in board)), int(max(p.imag for p in board))
        for y in range(min_y, max_y+1):
            line = ""
            for x in range(min_x, max_x+1):
                line += "#" if complex(x,y) in board else "."
            print(line)
        print()
        
    def show_c(self, board):
        min_x, max_x = min(x for x, y in board), max(x for x, y in board)
        min_y, max_y = min(y for x, y in board), max(y for x, y in board)
        for y in range(min_y, max_y+1):
            line = ""
            for x in range(min_x, max_x+1):
                line += "#" if board[(x,y)] else "."
            print(line)
        
    def part1(self, parsed_input: InputType) -> int:
        algo, board = parsed_input
        setboard = set(complex(x, y) for (x, y), val in board.items() if val)
        return self.part1_set(algo, setboard)
        # return self.part1_box(algo, board)

    def part1_box(self, algo, board) -> int:
        ones = int("1" * 9, 2)
        min_xy = 0
        max_x = max(x for x, y in board)
        max_y = max(y for x, y in board)
        blink = algo[0] and not algo[ones]

        neighbors = lambda x, y: [(x + xstep, y + ystep) for ystep in range(-1, 2) for xstep in range(-1, 2)]

        for step in range(2):
            print("Step", step)
            is_on = board.copy()
            background = blink and bool(step % 2)
            # Add a ring of False to the board.
            for x in range(min_xy - 1, max_x + 2):
                is_on[(x, min_xy - 1)] = False
                is_on[(x, max_y + 1)] = False
            for y in range(min_xy - 1, max_y + 2):
                is_on[(min_xy - 1, y)] = False
                is_on[(min_xy + 1, y)] = False
            # For the new board, consider all points in the old board plus one wider
            print("is_on")
            self.show_c(is_on)
            new_points = list(is_on.keys())
            # Add a ring of Background to the board, two spaces out.
            for x in range(min_xy - 2, max_x + 3):
                is_on[(x, min_xy - 2)] = background
                is_on[(x, max_y + 2)] = background
            for y in range(min_xy - 2, max_y + 3):
                is_on[(min_xy - 2, y)] = background
                is_on[(min_xy + 2, y)] = background

            print("is_on")
            self.show_c(is_on)

            new_board = {}
            for point in new_points:
                bits = [is_on[p] for p in neighbors(*point)]
                addr = "".join("1" if b else "0" for b in bits)
                res = algo[int(addr, 2)]
                new_board[point] = res
            board = new_board

            min_xy -= 1
            max_x += 1
            max_y += 1

        return sum(1 for v in board.values() if v)
        
    def part1_set(self, algo: list[bool], board: set[complex]) -> int:
        # Return the 3x3 points centered around `point`.
        area3x3 = lambda point: [point + complex(x, y) for y in range(-1, 2) for x in range(-1, 2)]
        # Blink if 000_000_000 => on and 111_111_111 => off
        blink = algo[0] and not algo[int("1" * 9, 2)]
        trans = {True: "1", False: "0"}

        candidate_points = set()
        for step in range(50):
            explored = candidate_points
            # Expand each on-point (and maybe explored) to all neighbors.
            candidate_points = set().union(*(set(area3x3(point)) for point in (board | explored)))

            def bitstring(point):
                bits = [(blink and step % 2 and p not in explored) or p in board for p in area3x3(point)]
                return "".join(trans[b] for b in bits)

            board = set(
                point
                for point in candidate_points
                if algo[int(bitstring(point), 2)]
            )

        return len(board)

    def part1b(self, parsed_input: InputType) -> int:
        algo, board = parsed_input
        ones = int("1" * 9, 2)
        print(f"{algo[0]=} {algo[ones]=}")

        if algo[0] and not algo[ones]:
            print("Blinking")
            defaults = [True, False]
        else:
            print("No blinking")
            defaults = [False, False]

        def is_alive(point, board, default):
            loc = ""
            for p in self.neighbors(point):
                if board.get(p, default):
                    loc += "1"
                else:
                    loc += "0"
            loc = int(loc, 2)
            return algo[loc]

        for step in range(3):
            self.show(board)
            min_x, max_x = min(x for x, y in board), max(x for x, y in board)
            min_y, max_y = min(y for x, y in board), max(y for x, y in board)

            default = defaults[step % 2]
            print(f"{default=}")
            print(-min_x - 1, max_x + 2)
            print(-min_y -1, max_y + 2)

            new_board = {}
            for x in range(-min_x - 1, max_x + 2):
                for y in range(-min_y -1, max_y + 2):
                    p = (x,y)
                    new_board[p] = is_alive(p, board, default)
            board = new_board
            
        print(f"{len(board)=}")
        self.show(board)
        return sum(1 for i in board.values() if i)

    def part1c(self, parsed_input: InputType) -> int:
        global bg, img, alg
        alg, img = parsed_input
        print(sum(img.values()))
        iter()
        print(sum(img.values()))
        iter()
        print(sum(img.values()))


    def part1d(self, parsed_input: InputType) -> int:
        algo, board = parsed_input
        board = set(complex(x, y) for (x, y), val in board.items() if val)

        ones = int("1" * 9, 2)
        print(f"{algo[0]=} {algo[ones]=}")

        neighbors = lambda point: [point + complex(x, y) for y in range(-1, 2) for x in range(-1, 2)]

        def to_bits(point, board, min_x, max_x, min_y, max_y, default):
            loc = ""
            for p in neighbors(point):
                if p in board:
                    loc += "1"
                elif min_x < p.real < max_x and min_y < p.imag < max_y:
                    loc += "0"
                else:
                    loc += "1" if default else "0"
            return loc

        if algo[0] and not algo[ones]:
            blink = True
        else:
            blink = False

        default = False

        for step in range(2):
            candidate_points = set().union(*(set(neighbors(point)) for point in board))

            min_x, max_x = min(p.real for p in board) - 1, max(p.real for p in board) + 1
            min_y, max_y = min(p.imag for p in board) - 1, max(p.imag for p in board) + 1

            new_board = set()
            for point in candidate_points:
                if algo[int(to_bits(point, board, min_x, max_x, min_y, max_y, default), 2)]:
                    new_board.add(point)
            board = new_board
            if blink:
                default = not default
        return len(board)


    def part2(self, parsed_input: InputType) -> int:
        return -1

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        algo, board = puzzle_input.split("\n\n")
        algo = [i == "#" for i in algo]

        gameboard = {}
        for y, line in enumerate(board.splitlines()):
            for x, elem in enumerate(line):
                gameboard[(x,y)] = elem == "#"
        return algo, gameboard
        # return algo, {pos for pos, val in gameboard.items() if val}


if __name__ == "__main__":
    typer.run(Day20().run)

# vim:expandtab:sw=4:ts=4
