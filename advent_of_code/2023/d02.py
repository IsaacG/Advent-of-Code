#!/bin/python
"""Advent of Code, Day 2: Cube Conundrum. Analyze marble game stats."""
import collections
import math

P1_LIMITS = {"red": 12, "green": 13, "blue": 14}


def solve(data: dict[int, list[dict[str, int]]], part: int) -> int:
    """Find valid games based on colors."""
    # Return which games are valid based on a per-color limit.
    if part == 1:
        return sum(
            game_id for game_id, bunches in data.items()
            if all(
                all(
                    bunch.get(color, 0) <= limit for color, limit in P1_LIMITS.items()
                )
                for bunch in bunches
            )
        )

    # Return the per-color minimum if all bunches are valid.
    return sum(
        math.prod(
            max(bunch.get(i, 0) for bunch in bunches)
            for i in ["red", "green", "blue"]
        )
        for bunches in data.values()
    )


def input_parser(data: str) -> dict[int, list[dict[str, int]]]:
    """Parse the input data."""
    games = collections.defaultdict(list)
    for line in data.splitlines():
        game, bunches = line.split(":")
        game_id = int(game.removeprefix("Game "))
        for bunch in bunches.split("; "):
            counts = {}
            for one in bunch.split(", "):
                count, color = one.split()
                counts[color] = int(count)
            games[game_id].append(counts)
    return games


SAMPLE = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
TESTS = [(1, SAMPLE, 8), (2, SAMPLE, 2286)]
# vim:expandtab:sw=4:ts=4
