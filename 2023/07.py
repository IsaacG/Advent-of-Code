#!/bin/python
"""Advent of Code, Day 7: Camel Cards."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

InputType = list[list[str]]

ORDERS = (list("AKQJT98765432"), list("AKQT98765432J"))


class Day07(aoc.Challenge):
    """Day 7: Camel Cards."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=6440),
        aoc.TestCase(inputs=SAMPLE, part=2, want=5905),
    ]
    INPUT_PARSER = aoc.parse_multi_str_per_line
    PARAMETERIZED_INPUTS = [0, 1]

    def primary_ordering(self, part: int, hand: str) -> int:
        cnt = collections.Counter(hand)

        if part and "J" in hand:
            count = max(collections.Counter(i for i in hand if i != "J").values(), default="A")
            select = max((card for card in hand if card != "J" and cnt[card] == count), default="A")
            hand = hand.replace("J", select)
            cnt = collections.Counter(hand)

        if cnt.most_common(1)[0][1] == 5:
            return 1
        if cnt.most_common(1)[0][1] == 4:
            return 2
        if set(cnt.values()) == {2, 3}:
            return 3
        if cnt.most_common(1)[0][1] == 3:
            return 4
        if sum(i == 2 for i in cnt.values()) == 2:
            return 5
        if 2 in cnt.values():
            return 6
        return 7

    def secondary_ordering(self, card_order: list[str], hand: str) -> int:
        score = 0
        for card in hand:
            score = score * 13 + card_order.index(card)
        return score

    def sort(self, param: int, line: list[str]) -> tuple(int, int):
        hand = line[0]
        return (self.primary_ordering(param, hand), self.secondary_ordering(ORDERS[param], hand))

    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        parsed_input.sort(key=lambda x: self.sort(param, x), reverse=True)
        return sum(idx * int(bid) for idx, (_, bid) in enumerate(parsed_input, start=1))

# vim:expandtab:sw=4:ts=4
