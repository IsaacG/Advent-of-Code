#!/bin/python
"""Advent of Code, Day 22: Wizard Simulator 20XX. Pick the best spells to cast to beat the boss."""
from __future__ import annotations

import queue
import dataclasses
from typing import Any

from lib import aoc

SAMPLE = """\
Hit Points: 51
Damage: 9"""

LineType = list[int | str]
InputType = list[LineType]

# Lowest to highest mana cost
MISSILE, DRAIN, SHIELD, POISON, RECHARGE = range(5)
DURATION = {
    MISSILE: 0,
    DRAIN: 0,
    SHIELD: 6,
    POISON: 6,
    RECHARGE: 5,
}
COST = {
    MISSILE: 53,
    DRAIN: 73,
    SHIELD: 113,
    POISON: 173,
    RECHARGE: 229,
}


@dataclasses.dataclass(slots=True, frozen=True)
class GameState:
    """State of a game at a given turn."""

    player_hp: int
    boss_hp: int
    boss_damage: int
    player_mana: int
    mana_spent: int
    effects: tuple[int, int, int, int, int]
    hard: bool
    win: bool = False
    lose: bool = False

    def __lt__(self, other: GameState) -> bool:
        """Provide sorting for the priority queue; only care about mana spent."""
        return self.mana_spent < other.mana_spent

    @staticmethod
    def apply_effects(data: dict[str, Any]) -> None:
        """Update state with the effects."""
        if not any(effect for effect in data["effects"]):
            return
        if data["effects"][POISON]:
            data["boss_hp"] -= 3
        if data["effects"][RECHARGE]:
            data["player_mana"] += 101
        data["effects"] = tuple(
            max(0, effect - 1)
            for effect in data["effects"]
        )

    def valid_moves(self) -> list[int]:
        """Return valid player moves.

        Note, if effect timer == 1, it will expire at the start of the move
        and the player will be able to cast it again.
        """
        return [
            move
            for move in range(5)
            if COST[move] <= self.player_mana and self.effects[move] <= 1
        ]

    def move(self, move: int) -> GameState:
        """Apply a move and return next turn state."""
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
                data["mana_spent"] += cost
                data["player_mana"] -= cost

                if move == MISSILE:
                    data["boss_hp"] -= 4
                elif move == DRAIN:
                    data["boss_hp"] -= 2
                    data["player_hp"] += 2
                else:
                    effects = list(data["effects"])
                    effects[move] = DURATION[move]
                    data["effects"] = tuple(effects)

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

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=aoc.TEST_SKIP),
        aoc.TestCase(inputs=SAMPLE, part=2, want=aoc.TEST_SKIP),
    ]
    INPUT_PARSER = aoc.parse_re_group_mixed(r"(.*): (\d+)")

    def simulate(self, boss: dict[str, int], hard: bool) -> int:
        """Return the min mana needed to beat the boss."""
        start = GameState(
            player_hp=50,
            player_mana=500,
            boss_hp=boss["Hit Points"],
            boss_damage=boss["Damage"],
            mana_spent=0,
            effects=(0, 0, 0, 0, 0),
            hard=hard,
        )

        todo: queue.Queue[GameState] = queue.PriorityQueue()
        todo.put(start)

        seen = set()
        while todo:
            state = todo.get()
            # State checking: reduce runtime significantly!
            if state in seen:
                continue
            seen.add(state)
            # Terminate on first win.
            if state.win:
                return state.mana_spent
            # Add future states.
            for move in state.valid_moves():
                outcome = state.move(move)
                if not outcome.lose:
                    todo.put(outcome)

        raise RuntimeError("No solution found.")

    def part1(self, parsed_input: InputType) -> int:
        """Return mana to win, easy mode."""
        return self.simulate(dict(parsed_input), False)

    def part2(self, parsed_input: InputType) -> int:
        """Return mana to win, hard mode."""
        got = self.simulate(dict(parsed_input), True)
        assert got > 900   # Attempt 1
        assert got < 1242  # Attempt 2
        assert got > 1189  # Attempt 3
        return got
