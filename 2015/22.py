#!/bin/python
"""Advent of Code, Day 22: Wizard Simulator 20XX."""
from __future__ import annotations

import queue
import collections
import dataclasses
import functools
import itertools
import math
import re
from typing import Any

import typer
from lib import aoc

SAMPLE = """\
Hit Points: 51
Damage: 9"""

LineType = int
InputType = list[LineType]

# Lowest to highest mana cost
MISSILE, DRAIN, SHIELD, POISON, RECHARGE = range(5)
DURATION = {i: n for i, n in enumerate([0, 0, 6, 6, 5])}
COST = {i: n for i, n in enumerate([53, 73, 113, 173, 229])}


@dataclasses.dataclass(slots=True, frozen=True)
class GameState:

    player_hp: int
    boss_hp: int
    boss_damage: int
    player_mana: int
    mana_spent: int
    effects: list[int]

    def __lt__(self, other: GameState) -> bool:
        return self.mana_spent < other.mana_spent

    @staticmethod
    def apply_effects(data: dict[str, Any]) -> None:
        if data["effects"][POISON]:
            data["boss_hp"] -= 3
        if data["effects"][RECHARGE]:
            data["player_mana"] += 101
        for effect in (SHIELD, POISON, RECHARGE):
            if data["effects"][effect]:
                data["effects"][effect] -= 1

    def valid_moves(self) -> list[int]:
        return [
            move
            for move in range(5)
            if COST[move] <= self.player_mana and self.effects[move] == 0
        ]

    def move(self, move: int) -> bool | GameState:
        """Apply a move and return win|lose|next state."""
        data = dataclasses.asdict(self)
        for is_player in (True, False):
            # Effects occur.
            self.apply_effects(data)
            # Player wins if boss dies.
            if data["boss_hp"] <= 0:
                return True

            if is_player:
                # Player casts spell.
                cost = COST[move]
                # Player loses if they cannot cast.
                if self.player_mana < cost:
                    return False
                data["mana_spent"] += cost
                data["player_mana"] -= cost

                if move == MISSILE:
                    data["boss_hp"] -= 4
                elif move == DRAIN:
                    data["boss_hp"] -= 2
                    data["player_hp"] += 2
                else:
                    assert self.effects[move] == 0
                    data["effects"][move] = DURATION[move]

                # Player wins if boss dies.
                if data["boss_hp"] <= 0:
                    return True
            else:
                # Boss turn
                damage = self.boss_damage
                if data["effects"][SHIELD]:
                    damage -= 7
                damage = max(damage, 1)
                data["player_hp"] -= damage
                if data["player_hp"] < 1:
                    return False

        return GameState(**data)



class Day22(aoc.Challenge):
    """Day 22: Wizard Simulator 20XX."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=900),
        aoc.TestCase(inputs=SAMPLE, part=2, want=0),
        aoc.TestCase(inputs=SAMPLE, part=1, want=aoc.TEST_SKIP),
        aoc.TestCase(inputs=SAMPLE, part=2, want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_re_group_mixed(r"(.*): (\d+)")

    def part1(self, parsed_input: InputType) -> int:
        boss = dict(parsed_input)
        start = GameState(
            player_hp=50,
            player_mana=500,
            boss_hp=boss["Hit Points"],
            boss_damage=boss["Damage"],
            mana_spent=0,
            effects=[0] * 5,
        )
        todo = queue.PriorityQueue()
        todo.put(start)

        steps = 0
        while todo and steps < 50000:
            steps += 1
            state = todo.get()
            # print(state)
            for move in state.valid_moves():
                outcome = state.move(move)
                # Player wins
                if outcome is True:
                    return state.mana_spent + COST[move]
                # Player loses
                if outcome is False:
                    continue
                # Game continues
                todo.put(outcome)



if __name__ == "__main__":
    typer.run(Day22().run)

# vim:expandtab:sw=4:ts=4
