#!/bin/python
"""Advent of Code, Day 13: Knights of the Dinner Table."""

import itertools
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
]

InputType = tuple[dict[tuple[str, str], int], set[str]]


class Day13(aoc.Challenge):
    """Day 13: Compute happiness of guests sitting around a table."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=330),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    def max_happiness(self, data: dict[tuple[str, str], int], people: set[str]) -> int:
        """Return the max happiness which can be achieved through any seating arrangement."""
        return max(
            sum(
                data.get((person, neighbor), 0) + data.get((neighbor, person), 0)
                for person, neighbor in zip(order, order[1:] + order[:1])
            )
            for order in itertools.permutations(people, len(people))
        )

    def part1(self, parsed_input: InputType) -> int:
        """Return the max happiness for the guests."""
        return self.max_happiness(*parsed_input)

    def part2(self, parsed_input: InputType) -> int:
        """Return the max happiness for the guests and yourself."""
        data, people = parsed_input
        people.add("__yourself__")
        return self.max_happiness(data, people)

    def input_parser(self, puzzle_input: str) -> InputType:
        """Return happiness data and the guest list from the input."""
        data = {}
        people = set()
        matcher = re.compile(
            r"(.*) would (gain|lose) (\d+) happiness units by sitting next to (.*)."
        )
        for line in puzzle_input.splitlines():
            match = matcher.match(line)
            assert match is not None
            person, direction, num, neighbor = match.groups()
            num = int(num)
            if direction == "lose":
                num *= -1
            data[person, neighbor] = num
            people.add(person)
        return data, people


if __name__ == "__main__":
    typer.run(Day13().run)

# vim:expandtab:sw=4:ts=4
