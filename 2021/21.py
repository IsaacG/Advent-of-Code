#!/bin/python
"""Advent of Code: Day 21."""

import collections
import functools
import itertools

import typer
from lib import aoc

SAMPLE = "Player 1 starting position: 4\nPlayer 2 starting position: 8"
DICE_COUNTS = collections.Counter(sum(vals) for vals in itertools.product(range(1, 4), repeat=3))

class Day21(aoc.Challenge):
    """Implement Dirac Dice."""

    TESTS = (
        aoc.TestCase(inputs=SAMPLE, part=1, want=739785),
        aoc.TestCase(inputs=SAMPLE, part=2, want=444356092776315),
    )

    def part1(self, parsed_input: tuple[int, int]) -> int:
        """Play Dirac Dice to 100 points with deterministic dice."""
        positions = list(parsed_input)
        scores = [0, 0]
        dice = itertools.cycle(range(100))
        turn = 0
        for step in range(1, 1000):
            roll = sum(next(dice) + 1 for _ in range(3))
            positions[turn] = (positions[turn] + roll) % 10
            scores[turn] += positions[turn]
            if positions[turn] == 0:
                scores[turn] += 10
            if scores[turn] >= 1000:
                break
            turn = 1 - turn
        return step * 3 * scores[1 - turn]

    def part2(self, parsed_input: tuple[int, int]) -> int:
        """Play Dirac Dice, Quantum Edition to 21 points."""
        positions = parsed_input
        wins = self.play_quantum_round(0, 0, positions[0], positions[1])
        return max(wins)

    @functools.cache
    def play_quantum_round(
        self,
        score_self: int,
        score_other: int,
        position_self: int,
        position_other: int,
    ) -> tuple[int, int]:
        """Play a Quantum Round of Dirac Dice.

        By keeping the interface single, the code doesn't have to worry about
        mutable objects and the caching is more efficient.

        This method plays a round, considering all possible dice roll combinations,
        and recursively runs sub-rounds.

        Since rolls [1,1,2] [1,2,1] [2,1,1] are all the same and we just care about
        the sum, we can collapse all rolls into just their sum.

        The sum 6 shows up 7 times; each version produces the same results so we don't
        need to run it multiple times. Instead, do it once and track the count.
        If play A wins 4 tims, multiply the wins by the count and it's all good.

        Rather then tracking players directly and having to maintain all that extra state,
        we can just track "self" and "other" then swap those positions on each iteration.
        This logic is applied to the scores, positions and wins.

        The variables can be collapsed into tuples for a cleaner namespace but this is faster.
        """
        win_self, win_other = 0, 0
        # collections.Counter(sum(vals) for vals in itertools.product(range(1, 4), repeat=3))
        for roll, count in DICE_COUNTS.items():
            new_position = (position_self + roll) % 10
            new_score = score_self + new_position
            if new_position == 0:
                new_score += 10
            if new_score >= 21:
                win_self += count
            else:
                sub_win_other, sub_win_self = self.play_quantum_round(
                    score_other,
                    new_score,
                    position_other,
                    new_position,
                )
                win_self += sub_win_self * count
                win_other += sub_win_other * count
        return win_self, win_other

    def input_parser(self, puzzle_input: str) -> tuple[int, ...]:
        """Parse the input data."""
        return tuple([int(line.split(": ")[1]) for line in puzzle_input.splitlines()])


if __name__ == "__main__":
    typer.run(Day21().run)

# vim:expandtab:sw=4:ts=4
