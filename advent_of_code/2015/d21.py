#!/bin/python
"""Advent of Code, Day 21: RPG Simulator 20XX. Compute the costs to win a battle."""

import itertools
import math

from lib import aoc

SAMPLE = """\
Hit Points: 104
Damage: 8
Armor: 1"""

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

PARSER = aoc.parse_re_group_mixed(r"(.*): (\d+)")


def player_wins(you: dict[str, int], boss: dict[str, int]) -> bool:
    """Return if the player wins the battle."""
    players = {True: you, False: boss}
    rounds_to_win = {}

    for player_turn in (True, False):
        damage = players[player_turn]["Damage"]
        damage -= players[not player_turn]["Armor"]
        damage = max(damage, 1)
        hp = players[not player_turn]["Hit Points"]
        rounds_to_win[player_turn] = math.ceil(hp / damage)

    return rounds_to_win[True] <= rounds_to_win[False]


def simulate(boss: dict[str, int]) -> dict[bool, list[int]]:
    """Compute all costs for all outcomes."""
    costs: dict[bool, list[int]] = {True: [], False: []}
    you = {"Hit Points": 100}

    weapon = ITEMS["Weapons"]
    armor = ITEMS["Armor"]
    rings = itertools.combinations(ITEMS["Rings"], 2)

    for a, b, (c, d) in itertools.product(weapon, armor, rings):
        gear = (a, b, c, d)
        # Name Cost Damage Armor
        cost = sum(i[1] for i in gear)
        you["Damage"] = sum(i[2] for i in gear)
        you["Armor"] = sum(i[3] for i in gear)
        costs[player_wins(you, boss)].append(cost)
    return costs


def solve(data: list[tuple[str, int]], part: int) -> int:
    """Return the min cost for the player to win/max cost for the boss to win."""
    costs = simulate(dict(data))
    if part == 1:
        return min(costs[True])
    return max(costs[False])


TESTS = [(1, SAMPLE, 78), (2, SAMPLE, 148)]

