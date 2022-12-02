#!/bin/python
"""Advent of Code: Day 02."""

import typer
from lib import aoc

SAMPLE = """\
A Y
B X
C Z
"""
InputType = list[tuple[str, str]]


LOSE, DRAW, WIN = "XYZ"
POINTS = {LOSE: 0, DRAW: 3, WIN: 6}


class Day02(aoc.Challenge):
    """Day 2: Rock Paper Scissors. Score a tournament."""

    TESTS = (
        aoc.TestCase(inputs=SAMPLE, part=1, want=15),
        aoc.TestCase(inputs=SAMPLE, part=2, want=12),
    )
    INPUT_TYPES = tuple[str, str]

    def part1(self, parsed_input: InputType) -> int:
        """Score a tournament with the columns representing the choices."""
        score = 0
        for elf_move, my_move in parsed_input:
            pos_a = "ABC".index(elf_move)
            pos_b = "XYZ".index(my_move)
            score += pos_b + 1
            if pos_a == pos_b:
                score += POINTS[DRAW]
            elif pos_b == (pos_a + 1) % 3:
                score += POINTS[WIN]
        return score

    def part2(self, parsed_input: InputType) -> int:
        """Score a tournament with the second column representing the outcome."""
        score = 0
        for elf_move, outcome in parsed_input:
            pos_a = "ABC".index(elf_move)
            score += POINTS[outcome]
            # The outcome determines if my move is the object before/after/same as the elf's.
            shift = {DRAW: 0, WIN: 1, LOSE: 2}[outcome]
            score += ((pos_a + shift) % 3) + 1
        return score

    def part2_short(self, parsed_input: InputType) -> int:
        """One liner."""
        # Sum up the points based on the outcome.
        # Combine the elf's move and outcome to get choice scores [0..2].
        # Add one for each round to shift the choice scores from [0..2] to [1..3].
        return sum(
            POINTS[outcome] + ("ABC".index(elf_move) + {DRAW: 0, WIN: 1, LOSE: 2}[outcome]) % 3
            for elf_move, outcome in parsed_input
        ) + len(parsed_input)

    def part2_reuse(self, parsed_input: InputType) -> int:
        """Solve part2 by rewriting the input and reusing part1."""
        moves = []
        for elf_move, outcome in parsed_input:
            pos_a = "ABC".index(elf_move)
            shift = {DRAW: 0, WIN: 1, LOSE: 2}[outcome]
            pos_b = (pos_a + shift) % 3
            my_move = "XYZ"[pos_b]
            moves.append((elf_move, my_move))
        return self.part1(moves)

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return [tuple(i.split()) for i in puzzle_input.splitlines()]


if __name__ == "__main__":
    typer.run(Day02().run)

# vim:expandtab:sw=4:ts=4
