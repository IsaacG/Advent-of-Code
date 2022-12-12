#!/bin/python
"""Advent of Code, Day 21: RPG Simulator 20XX."""

import collections
import itertools
import functools
import math
import re

import typer
from lib import aoc

SAMPLE = """\
Hit Points: 104
Damage: 8
Armor: 1"""

STORE = """\
Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3"""

ITEMS = {
    "Weapons": [
        # Name Cost Damage Armor
        ("Dagger", 8, 4, 0),
        ("Shortsword", 10, 5, 0),
        ("Warhammer", 25, 6, 0),
        ("Longsword", 40, 7, 0),
        ("Greataxe", 74, 8, 0),
    ],
    "Armor": [
        ("None", 0, 0, 0),
        ("Leather", 13, 0, 1),
        ("Chainmail", 31, 0, 2),
        ("Splintmail", 53, 0, 3),
        ("Bandedmail", 75, 0, 4),
        ("Platemail", 102, 0, 5),
    ],
    "Rings": [
        ("None", 0, 0, 0),
        ("None", 0, 0, 0),
        ("Damage +1", 25, 1, 0),
        ("Damage +2", 50, 2, 0),
        ("Damage +3", 100, 3, 0),
        ("Defense +1", 20, 0, 1),
        ("Defense +2", 40, 0, 2),
        ("Defense +3", 80, 0, 3),
    ],
}

LineType = int
InputType = list[LineType]


class Day21(aoc.Challenge):
    """Day 21: RPG Simulator 20XX."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=78),
        aoc.TestCase(inputs=SAMPLE, part=2, want=148),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_re_group_mixed(r"(.*): (\d+)")

    def player_wins(self, you, boss) -> bool:
        players = {True: you, False: boss}
        rounds_to_win = {}

        for player_turn in (True, False):
            damage = players[player_turn]["Damage"]
            damage -= players[not player_turn]["Armor"]
            damage = max(damage, 1)
            hp = players[not player_turn]["Hit Points"]
            rounds_to_win[player_turn] = math.ceil(hp / damage)

        return rounds_to_win[True] <= rounds_to_win[False]

    def part1(self, parsed_input: InputType) -> int:
        boss = dict(parsed_input)
        you = {"Hit Points": 100, "Damage": 0, "Armor": 0}
        weapon = itertools.combinations(ITEMS["Weapons"], 1)
        armor = itertools.combinations(ITEMS["Armor"], 1)
        rings = itertools.combinations(ITEMS["Rings"], 2)

        win_costs = []

        count = 0
        for (a, ), (b, ), (c, d) in itertools.product(weapon, armor, rings):
            # Name Cost Damage Armor
            # print(a, b, c, d)
            cost = sum(i[1] for i in (a, b, c, d))
            you["Damage"] = sum(i[2] for i in (a, b, c, d))
            you["Armor"] = sum(i[3] for i in (a, b, c, d))
            if self.player_wins(you, boss):
                win_costs.append(cost)
        print(win_costs)
        return min(win_costs)
        
    def part2(self, parsed_input: InputType) -> int:
        boss = dict(parsed_input)
        you = {"Hit Points": 100, "Damage": 0, "Armor": 0}
        weapon = itertools.combinations(ITEMS["Weapons"], 1)
        armor = itertools.combinations(ITEMS["Armor"], 1)
        rings = itertools.combinations(ITEMS["Rings"], 2)

        win_costs = []

        count = 0
        for (a, ), (b, ), (c, d) in itertools.product(weapon, armor, rings):
            # Name Cost Damage Armor
            # print(a, b, c, d)
            cost = sum(i[1] for i in (a, b, c, d))
            you["Damage"] = sum(i[2] for i in (a, b, c, d))
            you["Armor"] = sum(i[3] for i in (a, b, c, d))
            if not self.player_wins(you, boss):
                win_costs.append(cost)
        print(win_costs)
        return max(win_costs)
        



if __name__ == "__main__":
    typer.run(Day21().run)

# vim:expandtab:sw=4:ts=4
