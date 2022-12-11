#!/bin/python
"""Advent of Code, Day 11: Monkey in the Middle. Track items thrown between monkeys."""

import dataclasses
import operator
import math
import re
from typing import Any, Callable, Optional

import typer
from lib import aoc

SAMPLE = [
    """\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1""",  # 0
]

# Regex to parse the inputs
MONKEY_RE = re.compile(r"""
Monkey (?P<id>\d):
  Starting items: (?P<items>(?:\d+, )*\d+)
  Operation: new = old (?P<operator>[+*]) (?P<operand>\d+|old)
  Test: divisible by (?P<test_num>\d+)
    If true: throw to monkey (?P<true>\d+)
    If false: throw to monkey (?P<false>\d+)
""".strip())


@dataclasses.dataclass(slots=True)
class Monkey:
    """Details about each monkey."""

    id: int
    items: list[int]
    operator: Callable[[int, int], int]
    operand: Optional[int]
    test: int
    true: int
    false: int
    inspected: int


InputType = list[Monkey]


class Day11(aoc.Challenge):
    """Day 11: Monkey in the Middle."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=10605),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=2713310158),
    ]

    def solver(self, monkeys: list[Monkey], rounds: int, div: bool) -> int:
        """Simulate rounds of monkeys inspecting and throwing items."""
        # Use the LCM to keep the item size low.
        lcm = math.lcm(*[m.test for m in monkeys])

        # Cycle through rounds and monkeys.
        for _ in range(rounds):
            for monkey in monkeys:
                # Track how many items the monkey inspected.
                monkey.inspected += len(monkey.items)
                # For each item, update values and throw it to another monkey.
                for item in monkey.items:
                    item = monkey.operator(item, monkey.operand or item)
                    if div:
                        item = item // 3
                    item %= lcm
                    # Throw the item to the next monkey.
                    next_monkey = monkey.true if (item % monkey.test == 0) else monkey.false
                    monkeys[next_monkey].items.append(item)
                monkey.items = []
        inspected = sorted(monkey.inspected for monkey in monkeys)
        return self.mult(inspected[-2:])

    def part1(self, parsed_input: InputType) -> int:
        """Return the most troublesome monkeys after 20 rounds with div-by-three."""
        return self.solver(parsed_input, 20, True)

    def part2(self, parsed_input: InputType) -> int:
        """Return the most troublesome monkeys after 10000 rounds without div-by-three."""
        return self.solver(parsed_input, 10000, False)

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        monkeys = []
        for block in puzzle_input.split("\n\n"):
            match = MONKEY_RE.match(block)
            if not match:
                raise ValueError(f"Block did not match regex. {block}")
            numbers = {k: int(v) for k, v in match.groupdict().items() if v.isdigit()}
            monkeys.append(Monkey(
                id=numbers["id"],
                items=[int(i) for i in match.group("items").split(", ")],
                operator={"+": operator.add, "*": operator.mul}[match.group("operator")],
                operand=None if match.group("operand") == "old" else numbers["operand"],
                test=numbers["test_num"],
                true=numbers["true"],
                false=numbers["false"],
                inspected=0,
            ))

        return monkeys


if __name__ == "__main__":
    typer.run(Day11().run)

# vim:expandtab:sw=4:ts=4
