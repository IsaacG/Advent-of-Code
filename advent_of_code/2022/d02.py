#!/bin/python
"""Advent of Code: Day 02. Rock Paper Scissors. Score a tournament."""

from lib import aoc

LOSE, DRAW, WIN = list("XYZ")
POINTS = {LOSE: 0, DRAW: 3, WIN: 6}


def solve(data: str, part: int) -> int:
    """Solve the parts."""
    return (part1 if part == 1 else part2)(data)


def part1(data: list[list[str]]) -> int:
    """Score a tournament with the columns representing the choices."""
    score = 0
    for elf_move, my_move in data:
        pos_a = "ABC".index(elf_move)
        pos_b = "XYZ".index(my_move)
        score += pos_b + 1
        if pos_a == pos_b:
            score += POINTS[DRAW]
        elif pos_b == (pos_a + 1) % 3:
            score += POINTS[WIN]
    return score

def part2(data: list[list[str]]) -> int:
    return part2_readable(data)
    # return part2_reuse(data)

def part2_readable(data: list[list[str]]) -> int:
    """Score a tournament with the second column representing the outcome."""
    score = 0
    for elf_move, outcome in data:
        pos_a = "ABC".index(elf_move)
        pos_outcome = "XYZ".index(outcome)
        score += 3 * pos_outcome
        # The outcome determines if my move is the object before/after/same as the elf's.
        score += ((pos_a + pos_outcome + 2) % 3) + 1
    return score

def part2_reuse(data: list[list[str]]) -> int:
    """Solve part2 by rewriting the input and reusing part1."""
    moves = []
    for elf_move, outcome in data:
        pos_a = "ABC".index(elf_move)
        shift = {DRAW: 0, WIN: 1, LOSE: 2}[outcome]
        pos_b = (pos_a + shift) % 3
        my_move = "XYZ"[pos_b]
        moves.append((elf_move, my_move))
    return part1(moves)


SAMPLE = """\
A Y
B X
C Z
"""
TESTS = [(1, SAMPLE, 15), (2, SAMPLE, 12)]
