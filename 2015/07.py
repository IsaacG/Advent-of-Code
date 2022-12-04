#!/bin/python
"""Advent of Code: Day 07."""

import collections
import functools
import math
import re

import typer
from lib import aoc

SAMPLE = ["""\
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> a
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
"""]
InputType = list[int]


class Day07(aoc.Challenge):
    """Day 7: Some Assembly Required."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=492),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=492),
    ]

    # Convert lines to type:
    INPUT_TYPES = int
    # Split on whitespace and coerce types:
    # INPUT_TYPES = [str, int]
    # Apply a transform function
    # TRANSFORM = lambda _, l: (l[0], int(l[1:]))

    def part1(self, parsed_input: InputType) -> int:
        wire_in = set(parsed_input)
        wire_val = {}
        count = 0
        prior = 0

        for out, op, a, b in list(wire_in):
            if a.isdigit():
                wire_val[a] = int(a)
            if b.isdigit():
                wire_val[b] = int(b)

        while wire_in:
            count += 1
            # self.debug((count, len(wire_in), wire_val))
            if prior == len(wire_in):
                # print(wire_in)
                print("No progress!")
                break
            prior = len(wire_in)
            for out, op, a, b in list(wire_in):
                if op == "VAL" and a in wire_val:
                    wire_val[out] = wire_val[a]
                    wire_in.remove((out, op, a, b))
                elif op == "NOT" and a in wire_val:
                    wire_val[out] = ~wire_val[a] & 65535
                    wire_in.remove((out, op, a, b))
                elif op in ("RSHIFT", "LSHIFT") and a in wire_val:
                    if op == "RSHIFT":
                        wire_val[out] = wire_val[a] >> int(b)
                    if op == "LSHIFT":
                        wire_val[out] = wire_val[a] << int(b)
                    wire_in.remove((out, op, a, b))
                elif a in wire_val and b in wire_val:
                    if op == "AND":
                        wire_val[out] = wire_val[a] & wire_val[b]
                    if op == "OR":
                        wire_val[out] = wire_val[a] | wire_val[b]
                    wire_in.remove((out, op, a, b))
        else:
            return wire_val["a"]

        self.debug(f"Known: {list(wire_val)}")
        self.debug(f"Ops: {set(op for out, op, a, b in wire_in)}")
        for out, op, a, b in wire_in:
            if len(a) == 1:
                print(out, op, a, b)

    def part2(self, parsed_input: InputType) -> int:
        val_a = self.part1(parsed_input)
        v2 = []
        for out, op, a, b in parsed_input:
            if op == "VAL" and out == "b":
                a = str(val_a)
            v2.append((out, op, a, b))
        return self.part1(v2)


    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return super().parse_input(puzzle_input)
        return puzzle_input.splitlines()
        return puzzle_input
        return [int(i) for i in puzzle_input.splitlines()]
        mutate = lambda x: (x[0], int(x[1])) 
        return [mutate(line.split()) for line in puzzle_input.splitlines()]

    def line_parser(self, line: str) -> InputType:
        inp, out = line.split(" -> ")
        parts = inp.split()
        if len(parts) == 1:
            return (out, "VAL", parts[0], "0")
        if len(parts) == 2:
            return (out, "NOT", parts[1], "0")
        else:
            return (out, parts[1], parts[0], parts[2])


if __name__ == "__main__":
    typer.run(Day07().run)

# vim:expandtab:sw=4:ts=4
