#!/bin/python
"""Advent of Code: Day 14."""

import collections
from lib import aoc

InputType = tuple[str, dict[str, str]]
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
    """Compute a polymer after it transforms a bunch of times."""

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=1588),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=2188189693529),
    )

    def part1(self, parsed_input: InputType) -> int:
        """Transform the polymer 10 times."""
        return self.solve(parsed_input, 10)

    def part2(self, parsed_input: InputType) -> int:
        """Transform the polymer 10 times."""
        return self.solve(parsed_input, 40)

    @staticmethod
    def solve(parsed_input, count) -> int:
        """Transform the polymer a bunch of times and count.

        To avoid requiring more RAM than I can fit in a computer, do not actually expand
        the string for each step. Instead, store the number of times each pair occurs.

        ABCBCD => AB, BC, CB, BC, CD => AB: 1, BC: 2, CB: 1, CD: 1

        Then the transforms can be applied pair-wise.
        Assume formulas AB -> X, BC -> Y
        AB: 1 becomes AX: 1, XB: 1
        BC: 2 becomes BY: 2, YC: 2
        etc

        At the end we can simply count up the (first) letter from each pair-count.
        AX: 1, XB: 1, BY: 2, YC: 2 => 1*(A, X), 2*(B, Y)

        Note, however, that ABCD turns into AB BC CD.
        Looking at just the first letters means dropping the final letter.
        The final letter needs adding back.
        """
        start, formulas = parsed_input
        # The first and last char need an extra count at the end as they are not duplicated.
        last = start[-1]
        # Build a counter of how many times each pair shows up.
        pairs = dict(collections.Counter([a + b for a, b in zip(start, start[1:])]))
        for _ in range(count):
            out: dict[str, int] = collections.defaultdict(int)
            # Assume AB -> C. If AB appears N times, add AC and CB both N times.
            for pair, occurances in pairs.items():
                for new_pair in formulas[pair]:
                    out[new_pair] += occurances
            pairs = out
        # Count the number of occurances of each letter.
        counter: dict[str, int] = collections.defaultdict(int)
        for pair, occurances in pairs.items():
            counter[pair[0]] += occurances
        # Add the last letter back in.
        counter[last] += 1
        return max(counter.values()) - min(counter.values())

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        # Start formula and a list of formulas.
        start, formula_block = puzzle_input.split("\n\n")

        # The formulas are pairs joined on " -> ".
        formulas = {}
        for line in formula_block.splitlines():
            pair, add = line.split(" -> ")
            formulas[pair] = (pair[0] + add, add + pair[1])

        return (start, formulas)
