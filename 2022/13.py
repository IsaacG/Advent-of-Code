#!/bin/python
"""Advent of Code, Day 13: Distress Signal."""
from __future__ import annotations

import random
import collections
import functools
import itertools
import math
import re

import typer
from lib import aoc

SAMPLE = [
    """\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]""",  # 0
]

LineType = int
InputType = list[LineType]


def dosort(vals):
    for i in range(len(vals) - 1):
        for j in range(len(vals) - 1):
            if inorder(vals[j], vals[j + 1]):
                vals[j], vals[j + 1] = vals[j+1], vals[j]
    return vals


def inorder(a, b) -> int:
    print(f"match {a=} {b=}")
    match [a, b]:
        case [int(), int()]:
            if a < b:
                return -1
            if b < a:
                return 1 
            return 0 
        case [list(), list()]:
            for i in range(min(len(a), len(b))):
                o = inorder(a[i], b[i])
                if o != 0:
                    return o 
            if len(a) < len(b):
                print("a", f"{len(a)=} {len(b)=} {a=} {b=}")
                return -1 
            if len(a) > len(b):
                return 1 
            return 0 
        case [list(), int()]:
            return inorder(a, [b]) 
        case [int(), list()]:
            return inorder([a], b) 
        case _:
            raise ValueError(f"Umatched {a} {b}")
    raise ValueError

class Day13(aoc.Challenge):
    """Day 13: Distress Signal."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=13),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=140),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]
    INPUT_PARSER = aoc.ParseBlocks([aoc.parse_one_str_per_line])

    def inorder(self, a, b) -> int:
        match [a, b]:
            case [int(), int()]:
                if a < b:
                    return 1
                if b < a:
                    return -1
                return 0
            case [list(), list()]:
                for i in range(min(len(a), len(b))):
                    o = self.inorder(a[i], b[i])
                    if o != 0:
                        return o
                if len(a) < len(b):
                    return 1
                if len(a) > len(b):
                    return -1
                return 0
            case [list(), int()]:
                return self.inorder(a, [b])
            case [int(), list()]:
                return self.inorder([a], b)
            case _:
                raise ValueError(f"Umatched {a} {b}")
        return False

    def part1(self, parsed_input: InputType) -> int:
        return None
        pairs = parsed_input
        count = 0
        for i, (a, b) in enumerate(pairs, start=1):
            o = self.inorder(eval(a), eval(b))
            print(o, a, b)
            if o == 1:
                count += i
        return count

    def part2(self, parsed_input: InputType) -> int:
        pairs = parsed_input
        vals = []
        vals.append([[6]])
        vals.append([[2]])
        for a, b in pairs:
            vals.append(eval(a))
            vals.append(eval(b))
        # print(vals)
        # dosort(vals)
        # print(vals)
        vals.sort(key=functools.cmp_to_key(inorder))
        print(vals)
        # print(vals.index([[2]]))
        # print(vals.index([[6]]))
        s = [[[2]], [], [[6]]]
        print(s)
        s.sort(key=functools.cmp_to_key(inorder))
        print(s)

        # s = list(range(10))
        # random.shuffle(s)
        # print(s)
        # dosort(s)
        # print(s)

        return (vals.index([[2]]) +1 )* (vals.index([[6]]) +1 )






if __name__ == "__main__":
    typer.run(Day13().run)

# vim:expandtab:sw=4:ts=4
