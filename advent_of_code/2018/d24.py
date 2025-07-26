#!/bin/python
"""Advent of Code, Day 24: Immune System Simulator 20XX."""

from __future__ import annotations

import dataclasses
import re

from lib import aoc

SAMPLE = """\
Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4"""


@dataclasses.dataclass(kw_only=True)
class Group:
    """Group holds a group of cells."""
    team: str
    num: int
    units: int
    hp: int
    dmg: int
    init: int
    damage_type: str
    weak: set[str]
    immune: set[str]

    @property
    def effective_power(self) -> int:
        """Return the effective power."""
        return self.units * self.dmg

    def damage_dealt(self, other) -> int:
        """Return the damage dealt, factoring in weakness and immunity."""
        if self.damage_type in other.immune:
            return 0
        if self.damage_type in other.weak:
            return self.effective_power * 2
        return self.effective_power

    def attack(self, other: Group) -> int:
        """Perform an attack, returning the number of units killed."""
        dmg = self.damage_dealt(other)
        dies = min(dmg // other.hp, other.units)
        other.units -= dies
        return dies

    def __hash__(self) -> int:
        return self.num

    def __str__(self) -> str:
        return f"{self.team} {self.num}: {self.units}x {self.hp}hp {self.dmg}dmg"


class Battle:
    """Battle holds the initial setup state and logic to simulate a battle."""

    def __init__(self, teams: list[list[Group]]):
        self.teams = teams

    def select_targets(self, teams: list[list[Group]]) -> dict[Group, Group]:
        """Return which group targets which opposing group.

        If an attacking group is considering two defending groups to which it would deal equal damage,
        it chooses to target the defending group with the largest effective power;
        if there is still a tie, it chooses the defending group with the highest initiative.
        If it cannot deal any defending groups damage, it does not choose a target.
        Defending groups can only be chosen as a target by one attacking group.
        """
        targets = {}
        for attacking, defending in (teams, reversed(teams)):
            available = set(g for g in defending if g.units)
            for attacker in sorted(attacking, reverse=True, key=lambda x: (x.effective_power, x.init)):
                if not attacker.units:
                    continue
                target = max(
                    available,
                    key=lambda x: (attacker.damage_dealt(x), x.effective_power, x.init),
                    default=None,
                )
                if target is None or attacker.damage_dealt(target) == 0:
                    continue
                available.remove(target)
                targets[attacker] = target
        return targets

    def battle(self, boost: int) -> tuple[bool, int]:
        """Simulate a battle, returning if the immune system wins and the remaining units."""
        # Make a copy of the teams with a boost.
        teams = [
            [dataclasses.replace(g, dmg=g.dmg + (boost if idx == 0 else 0)) for g in team]
            for idx, team in enumerate(self.teams)
        ]
        # Fight while units are alive.
        while all(any(g.units for g in team) for team in teams):
            targets = self.select_targets(teams)
            died = 0
            for attacker, defender in sorted(targets.items(), key=lambda x: x[0].init, reverse=True):
                died += attacker.attack(defender)
            if not died:
                # Stale mate. No winners.
                return False, 0
            # Remove dead groups.
            teams = [[g for g in team if g.units] for team in teams]
        return any(g.units for g in teams[0]), sum(g.units for team in teams for g in team)


class Day24(aoc.Challenge):
    """Day 24: Immune System Simulator 20XX."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=5216),
        aoc.TestCase(part=2, inputs=SAMPLE, want=51),
    ]

    def solver(self, puzzle_input: Battle, part_one: bool) -> int:
        """Solve the exercise."""
        boost = 0 if part_one else self.get_boost(puzzle_input)
        return puzzle_input.battle(boost)[1]

    def get_boost(self, puzzle_input: Battle) -> int:
        """Return the minimum boost needed for the immune system to win."""
        # Find an upper limit using exponential growth.
        upper_limit = 2
        while not puzzle_input.battle(upper_limit)[0]:
            upper_limit *= 2

        # Find the minimum using binary search.
        lower_limit = upper_limit // 2
        while upper_limit > lower_limit:
            mid = (upper_limit + lower_limit) // 2
            too_low = not puzzle_input.battle(mid)[0]
            if too_low:
                lower_limit = mid + 1
            else:
                upper_limit = mid

        return lower_limit

    def input_parser(self, puzzle_input: str) -> Battle:
        """Parse the input data."""
        groups = []
        num = 1
        # Split into two armies.
        for block in puzzle_input.split("\n\n"):
            group = []
            team, *lines = block.splitlines()
            for line in lines:
                m = re.match(
                        r"(\d+) units each with (\d+) hit points ((?:\(.*\))?) ?with an attack "
                        r"that does (\d+) (.*) damage at initiative (\d+)", 
                        line
                    )
                assert m is not None
                units, hp, special, dmg, damage_type, init = m.groups()
                weak: set[str] = set()
                immune: set[str] = set()
                if special:
                    for s in special[1:-1].split("; "):
                        if s.startswith("immune to "):
                            immune.update(s.removeprefix("immune to ").split(", "))
                        if s.startswith("weak to "):
                            weak.update(s.removeprefix("weak to ").split(", "))
                group.append(Group(
                    team=team, num=num,
                    units=int(units), hp=int(hp), dmg=int(dmg), init=int(init),
                    damage_type=damage_type, weak=weak, immune=immune,
                ))
                num += 1
            groups.append(group)
        return Battle(groups)


# vim:expandtab:sw=4:ts=4
