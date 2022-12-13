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
    hard: bool
    win: bool = False
    lose: bool = False

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

    def move(self, move: int) -> GameState:
        """Apply a move and return win|lose|next state."""
        data = dataclasses.asdict(self)
        # At start of player's turn, on hard mode, drop 1HP.
        if self.hard:
            data["player_hp"] -= 1
            if data["player_hp"] < 1:
                return GameState(**data | {"lose": True})

        for is_player in (True, False):
            # Effects occur.
            self.apply_effects(data)
            # Player wins if boss dies.
            if data["boss_hp"] <= 0:
                return GameState(**data | {"win": True})

            if is_player:
                # Player turn. Player casts spell.
                cost = COST[move]
                # Player loses if they cannot cast.
                # if self.player_mana < cost:
                #     return GameState(**data | {"lose": True})
                data["mana_spent"] += cost
                data["player_mana"] -= cost

                if move == MISSILE:
                    data["boss_hp"] -= 4
                elif move == DRAIN:
                    data["boss_hp"] -= 2
                    data["player_hp"] += 2
                else:
                    assert data["effects"][move] == 0
                    data["effects"][move] = DURATION[move]

                # Player wins if boss dies.
                if data["boss_hp"] <= 0:
                    return GameState(**data | {"win": True})
            else:
                # Boss turn
                damage = data["boss_damage"]
                if data["effects"][SHIELD]:
                    damage -= 7
                damage = max(damage, 1)
                data["player_hp"] -= damage
                if data["player_hp"] < 1:
                    return GameState(**data | {"lose": True})

        return GameState(**data)



class Day22(aoc.Challenge):
    """Day 22: Wizard Simulator 20XX."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=aoc.TEST_SKIP),
        aoc.TestCase(inputs=SAMPLE, part=2, want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_re_group_mixed(r"(.*): (\d+)")

    def solver(self, boss: dict[str, int], hard: bool) -> int:
        start = GameState(
            player_hp=50,
            player_mana=500,
            boss_hp=boss["Hit Points"],
            boss_damage=boss["Damage"],
            mana_spent=0,
            effects=[0] * 5,
            hard=hard,
        )
        todo = queue.PriorityQueue()
        todo.put(start)
        costs = []

        step = 0
        while todo and step < 50000:
            step += 1
            state = todo.get()
            if step and step % 5000 == 0:
                print(f"{step=} {state}")
            if state.win:
                return state.mana_spent
            # print(state)
            for move in state.valid_moves():
                outcome = state.move(move)
                if not outcome.lose:
                    todo.put(outcome)
        raise RuntimeError("No solution found.")

    def part1(self, parsed_input: InputType) -> int:
        return self.solver(dict(parsed_input), False)

    def part2(self, parsed_input: InputType) -> int:
        got = self.solver(dict(parsed_input), True)
        assert got > 900   # Attempt 1
        assert got < 1242  # Attempt 2
        assert got > 1189  # Attempt 3
        return got


if __name__ == "__main__":
    typer.run(Day22().run)

# vim:expandtab:sw=4:ts=4
