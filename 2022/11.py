#!/bin/python
"""Advent of Code, Day 11: Monkey in the Middle. Track items thrown between monkeys."""

import dataclasses
import math
import re
from typing import Any, Callable

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


@dataclasses.dataclass(slots=True)
class Monkey:
    """Details about each monkey."""

    number: int
    items: list[int]
    op: Callable[[int], int]
    test: Callable[[int], bool]
    test_num: int
    true: int
    false: int
    inspected: int = 0


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
        lcm = math.lcm(*[m.test_num for m in monkeys])

        # Cycle through rounds and monkeys.
        for _ in range(rounds):
            for monkey in monkeys:
                # Track how many items the monkey inspected.
                monkey.inspected += len(monkey.items)
                # For each item, update values and throw it to another monkey.
                for item in monkey.items:
                    item = monkey.op(item)
                    if div:
                        item = item // 3
                    item %= lcm
                    # Throw the item to the next monkey.
                    next_monkey = monkey.true if monkey.test(item) else monkey.false
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
        blocks = puzzle_input.split("\n\n")
        monkeys = []
        num_re = re.compile(r"\d+")
        for block in blocks:
            data: dict[str, Any] = {}
            for line in block.splitlines():
                line = line.strip()
                nums = [int(i) for i in num_re.findall(line)]
                if line.startswith("Monkey"):
                    data["number"] = nums[0]
                elif line.startswith("Starting items:"):
                    data["items"] = nums
                elif line.startswith("Test: divisible by"):
                    data["test"] = lambda x, n=nums[0]: x % n == 0
                    data["test_num"] = nums[0]
                elif line.startswith("Operation: new = "):
                    op = line.split(" = ")[-1]
                    if re.match(r"old \+ \d+", op):
                        data["op"] = lambda x, n=nums[0]: x + n
                    elif re.match(r"old \* \d+", op):
                        data["op"] = lambda x, n=nums[0]: x * n
                    elif re.match(r"old \* old", op):
                        data["op"] = lambda x: x * x
                    else:
                        raise ValueError(f"{op!r} op no match")
                elif line.startswith("Test: divisible by"):
                    data["test"] = nums[0]
                elif line.startswith("If true: throw to monkey"):
                    data["true"] = nums[0]
                elif line.startswith("If false: throw to monkey"):
                    data["false"] = nums[0]
                else:
                    raise ValueError("Not matched")
            monkeys.append(Monkey(**data))
        return monkeys


if __name__ == "__main__":
    typer.run(Day11().run)

# vim:expandtab:sw=4:ts=4
