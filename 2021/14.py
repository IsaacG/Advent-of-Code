#!/bin/python
"""Advent of Code: Day 14."""

import collections
import functools
import math
import re

import typer

from lib import aoc

InputType = list[int]
SAMPLE = ["""\
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""]


class Day14(aoc.Challenge):

    DEBUG = True

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=1588),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=2188189693529),
    )

    def part1(self, lines: InputType) -> int:
        start, formulas = lines
        for _ in range(10):
            out = []
            for a, b in zip(start, start[1:]):
                pair = a + b
                out.append(a)
                out.append(formulas[pair])
            out.append(start[-1])
            start = out
        count = collections.Counter(start)
        return count.most_common()[0][1] - count.most_common()[-1][1]

    def part2(self, lines: InputType) -> int:
        start, formulas = lines
        original = start[0] + start[-1]
        pairs = collections.Counter([a + b for a, b in zip(start, start[1:])])
        for _ in range(40):
            out = collections.defaultdict(int)
            for pair, count in pairs.items():
                new_char = formulas[pair]
                pair1 = pair[0] + new_char
                pair2 = new_char + pair[1]
                out[pair1] += count
                out[pair2] += count
            pairs = out
        counter = collections.defaultdict(int)
        for pair, count in pairs.items():
            counter[pair[0]] += count
            counter[pair[1]] += count
        counter[original[0]] += 1
        counter[original[1]] += 1
        counter = {k: v//2 for k, v in counter.items()}
        return max(counter.values()) - min(counter.values())

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        start, formula_block = puzzle_input.split("\n\n")
        formulas = {}
        for line in formula_block.splitlines():
            pair, insert = line.split(" -> ")
            formulas[pair] = insert
        return (start, formulas)


if __name__ == "__main__":
    typer.run(Day14().run)

# vim:expandtab:sw=4:ts=4
