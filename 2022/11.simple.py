#!/bin/python
"""Advent of Code, Day 11: Monkey in the Middle. Track items thrown between monkeys."""

import dataclasses
import operator
import math
import re
import sys
from typing import Any, Callable, Optional

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


class Day11:
    """Day 11: Monkey in the Middle."""

    PARAMETERIZED_INPUTS = [(20, True), (10000, False)]

    def solver(self, monkeys: list[Monkey], rounds_div: tuple[int,  bool]) -> int:
        """Simulate rounds of monkeys inspecting and throwing items."""
        rounds, div = rounds_div
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
        a, b = inspected[-2:]
        return a * b

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
    challenge = Day11()
    with open(sys.argv[1]) as f:
        monkeys = challenge.input_parser(f.read())
    for params in challenge.PARAMETERIZED_INPUTS:
        print(f"Got {challenge.solver(monkeys, params)}.")

# vim:expandtab:sw=4:ts=4
