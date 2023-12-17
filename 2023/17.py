#!/bin/python
"""Advent of Code, Day 17: Clumsy Crucible."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import queue
import re

from lib import aoc

SAMPLE = [
    """\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533""",  # 0
    """\
111111111111
999999999991
999999999991
999999999991
999999999991""",
]

LineType = int
InputType = list[LineType]


class Day17(aoc.Challenge):
    """Day 17: Clumsy Crucible."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=102),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=94),
        aoc.TestCase(inputs=SAMPLE[1], part=2, want=71),
    ]

    INPUT_PARSER = aoc.parse_ascii_char_map(lambda x: int(x))

    def part1(self, parsed_input: InputType) -> int:
        board = {(int(p.real), int(p.imag)): val for p, val in parsed_input.items()}
        min_x, min_y, max_x, max_y = aoc.bounding_coords(parsed_input)
        end = (max_x, max_y)
        location, direction, count = (0, 0), (0, 0), 0
        todo = queue.PriorityQueue()
        todo.put((0 + (max_x - location[0]) + (max_y - location[1]), 0, location, direction, count))
        seen = {}

        while not todo.empty():
            _, loss, location, direction, count = todo.get()
            if location == end:
                return loss
            
            for next_direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                if next_direction[0] == -direction[0] and next_direction[1] == -direction[1]:
                    continue
                if next_direction == direction and count == 3:
                    continue
                next_location = (location[0] + next_direction[0], location[1] + next_direction[1])
                if next_location not in board:
                    continue
                next_loss = loss + board[next_location]
                next_count = count + 1 if next_direction == direction else 1

                fp = (next_location, next_direction, next_count)
                if fp in seen and seen[fp] <= next_loss:
                    continue
                seen[fp] = next_loss

                todo.put((next_loss + (max_x - next_location[0]) + (max_y - next_location[1]), next_loss, next_location, next_direction, next_count))

        raise RuntimeError

    def part2(self, parsed_input: InputType) -> int:
        board = {(int(p.real), int(p.imag)): val for p, val in parsed_input.items()}
        min_x, min_y, max_x, max_y = aoc.bounding_coords(parsed_input)
        end = (max_x, max_y)
        location, direction, count = (0, 0), (0, 0), 0
        todo = queue.PriorityQueue()
        todo.put((0 + (max_x - location[0]) + (max_y - location[1]), 0, location, direction, count))
        seen = {}

        while not todo.empty():
            _, loss, location, direction, count = todo.get()
            if location == end and count >= 4:
                print("Got to the end", location, count, loss)
                return loss
            
            for next_direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                if next_direction[0] == -direction[0] and next_direction[1] == -direction[1]:
                    continue
                if direction != (0, 0) and next_direction != direction and count < 4:
                    continue
                if next_direction == direction and count == 10:
                    continue
                next_location = (location[0] + next_direction[0], location[1] + next_direction[1])
                if next_location not in board:
                    continue
                next_loss = loss + board[next_location]
                next_count = count + 1 if next_direction == direction else 1

                fp = (next_location, next_direction, next_count)
                if fp in seen and seen[fp] <= next_loss:
                    continue
                seen[fp] = next_loss

                todo.put((next_loss + (max_x - next_location[0]) + (max_y - next_location[1]), next_loss, next_location, next_direction, next_count))

        print("Ran out")
        raise NotImplementedError

    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        raise NotImplementedError

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
