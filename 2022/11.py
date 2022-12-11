#!/bin/python
"""Advent of Code, Day 11: Monkey in the Middle."""

import operator
import collections
import dataclasses
import functools
import math
import re
from typing import Callable

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

LineType = int
InputType = list[LineType]


@dataclasses.dataclass
class Monkey:
    number: int
    items: list[int]
    op: Callable[[int], int]
    test: Callable[[int], bool]
    test_num: int
    true: int
    false: int
    inspected: int = 0

    def __post_init__(self):
        if self.number in (self.true, self.false):
            raise ValueError("Monkey should not throw self {self!r}")
        # print(self)

class Day11(aoc.Challenge):
    """Day 11: Monkey in the Middle."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=10605),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=2713310158),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    def part1(self, parsed_input: InputType) -> int:
        monkeys = parsed_input
        nums = sorted(monkeys)
        for step in range(20):
            for num in nums:
                monkey = monkeys[num]
                monkey.inspected += len(monkey.items)
                for item in monkey.items:
                    start = item
                    # print(f"{num=} {item=} {monkey.op(item)=}")
                    item = monkey.op(item)  # Worry level is multiplied by 19 to 1501.
                    change = item
                    item = item // 3  # Monkey gets bored with item. Worry level is divided by 3 to 500.
                    bored = item
                    if monkey.test(item):
                        monkeys[monkey.true].items.append(item)
                        # print(f"{step=} {num=} {start=} {change=} {bored=} True {monkey.true}")
                    else:
                        # print(f"{step=} {num=} {start=} {change=} {bored=} True {monkey.false}")
                        monkeys[monkey.false].items.append(item)
                monkey.items = []
            for num in nums:
                print(f"{step}: {num} is holding {monkeys[num].items}")
        for monkey in monkeys.values():
            print(f"Monkey {monkey.number} inspected {monkey.inspected}")
        inspected = sorted(monkey.inspected for monkey in monkeys.values())
        return self.mult(inspected[-2:])

    def part2(self, parsed_input: InputType) -> int:
        monkeys = parsed_input
        lcm = math.lcm(*[m.test_num for m in monkeys.values()])
        nums = sorted(monkeys)
        for step in range(10000):
            for num in nums:
                monkey = monkeys[num]
                monkey.inspected += len(monkey.items)
                for item in monkey.items:
                    start = item
                    # print(f"{num=} {item=} {monkey.op(item)=}")
                    item = monkey.op(item)  # Worry level is multiplied by 19 to 1501.
                    item %= lcm
                    if monkey.test(item):
                        monkeys[monkey.true].items.append(item)
                        # print(f"{step=} {num=} {start=} {change=} {bored=} True {monkey.true}")
                    else:
                        # print(f"{step=} {num=} {start=} {change=} {bored=} True {monkey.false}")
                        monkeys[monkey.false].items.append(item)
                monkey.items = []
            if step + 1 in (1, 20, 1000):
                for num in nums:
                    print(f"{step}: {num} is holding {monkeys[num].items}")
        for monkey in monkeys.values():
            print(f"Monkey {monkey.number} inspected {monkey.inspected}")
        inspected = sorted(monkey.inspected for monkey in monkeys.values())
        return self.mult(inspected[-2:])

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        blocks = puzzle_input.split("\n\n")
        monkeys = {}
        num_re = re.compile(r"\d+")
        for block in blocks:
            data = {}
            for line in block.splitlines():
                line = line.strip()
                nums = [int(i) for i in num_re.findall(line)]
                if line.startswith("Monkey"):
                    data["number"] = nums[0]
                elif line.startswith("Starting items:"):
                    data["items"] = nums
                elif line.startswith("Test: divisible by"):
                    data["test"] = functools.partial(divtest, nums[0])
                    data["test_num"] = nums[0]
                elif line.startswith("Operation: new = "):
                    op = line.split(" = ")[-1]
                    if re.match(r"old \+ \d+", op):
                        data["op"] = functools.partial(operator.add, nums[0])
                        # print(f"{line}: x + {nums[0]}")
                    elif re.match(r"old \* \d+", op):
                        data["op"] = functools.partial(operator.mul, nums[0])
                        # print(f"{line}: x * {nums[0]}")
                    elif re.match(r"old \* old", op):
                        data["op"] = lambda x: x * x
                        # print(f"{line}: x * x")
                    else:
                        raise ValueError(f"{op!r} op no match")
                    # print(f"{op} ==> 5 => {data['op'](5)}")
                elif line.startswith("Test: divisible by"):
                    data["test"] = nums[0]
                elif line.startswith("If true: throw to monkey"):
                    data["true"] = nums[0]
                elif line.startswith("If false: throw to monkey"):
                    data["false"] = nums[0]
                else:
                    raise ValueError("Not matched")
            monkeys[data["number"]] = Monkey(**data)
        return monkeys


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


def divtest(d, x):
    return x % d == 0


if __name__ == "__main__":
    typer.run(Day11().run)

# vim:expandtab:sw=4:ts=4
