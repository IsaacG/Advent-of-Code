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

OPS = {
    "add": operator.add,
    "mul": operator.mul,
    "div": operator.floordiv,
    "mod": operator.mod,
    "eql": operator.eq,
}

equallities = []


@dataclasses.dataclass
class Node:
    inp: int = None
    eql: int = None
    operator: str = None
    parts: list[Node] = None
    lit: int = None

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
            return f"Input_#{self.inp}"
        if self.operator == "NEQ":
            return f"NEQ#{self.eql}"
        if self.operator == "eql":
            return f"NEQ#{self.parts[1].inp - 1}"
        symbol = {
            "add": "+",
            "mul": "*",
            "mod": "%",
            "div": "//",
            "eql": "!=",
        }[self.operator]
        return f"({self.parts[0]} {symbol} {self.parts[1]})"

    def copy(self):
        return copy.deepcopy(self)

    def __add__(self, n):
        if self.lit == 0:
            return n
        if n.lit == 0:
            return self
        if self.is_lit and n.is_lit:
            return Node(lit=self.lit + n.lit)
        if self.operator == "add" and self.parts[1].is_lit and n.is_lit:
            rhs = Node(lit=self.parts[1].lit + n.lit)
            return Node(operator="add", parts=[self.parts[0], rhs])
        return Node(operator="add", parts=[self, n])

    @property
    def len(self):
        if self.is_lit or self.is_input:
            return 1
        return sum(n.len for n in self.parts)

    def eval(self, eqls):
        if self.is_lit:
            return self.lit
        if self.operator == "eql":
            assert self.parts[1].is_input
            return eqls[self.parts[1].inp - 1]
        if self.is_input:
            print(self)
            return 1
        assert self.operator in ("add", "mul", "mod", "div"), str(self)
        return OPS[self.operator](self.parts[0].eval(eqls), self.parts[1].eval(eqls))

    @property
    def max_val(self):
        if self.operator == "add":
            vals = [n.max_val for n in self.parts]
            if any(v is None for v in vals):
                return None
            return sum(vals)
        if self.is_lit:
            return self.lit
        if self.is_input:
            return 9

    def __mod__(self, n):
        assert n.is_lit
        if self.lit == 0:
            return self
        if (v := self.max_val) is not None and v < n.lit:
            return self
        return Node(operator="mod", parts=[self, n])
        assert n.is_lit and n.lit == 26
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
        return Node(operator="mod", parts=[self, n])

    def __mul__(self, n):
        if self.lit == 0 or n.lit == 1:
            return self
        if self.lit == 1 or n.lit == 0:
            return n
        return Node(operator="mul", parts=[self, n])

    def __floordiv__(self, n):
        if n.lit == 1:
            return self
        assert n.lit == 26
        return Node(operator="div", parts=[self,n])
        if self.operator == "mul" and self.parts[1].is_lit and self.parts[1].lit == 26:
            return self.parts[0]
        if self.operator == "add":
            if any(p.operator == "mul" and p.parts[1].lit == 26 for p in self.parts):
                return (self.parts[0]//26) + (self.parts[1]//26)
        return Node(operator="div", parts=[self,n])

    def eval_eq(self):
        # If we are comparing complex INPUTS, use a new node.
        if b.is_input:
            # print(f"Splitting at {idx=} for {line=}")
            ret = []
            assume = ([0, f"({mem[a]} == {b})"], [1, f"({mem[a]} != {b})"])
            for val, assm in assume:
                mem[a] = Node(lit=val)
                for assumptions, results in self.solver(idx + 1, mem):
                    ret.append(([assm] + assumptions, results))
            assert ret

    def __eq__(self, n):
        # Skip. We treat eql as __ne__ since it is always negated.
        if n.lit == 0:
            return self
        if self.is_lit and n.max_val is not None and self.lit > n.max_val:
            return Node(lit=1)
        eq = Node(operator="eql", parts=(self, n))
        global equallities
        equallities.append(eq)
        return eq
        eq = Node(operator="NEQ", eql=n.inp)
        print(eq)


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
        # self.code_len = 80

        global equallities

        input_counter = 1
        for idx in range(0, self.code_len):
            if idx % 50 == 0:
                print("Code Line", idx)
                # for var, val in mem.items():
                #     print(var, val)
            line = self.code[idx]

            if line[0] == "inp":
                var = line[1]
                mem[var] = Node(inp=input_counter)
                input_counter += 1
            else:
                a, b = line[1:]
                if b in "wxyz":
                    b = mem[b]
                else:
                    b = Node(lit=int(b))
                oper = OPS[line[0]]
                mem[a] = oper(mem[a], b)
            if line == ["add", "z", "y"]:
                if equallities:
                    e = equallities[-1]
                    print(f"NEQ#{e.parts[1].inp - 1} =>")
                    print(f"{e.parts[0]} != {e.parts[1]}")
                print(mem["z"])
                print()
            
        print("Done")
        print(mem["z"])
        print("# eqls:", len(equallities))
        if False:
           for e in equallities:
            print(f"NEQ#{e.parts[1].inp - 1} =>")
            print(f"{e.parts[0]} != {e.parts[1]}")
            print()
        eqls = [0] * len(equallities)
        # print("Eval:", mem["z"].eval(eqls))
        # x = [ (v % 26 + j) != Input N ]   =>       x_next =  (v * ((25 * x) + k)) + ((Input N + l) * x))) % 26 + m  != Input (N+1)

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return [line.split() for line in puzzle_input.splitlines()]


if __name__ == "__main__":
    typer.run(Day24().run)

# vim:expandtab:sw=4:ts=4
