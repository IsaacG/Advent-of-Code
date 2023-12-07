#!/bin/python
"""Advent of Code, Day 7: Camel Cards."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""",  # 28
]

LineType = int
InputType = list[LineType]


class Day07(aoc.Challenge):
    """Day 7: Camel Cards."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=6440),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=5905),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.parse_multi_str_per_line

    def srt(self, game: str) -> int:
        ORDER = list("AKQJT98765432")
        hand = game[0]
        score = 0
        for c in hand:
            score = score * 20 + ORDER.index(c)
        cnt = collections.Counter(hand)
        if cnt.most_common(1)[0][1] == 5:
            v = 1
        elif cnt.most_common(1)[0][1] == 4:
            v = 2
        elif set(cnt.values()) == {2, 3}:
            v = 3
        elif cnt.most_common(1)[0][1] == 3:
            v = 4
        elif sum(i == 2 for i in cnt.values()) == 2:
            v = 5
        elif 2 in cnt.values():
            v = 6
        else:
            v = 7
        return v, score

    def srt2(self, game: str) -> int:
        ORDER = list("AKQT98765432J")
        hand = game[0]
        score = 0
        for c in hand:
            score = score * 20 + ORDER.index(c)
        cnt = collections.Counter(hand)
        if "J" in hand:
            mostcommon = max(collections.Counter(i for i in hand if i != "J").values(), default="A")
            select = max((c for c in hand if c != "J" and cnt[c] == mostcommon), default="A")
            cnt = collections.Counter(hand.replace("J", select))

        if cnt.most_common(1)[0][1] == 5:
            v = 1
        elif cnt.most_common(1)[0][1] == 4:
            v = 2
        elif set(cnt.values()) == {2, 3}:
            v = 3
        elif cnt.most_common(1)[0][1] == 3:
            v = 4
        elif sum(i == 2 for i in cnt.values()) == 2:
            v = 5
        elif 2 in cnt.values():
            v = 6
        else:
            v = 7
        return v, score

    def part1(self, parsed_input: InputType) -> int:
        parsed_input.sort(key=self.srt, reverse=True)
        hands = [i[0] for i in parsed_input]
        assert len(hands) == len(set(hands))
        result = sum(idx * int(bid) for idx, (_, bid) in enumerate(parsed_input, start=1))
        return result

    def part2(self, parsed_input: InputType) -> int:
        parsed_input.sort(key=self.srt2, reverse=True)
        hands = [i[0] for i in parsed_input]
        assert len(hands) == len(set(hands))
        result = sum(idx * int(bid) for idx, (_, bid) in enumerate(parsed_input, start=1))
        return result

    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        raise NotImplementedError

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return super().input_parser(puzzle_input)
        return puzzle_input.splitlines()
        return puzzle_input
        return [int(i) for i in puzzle_input.splitlines()]
        mutate = lambda x: (x[0], int(x[1])) 
        return [mutate(line.split()) for line in puzzle_input.splitlines()]
        # Words: mixed str and int
        return [
            tuple(
                int(i) if i.isdigit() else i
                for i in line.split()
            )
            for line in puzzle_input.splitlines()
        ]
        # Regex splitting
        patt = re.compile(r"(.*) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.")
        return [
            tuple(
                int(i) if i.isdigit() else i
                for i in patt.match(line).groups()
            )
            for line in puzzle_input.splitlines()
        ]

# vim:expandtab:sw=4:ts=4
