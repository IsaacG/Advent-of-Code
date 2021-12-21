#!/bin/python
"""Advent of Code: Day 21."""

import collections
import functools
import itertools
import math
import re

import typer
from lib import aoc

SAMPLE = ["""\
Player 1 starting position: 4
Player 2 starting position: 8
"""]
InputType = list[int]

DICE_VALUES = list(itertools.product([1,2,3],[1,2,3],[1,2,3]))
DICE_COUNTS = collections.Counter(sum(vals) for vals in itertools.product(range(1, 4), repeat=3))

class Day21(aoc.Challenge):

    DEBUG = True
    SUBMIT = {1: True, 2: True}

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=739785),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=444356092776315),
    )

    # Convert lines to type:
    INPUT_TYPES = int
    # Split on whitespace and coerce types:
    # INPUT_TYPES = [str, int]
    # Apply a transform function
    # TRANSFORM = lambda _, l: (l[0], int(l[1:]))

    def part1(self, parsed_input: InputType) -> int:
        positions = parsed_input
        scores = [0,0]
        dice = itertools.cycle(range(100))
        turn = 0
        for step in range(1, 1000):
            roll = sum(next(dice) + 1 for _ in range(3))
            positions[turn] = (positions[turn] + roll) % 10
            scores[turn] += positions[turn]
            if positions[turn] == 0:
                scores[turn] += 10
            if scores[turn] >= 1000:
                break
            # print(f"{roll=} {positions[turn]=} {scores[turn]=}")
            turn = 1 - turn
        return (step * 3 * scores[1 - turn])

    def part2(self, parsed_input: InputType) -> int:
        positions = tuple(parsed_input)
        scores = tuple([0,0])
        turn = 0

        wins = self.go(0, 0, positions[0], positions[1], 0)
        print(wins, sum(wins))
        return max(wins)

    @functools.cache
    def go(self, cur_score, other_score, cur_pos, other_pos, turn):
        wins = [0, 0]
        # print(f"{step=} {scores=} {positions=}")
        # DICE_COUNTS = collections.Counter(sum(vals) for vals in itertools.product(range(1, 4), repeat=3))
        for roll, count in DICE_COUNTS.items():
            next_pos = (cur_pos + roll) % 10
            next_sco = cur_score + next_pos
            if next_pos == 0:
                next_sco += 10
            if next_sco >= 21:
                wins[turn] += count
            else:
                sub_win = self.go(other_score, next_sco, other_pos, next_pos, 1 - turn)
                for i in range(2):
                    wins[i] += sub_win[i] * count
        return wins

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return [int(line.split(": ")[1]) for line in puzzle_input.splitlines()]


if __name__ == "__main__":
    typer.run(Day21().run)

# vim:expandtab:sw=4:ts=4
