#!/bin/python
"""Advent of Code, Day 2: Cube Conundrum."""

import collections
import math

from lib import aoc

SAMPLE = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

InputType = dict[int, list[dict[str, int]]]
P1_LIMITS = {"red": 12, "green": 13, "blue": 14}


class Day02(aoc.Challenge):
    """Day 2: Cube Conundrum. Analyze marble game stats."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=8),
        aoc.TestCase(inputs=SAMPLE, part=2, want=2286),
    ]

    def part1(self, puzzle_input: InputType) -> int:
        """Return which games are valid based on a per-color limit."""
        return sum(
            game_id for game_id, bunches in puzzle_input.items()
            if all(
                all(
                    bunch.get(color, 0) <= limit for color, limit in P1_LIMITS.items()
                )
                for bunch in bunches
            )
        )

    def part2(self, puzzle_input: InputType) -> int:
        """Return the per-color minimum if all bunches are valid."""
        return sum(
            math.prod(
                max(bunch.get(i, 0) for bunch in bunches)
                for i in ["red", "green", "blue"]
            )
            for bunches in puzzle_input.values()
        )

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        games = collections.defaultdict(list)
        for line in puzzle_input.splitlines():
            game, bunches = line.split(":")
            game_id = int(game.removeprefix("Game "))
            for bunch in bunches.split("; "):
                counts = {}
                for one in bunch.split(", "):
                    count, color = one.split()
                    counts[color] = int(count)
                games[game_id].append(counts)
        return games

# vim:expandtab:sw=4:ts=4
