#!/bin/python
"""Advent of Code, Day 2: Cube Conundrum."""

import collections
import math

from lib import aoc

SAMPLE = [
    """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""",  # 3
]

LineType = int
InputType = list[LineType]


class Day02(aoc.Challenge):
    """Day 2: Cube Conundrum. Analyze marble game stats."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=8),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=2286),
    ]

    def part1(self, parsed_input: InputType) -> int:
        return sum(
            game_id for game_id, bunches in parsed_input.items()
            if all(
                b.get("red", 0) <= 12 and b.get("green", 0) <= 13 and b.get("blue", 0) <= 14
                for b in bunches
            )
        )
        return 0

    def part2(self, parsed_input: InputType) -> int:
        return sum(
            math.prod(
                max(b.get(i, 0) for b in bunches)
                for i in ["red", "green", "blue"]
            )
            for bunches in parsed_input.values()
        )

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        games = collections.defaultdict(list)
        for line in puzzle_input.splitlines():
            a, b = line.split(":")
            game_id = int(a.removeprefix("Game "))
            for bunch in b.split("; "):
                p = {}
                for one in bunch.split(", "):
                    count, color = one.split()
                    p[color] = int(count)
                games[game_id].append(p)
        return games

# vim:expandtab:sw=4:ts=4
