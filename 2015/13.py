#!/bin/python
"""Advent of Code, Day 13: Knights of the Dinner Table."""

import collections
import itertools
import functools
import math
import re

import typer
from lib import aoc

SAMPLE = [
    """\
Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.""",
    330,
]

InputType = dict[tuple[str, str], int]


class Day13(aoc.Challenge):
    """Day 13: Knights of the Dinner Table."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=SAMPLE[1]),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    def part1(self, parsed_input: InputType) -> int:
        people = set()
        for person, neighbor in parsed_input:
            people.add(person)
            people.add(neighbor)

        totals = [
            sum(
                parsed_input[person, neighbor] + parsed_input[neighbor, person]
                for person, neighbor in zip(order, order[1:] + order[:1])
            )
            for order in itertools.permutations(people, len(people))
        ]
        return max(totals)

    def part2(self, parsed_input: InputType) -> int:
        people = {"__yourself__"}
        for person, neighbor in parsed_input:
            people.add(person)
            people.add(neighbor)

        totals = [
            sum(
                parsed_input.get((person, neighbor), 0) + parsed_input.get((neighbor, person), 0)
                for person, neighbor in zip(order, order[1:] + order[:1])
            )
            for order in itertools.permutations(people, len(people))
        ]
        return max(totals)

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        data = {}
        matcher = re.compile(r"(.*) would (gain|lose) (\d+) happiness units by sitting next to (.*).")
        for line in puzzle_input.splitlines():
            person, direction, num, neighbor = matcher.match(line).groups()
            num = int(num)
            if direction == "lose":
                num *= -1
            data[person, neighbor] = num
        return data


if __name__ == "__main__":
    typer.run(Day13().run)

# vim:expandtab:sw=4:ts=4
