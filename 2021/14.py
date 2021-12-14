#!/bin/python
"""Advent of Code: Day 14."""

import collections
import typer
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

    def part1(self, lines: InputType) -> int:
        """Transform the polymer 10 times."""
        return self.solve(lines, 10)

    def part2(self, lines: InputType) -> int:
        """Transform the polymer 10 times."""
        return self.solve(lines, 40)

    @staticmethod
    def solve(lines, count) -> int:
        """Transform the polymer a bunch of times and count.

        To avoid requiring more RAM than I can fit in a computer, do not actually expand
        the string for each step. Instead, store the number of times each pair occurs.

        ABCBCD => AB, BC, CB, BC, CD => AB: 1, BC: 2, CB: 1, CD: 1

        Then the transforms can be applied pair-wise.
        Assume formulas AB -> X, BC -> Y
        AB: 1 becomes AX: 1, XB: 1
        BC: 2 becomes BY: 2, YC: 2
        etc

        At the end we can simply count up the letters from each pair-count.
        AX: 1, XB: 1, BY: 2, YC: 2 => 1*(A, X, X, B), 2*(B, Y, Y, C)

        Note, however, that ABCD turns into AB BC CD. The middle letters are all doubled.
        The first and last are not doubled. They remain the same throughout all steps.
        To balance that out, add one for the first and last then divide it all by two.
        """
        start, formulas = lines
        # The first and last char need an extra count at the end as they are not duplicated.
        first_last = start[0], start[-1]
        # Build a counter of how many times each pair shows up.
        pairs = dict(collections.Counter([a + b for a, b in zip(start, start[1:])]))
        for _ in range(count):
            out: dict[str, int] = collections.defaultdict(int)
            # Assume AB -> C. If AB appears N times, add AC and CB both N times.
            for pair, occurances in pairs.items():
                new_char = formulas[pair]
                new_pairs = (pair[0] + new_char, new_char + pair[1])
                for new_pair in new_pairs:
                    out[new_pair] += occurances
            pairs = out
        # Count the number of occurances of each letter.
        counter: dict[str, int] = collections.defaultdict(int)
        for pair, occurances in pairs.items():
            counter[pair[0]] += occurances
            counter[pair[1]] += occurances
        # Add one more for the first-last which didn't get doubled.
        for letter in first_last:
            counter[letter] += 1
        counter = {k: v // 2 for k, v in counter.items()}
        return max(counter.values()) - min(counter.values())

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        # Start formula and a list of formulas.
        start, formula_block = puzzle_input.split("\n\n")
        # The formulas are pairs joined on " -> ".
        formulas: dict[str, str] = dict(line.split(" -> ") for line in formula_block.splitlines())
        return (start, formulas)


if __name__ == "__main__":
    typer.run(Day14().run)

# vim:expandtab:sw=4:ts=4
