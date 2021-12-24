#!/bin/python
"""Advent of Code: Day 24."""

from __future__ import annotations
import collections
import copy
import dataclasses
import functools
import math
import operator

import typer
from lib import aoc

SAMPLE = ["""\
inp x
mul x -1
""","""\
inp z
inp x
mul z 3
eql z x
""","""\
inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2
"""]
InputType = list[int]

EQL_OPER = lambda x, y: 0 if x == y else 1

at_end = 0

@dataclasses.dataclass
class Node:
    inp: int = None
    operator: str = None
    parts: list[Node] = None
    lit: int = None

    def __post_init__(self):
        if self.parts is None:
            self.parts = []
        else:
            self.parts = tuple(Node(lit=n) if isinstance(n, int) else n.copy() for n in self.parts)

    @property
    def is_input(self):
        return self.inp is not None

    @property
    def is_lit(self):
        return self.lit is not None

    def __str__(self):
        if self.is_lit:
            return f"{self.lit}"
        if self.is_input:
            return f"Input_{self.inp}"
        if self.operator == "add":
            return f"({self.parts[0]} + {self.parts[1]})"
        if self.operator == "mul":
            return f"({self.parts[0]} * {self.parts[1]})"
        if self.operator == "mod":
            return f"({self.parts[0]} % {self.parts[1]})"
        if self.operator == "div":
            return f"({self.parts[0]} // {self.parts[1]})"
        if self.operator == "eql":
            return f"({self.parts[0]} != {self.parts[1]})"
        return super().__str__()

    def copy(self):
        return copy.deepcopy(self)

    def __add__(self, n):
        if self.is_lit:
            if isinstance(n, int):
                self.lit += n
                return self
            if self.lit == 0:
                return n
            if n.is_lit:
                self.lit += n.lit
                return self
        if n == 0 or (isinstance(n, Node) and n.lit == 0):
            return self
        return Node(operator="add", parts=[self, n])

    def __mod__(self, n):
        # print(f"{self} % {n}")
        assert n == 26
        if self.operator == "mul" and self.parts[1].lit == 26:
            return Node(lit=0)
        if self.is_input:
            return self
        if self.is_lit and self.lit < 26:
            return self
        if self.operator == "add":
            if self.parts[0].is_input and self.parts[1].is_lit and self.parts[1].lit <= 16:
                return self
            new = (self.parts[0] % 26) + (self.parts[1] % 26)
            return Node(operator="mod", parts=[new, n])
        assert False, str(self)

    def __mul__(self, n):
        assert isinstance(n, int), str(n)
        if n == 0:
            return Node(lit=0)
        if n == 1:
            return self
        return Node(operator="mul", parts=[self, n])

    def __floordiv__(self, n):
        if n == 1:
            return self
        assert n == 26
        if self.operator == "mul" and self.parts[1].is_lit and self.parts[1].lit == 26:
            return self.parts[0]
        if self.operator == "add":
            if any(p.operator == "mul" and p.parts[1].lit == 26 for p in self.parts):
                return (self.parts[0]//26) + (self.parts[1]//26)
        if self.is_under():
            return Node(lit=0)
        return Node(operator="div", parts=[self,n])

    def is_under(self):
        if self.is_lit and self.lit < 26:
            return True
        if self.operator == "add" and self.parts[0].is_input and self.parts[1].is_lit and self.parts[1].lit <= 16:
            return True
        return False


class Day24(aoc.Challenge):

    DEBUG = True
    SUBMIT = {1: False, 2: False}

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=-1),
        aoc.TestCase(inputs=SAMPLE[1], part=2, want=0),
    )

    def part1(self, parsed_input: InputType) -> int:
        mem = {v: Node(lit=0) for v in 'wxyz'}
        self.code = parsed_input
        self.code_len = len(parsed_input)

        results = self.solver(0, mem)
        for assum, res in results:
            print("a", assum)
            print("r", res)
            print()

    def solver(self, start_idx, mem) -> int:
        mem = copy.deepcopy(mem)

        input_counter = 1
        for idx in range(start_idx, self.code_len):
            # if idx % 25 == 0:
            #     print("Code Line", idx)
            line = self.code[idx]
            handled = False

            if line[0] == "inp":
                var = line[1]
                mem[var] = Node(inp=input_counter)
                input_counter += 1
                handled = True
            else:
                a, b = line[1:]
                if b in "wxyz":
                    b = mem[b]
                    if b.is_lit:
                        b = b.lit
                else:
                    b = int(b)

            if line[0] == "eql":
                handled = True
                # Skip. We treat eql as __ne__ since it is always negated.
                if b == 0:
                    pass
                # INPUT = (v: v>=10) is always False since INPUT < 10.
                elif mem[a].is_lit and b.is_input and mem[a].lit > 9:
                    mem[a].lit = 1
                # If we are comparing complex INPUTS, split.
                elif b.is_input:
                    # print(f"Splitting at {idx=} for {line=}")
                    ret = []
                    assume = ([0, f"({mem[a]} == {b})"], [1, f"({mem[a]} != {b})"])
                    for val, assm in assume:
                        mem[a] = Node(lit=val)
                        for assumptions, results in self.solver(idx + 1, mem):
                            ret.append(([assm] + assumptions, results))
                    assert ret
                else:
                    mem[a] = Node(operator=op, parts=(mem[a], b))
                    if b == 26:
                        print(f"{' '.join(line):12} | {handled}  | {args[0]} = {mem[args[0]]}")

            elif line[0] != "inp":
                oper = {
                    "add": operator.add,
                    "mul": operator.mul,
                    "div": operator.floordiv,
                    "mod": operator.mod,
                }[line[0]]

                if mem[a].is_lit and isinstance(b, int):
                    mem[a].lit = oper(mem[a].lit, b)
                    handled = True
                elif isinstance(b, int) and mem[a].is_lit:
                    mem[a] = oper(mem[a].lit, b)
                    handled = True
                else:
                    mem[a] = oper(mem[a], b)
                    handled = True

            # print(f"{' '.join(line):12} | {handled}  | {args[0]} = {mem[args[0]]}")
            assert handled, f"{' '.join(line):12} | {handled}  | {args[0]} = {mem[args[0]]}"

        assert str(mem["z"])
        global at_end
        at_end += 1
        print(f"{at_end=}")
        return [([], str(mem["z"]))]



    def brute(self, parsed_input: InputType) -> int:
        input_vals = iter(range(1, 100))
        for i in range(99999999999999, 0, -1):
            if i % 10000 == 0:
                print(i)
            i = str(i)
            if "0" in i:
                continue
            if self.check(parsed_input, i):
                return i
        raise RuntimeError("not found")

    def check(self, monad, inputs):
        input_vals = iter(inputs)
        mem = {v: 0 for v in 'wxyz'}
        for op, *args in monad:
            if op == "inp":
                mem[args[0]] = int(next(input_vals))
            else:
                a, b = args
                if b in "wxyz":
                    b = mem[b]
                else:
                    b = int(b)

                oper = {
                    "add": operator.add,
                    "mul": operator.mul,
                    "div": operator.floordiv,
                    "mod": operator.mod,
                    "eql": lambda x, y: 1 if x == y else 0,
                }[op]
                mem[a] = oper(mem[a], b)
        return mem["z"] == 0

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return [line.split() for line in puzzle_input.splitlines()]


if __name__ == "__main__":
    typer.run(Day24().run)

# vim:expandtab:sw=4:ts=4
