#!/bin/python
"""Advent of Code, Day 7: Camel Cards."""

import collections

from lib import aoc

SAMPLE = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

InputType = list[list[str]]

# The value of J changes from part 1 to part 2.
ORDERS = ("AKQJT98765432"[::-1], "AKQT98765432J"[::-1])
CARD_COUNT = max(len(cards) for cards in ORDERS)
# Hand ranking based on the largest group followed by the number of pairs:
# 5 of a kind. 4 of a kind. Full house. 3 of a kind. 2 pairs. 1 pair. Nothing.
RANK_ORDER = [(5, 0), (4, 0), (3, 1), (3, 0), (2, 2), (2, 1), (1, 0)]
RANKS = {
    largest_and_pairs: rank
    for rank, largest_and_pairs in enumerate(reversed(RANK_ORDER))
}


class Day07(aoc.Challenge):
    """Day 7: Camel Cards. Rank poker card hands."""

    INPUT_PARSER = aoc.parse_multi_str_per_line
    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=6440),
        aoc.TestCase(inputs=SAMPLE, part=2, want=5905),
    ]

    def sort(self, part_two: int, line: list[str]) -> tuple[int, int]:
        """Sort cards based on ranking then highest card."""
        hand = line[0]

        # Compute the secondary order.
        card_order = ORDERS[part_two]
        secondary = 0
        for card in hand:
            secondary = secondary * CARD_COUNT + card_order.index(card)

        # Replace J values if needed.
        if part_two and "J" in hand:
            card_counter = collections.Counter(i for i in hand if i != "J")
            # Pick the best replacement.
            # First, prefer the card that appears the most times.
            # Second, prefer the highest value card.
            card_ordering = lambda x: (card_counter[x], card_order.index(x))
            replacement = max(card_counter, key=card_ordering, default="A")
            hand = hand.replace("J", replacement)

        # Compute the primary order, using potentially an updated hand.
        card_counts = list(collections.Counter(hand).values())
        largest_group = max(card_counts)
        pairs = card_counts.count(2)
        primary = RANKS[largest_group, pairs]

        return (primary, secondary)

    def solver(self, puzzle_input: InputType, part_one: bool) -> int:
        """Sort hands then return the bid returns."""
        puzzle_input.sort(key=lambda x: self.sort(0 if part_one else 1, x))
        return sum(idx * int(bid) for idx, (_, bid) in enumerate(puzzle_input, start=1))

# vim:expandtab:sw=4:ts=4
