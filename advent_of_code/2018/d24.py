#!/bin/python
"""Advent of Code, Day 24: Immune System Simulator 20XX."""

import dataclasses
import logging
import math
import re

from lib import aoc
log = logging.info
DEBUG = False

SAMPLE = [
    """\
Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4""",  # 7
]

class Battle:
    def __init__(self, teams):
        self.teams = teams

    def select_targets(self, teams):
        """
        If an attacking group is considering two defending groups to which it would deal equal damage,
        it chooses to target the defending group with the largest effective power;
        if there is still a tie, it chooses the defending group with the highest initiative.
        If it cannot deal any defending groups damage, it does not choose a target.
        Defending groups can only be chosen as a target by one attacking group.
        """
        targets = {}
        first = True
        for attacking, defending in (teams, reversed(teams)):
            available = set(g for g in defending if g.units)
            for attacker in sorted(attacking, reverse=True, key=lambda x: (x.effective_power, x.init)):
                if not attacker.units:
                    continue
                target = max(available, key=lambda x: (attacker.damage_dealt(x), x.effective_power, x.init), default=None)
                if target is None or attacker.damage_dealt(target) == 0:
                    continue
                available.remove(target)
                targets[attacker] = target
        return targets

    def battle(self, boost):
        teams = [
            [dataclasses.replace(g, dmg=g.dmg + (boost if idx == 0 else 0)) for g in team]
            for idx, team in enumerate(self.teams)
        ]
        while all(any(g.units for g in team) for team in teams):
            targets = self.select_targets(teams)
            assert targets
            died = 0
            for attacker, defender in sorted(targets.items(), key=lambda x: x[0].init, reverse=True):
                died += attacker.do_attack(defender)
            if not died:
                log("Stale mate")
                log(f"{[sum(g.units for g in team) for team in teams]}")
                return False, 0
            teams = [[g for g in team if g.units] for team in teams]
        return any(g.units for g in teams[0]), sum(g.units for team in teams for g in team)

@dataclasses.dataclass(kw_only=True)
class Group:
    team: str
    num: int
    units: int
    hp: int
    dmg: int
    init: int
    attack: str
    weak: set[str]
    immune: set[str]

    @property
    def effective_power(self) -> int:
        return self.units * self.dmg

    def damage_dealt(self, other) -> int:
        if self.attack in other.immune:
            return 0
        if self.attack in other.weak:
            return self.effective_power * 2
        return self.effective_power

    def do_attack(self, other) -> int:
        dmg = self.damage_dealt(other)
        dies = min(dmg // other.hp, other.units)
        other.units -= dies
        # log(f"{self} attacks {other} killing {dies}")
        return dies

    def __hash__(self) -> int:
        return hash((self.team, self.num))

    def __str__(self) -> str:
        return f"{self.team} {self.num}"


class Day24(aoc.Challenge):
    """Day 24: Immune System Simulator 20XX."""

    DEBUG = False
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=5216),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=51),
    ]

    def solver(self, puzzle_input: InputType, part_one: bool) -> int:
        boost = 0 if part_one else self.get_boost(puzzle_input)
        return puzzle_input.battle(boost)[1]

    def get_boost(self, puzzle_input: InputType) -> int:
        upper_limit = 18
        needs_more = True
        while not puzzle_input.battle(upper_limit)[0]:
            upper_limit *= 2
            log(f"Testing if {upper_limit} is high enough")

        lower_limit = upper_limit // 2
        while upper_limit > lower_limit:
            mid = (upper_limit + lower_limit) // 2
            log(f"{lower_limit} {mid} {upper_limit}")
            if mid == 33: DEBUG = True
            too_low = not puzzle_input.battle(mid)[0]
            if too_low:
                lower_limit = mid + 1
            else:
                upper_limit = mid

        assert upper_limit == lower_limit
        log(f"Boost {lower_limit}")
        return lower_limit

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        groups = ()
        inits = set()
        for block in puzzle_input.split("\n\n"):
            group = []
            team = block.splitlines()[0].removesuffix(":")
            for num, line in enumerate(block.splitlines()[1:], 1):
                m = re.match(r"(\d+) units each with (\d+) hit points ((?:\(.*\))?) ?with an attack that does (\d+) (.*) damage at initiative (\d+)", line)
                if m is None:
                    print(line)
                units, hp, special, dmg, attack, init = m.groups()
                weak = set()
                immune = set()
                if special:
                    for s in special[1:-1].split("; "):
                        if s.startswith("immune to "):
                            immune.update(s.removeprefix("immune to ").split(", "))
                        if s.startswith("weak to "):
                            weak.update(s.removeprefix("weak to ").split(", "))
                group.append(Group(
                    team=team,
                    num=num,
                    units=int(units),
                    hp=int(hp),
                    dmg=int(dmg),
                    init=int(init),
                    attack=attack,
                    weak=weak,
                    immune=immune,
                ))
                assert init not in inits
                inits.add(init)
            groups += (group,)
        return Battle(groups)


# vim:expandtab:sw=4:ts=4
