#!/bin/python
"""Advent of Code, Day 13: Care Package."""

import collections
import functools
import itertools
import math
import re

import intcode
from lib import aoc

# Tiles
BLOCK = 2
PADDLE = 3
BALL = 4
SCORE = (-1, 0)


class Day13(aoc.Challenge):
    """Day 13: Care Package. Play paddle ball."""

    TESTS = [
        aoc.TestCase(inputs="", part=1, want=aoc.TEST_SKIP),
        aoc.TestCase(inputs="", part=2, want=aoc.TEST_SKIP),
    ]

    def part1(self, puzzle_input: str) -> int:
        """Count how many block tiles are printed."""
        computer = intcode.Computer(puzzle_input, debug=self.DEBUG)
        computer.run()
        blocks = set()
        while computer.output:
            x, y, tile = (computer.output.popleft() for _ in range(3))
            if tile == BLOCK:
                blocks.add((x, y))
        return len(blocks)


    def part2(self, puzzle_input: str) -> int:
        """Play the game by moving the paddle to follow the ball."""
        computer = intcode.Computer(puzzle_input, debug=self.DEBUG)
        computer.memory[0] = 2  # start the game without tokens

        paddle, ball, score = 0, 0, 0
        while not computer.stopped:
            computer.run()
            # Read all the video output
            while computer.output:
                x, y, tile = (computer.output.popleft() for _ in range(3))
                if tile == PADDLE:
                    paddle = x
                elif tile == BALL:
                    ball = x
                elif (x, y) == SCORE:
                    score = tile

            # Move the joystick.
            if paddle > ball:
                direction = -1
            elif paddle < ball:
                direction = 1
            else:
                direction = 0
            computer.input.append(direction)
        return score



# vim:expandtab:sw=4:ts=4
