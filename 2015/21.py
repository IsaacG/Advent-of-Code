#!/bin/python
"""Advent of Code, Day 21: RPG Simulator 20XX. Compute the costs to win a battle."""

import itertools
import math

import typer
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

InputType = list[tuple[str, int]]


class Day21(aoc.Challenge):
    """Day 21: RPG Simulator 20XX."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=78),
        aoc.TestCase(inputs=SAMPLE, part=2, want=148),
    ]
    INPUT_PARSER = aoc.parse_re_group_mixed(r"(.*): (\d+)")

    def player_wins(self, you: dict[str, int], boss: dict[str, int]) -> bool:
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

    def solver(self, boss: dict[str, int]) -> dict[bool, list[int]]:
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
            costs[self.player_wins(you, boss)].append(cost)
        return costs

    def part1(self, parsed_input: InputType) -> int:
        """Return the min cost for the player to win."""
        costs = self.solver(dict(parsed_input))
        return min(costs[True])

    def part2(self, parsed_input: InputType) -> int:
        """Return the max cost for the boss to win."""
        costs = self.solver(dict(parsed_input))
        return max(costs[False])


if __name__ == "__main__":
    typer.run(Day21().run)

# vim:expandtab:sw=4:ts=4
