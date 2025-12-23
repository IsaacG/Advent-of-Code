#!/bin/python
"""Advent of Code, Day 4: Scratchcards. Count up scorecard points."""


def solve(data: list[tuple[set[int], set[int]]], part: int) -> int:
    """Find scorecards that win."""
    if part == 1:
        return sum(
            2 ** (count - 1)
            for winning, has in data
            if (count := len(winning & has))
        )

    # Count how many scorecards we have.
    # Initialize the card count to one of each.
    card_count = {i: 1 for i in range(len(data))}

    for card_number, (winning, has) in enumerate(data):
        points = len(winning & has)
        count = card_count[card_number]
        # For all copies we get, add `count` times more.
        for i in range(card_number + 1, card_number + points + 1):
            card_count[i] += count
    return sum(card_count.values())


def input_parser(data: str) -> list[tuple[set[int], set[int]]]:
    """Parse the input data."""
    out = []
    for line in data.splitlines():
        winning, has = line.split(" | ")
        winning = winning.split(": ")[1].strip()
        winning_numbers = {int(i) for i in winning.split()}
        has_numbers = {int(i) for i in has.split()}
        out.append((winning_numbers, has_numbers))
    return out


SAMPLE = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
TESTS = [(1, SAMPLE, 13), (2, SAMPLE, 30)]
# vim:expandtab:sw=4:ts=4
