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

OPS = {
    "add": operator.add,
    "mul": operator.mul,
    "div": operator.floordiv,
    "mod": operator.mod,
    "eql": operator.eq,
}


@dataclasses.dataclass
class Node:
    inp: int = None
    operator: str = None
    parts: list[Node] = None
    lit: int = None
    z: int = None
    val: Node = None

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
        if self.z is not None:
            return f"z_{self.z:02}"
        return f"({self.parts[0]} {self.operator} {self.parts[1]})"

    def eql_range_check_true(self):
        assert self.operator == "!="
        assert self.parts[1].is_input
        if self.parts[0].is_lit:
            return self.parts[0].lit >= 10
        assert self.parts[0].parts[1].is_lit
        return self.parts[0].parts[1].lit >= 10

    @property
    def len(self):
        if self.is_lit or self.is_input:
            return 1
        return sum(n.len for n in self.parts)

    def find_eql(self):
        if self.operator == "!=":
            return self
        if self.operator:
            for n in self.parts:
                if m := n.find_eql():
                    return m
        return None

    def eval_node_with(self, node, val):
        if self.z is not None:
            return self
        if self.is_lit:
            return self
        if self.operator == "!=":
            assert self == node
            return Node(lit=val)
        if self.is_input:
            return self
        assert self.operator in ("+", "*", "%", "//"), str(self)
        op = {
            "+": operator.add,
            "*": operator.mul,
            "//": operator.floordiv,
            "%": operator.mod,
        }[self.operator]
        vals = [n.eval_node_with(node, val) for n in self.parts]
        return op(vals[0], vals[1])

    def __add__(self, n):
        if self.lit == 0:
            return n
        if n.lit == 0:
            return self
        if self.is_lit and n.is_lit:
            return Node(lit=self.lit + n.lit)
        if self.operator == "+" and self.parts[1].is_lit and n.is_lit:
            rhs = Node(lit=self.parts[1].lit + n.lit)
            return Node(operator="+", parts=[self.parts[0], rhs])
        return Node(operator="+", parts=[self, n])

    def __mod__(self, n):
        if self.lit == 0:
            return self
        return Node(operator="%", parts=[self, n])

    def __mul__(self, n):
        if self.lit == 0 or n.lit == 1:
            return self
        if self.lit == 1 or n.lit == 0:
            return n
        return Node(operator="*", parts=[self, n])

    def __floordiv__(self, n):
        if n.lit == 1:
            return self
        return Node(operator="//", parts=[self,n])

    def __eq__(self, n):
        return Node(operator="!=", parts=[self,n])

    def div26(self):
        if self.z is not None:
            self = self.val
        if self.operator == "+" and self.parts[0].is_input and self.parts[1].is_lit and self.parts[1].lit <= 16:
            return Node(lit=0)
        if self.operator == "*" and self.parts[1].is_lit and self.parts[1].lit == 26:
            return self.parts[0]
        if self.operator == "+":
            return self.parts[0].div26() + self.parts[1].div26()
        if self.operator == "//":
            assert self.parts[1].lit == 26
            return self.parts[0].div26().div26()
        raise RuntimeError(f"wot: {self} {self.val}")

    def mod26(self):
        if self.z is not None:
            self = self.val
        if self.operator == "+" and self.parts[0].is_input and self.parts[1].is_lit and self.parts[1].lit <= 16:
            return self
        if self.operator == "*" and self.parts[1].is_lit and self.parts[1].lit == 26:
            return Node(lit=0)
        if self.operator == "+":
            return self.parts[0].mod26() + self.parts[1].mod26()
        raise RuntimeError(f"wot: {self} {self.val}")

    def eval(self):
        if self.is_lit:
            return self
        if self.operator == "+":
            return self.parts[0].eval() + self.parts[1].eval()
        if self.operator == "%":
            assert self.parts[1] == 26
            return self.parts[0].mod26()
        raise RuntimeError(f"wot: {self} {self.val}")




class Day24(aoc.Challenge):
    """Compute which serial numbers are valid for the MONAD.

    This exercise is mostly focused around reverse engineering the "MONAD"
    input program and only minimally about implementing the VM described in the prose.

    The input MONADs have certain characteristics which need to be sussed out and used.
    The MONAD follows the same pattern 14 times:
    * Input is loaded into `w`.
    * The `x` and `y` are set to 0.
    * There are two `eql` statements back to back, `eql x w` then `eql x 0`. Combined,
      this can be treated as `x != w`.
    * The `z` is set to a function of the prior `z` and a conditional on the input.

    Step 1
    ------
    Resolve all 14 `z` values (indicated by `add z y`) in terms of a prior `z`.
    This gives the form:
    z_(n+1) = (f(z_(n)) * ((25 * (((z_(n) % 26) + a) != Input_(n+1))) + 1)) + ((Input_(n+1) + b) * (((z_(n) % 26) + a) != Input_(n+1)))
    where a, b are fixed ints and `f(x) = x` or `f(x) = x // 26`

    Rewritten as a conditional,

    ```
    if ((z_(n) % 26) + a) != Input_(n+1):
        z_(n+1) = 26 * f(z_(n)) + Input_(n+1) + c
    else:
        z_(n+1) = f((z_(n))
    ```

    Examining the conditionals and bearing in mind that inputs must be [1..9],
    `(z % 26) + a != Input` will be true for all possible inputs if `a > 9`.

    Applying that reduction to the code yields seven instances of:

    ```
    z_(n+1) = z_(n) * 26 + Input_(n+1) + a
    ```

    where `z_(-1) = 0` and `a` is a known int.

    Given that inputs are valid iff `z_13 = 0`, there must be seven instances of:
    `z_(n+1) = z_(n) // 26` to reduce the `z` value to 0. These are found by setting
    the conditional `(z_n % 26) + a = Input_(n+1)`.

    Given `z_(n+1) = z_(n) * 26 + Input_(n+1) + a` and `z_(n+2) = z_(n+1) // 26`,
    we can reduce `z_(n+2) = z_(n)`. Using this transformation, this allows us to write
    all `z` values in the form `z_(x) = z_(y) * 26 + Input_(z) + a`

    Applying the reduced `z` for to the known equallities,
    `(z_n % 26) + a = Input_(n+1)`, `z % 26` becomes `(z_y * 26 + Input + a) % 26`
    which becomes `(z_y * 26) % 26 + (Input + a) % 26` which further reduces to
    simply `Input + a`. That gives us seven instances of
    `Input_x = Input_y + a`, each with unrelated `x` and `y` values.

    Recalling that all inputs must be [1..9], `Input_x = Input_y + a` gives a min
    and max value for both `Input` values. This gives upper and lowe limits on all
    14 input values.
    """

    DEBUG = False

    TESTS = []

    def part1(self, parsed_input: InputType) -> int:
        ranges = self.solve_ranges(parsed_input)
        return int("".join(str(ranges[i][1]) for i in range(14)))

    def part2(self, parsed_input: InputType) -> int:
        ranges = self.solve_ranges(parsed_input)
        return int("".join(str(ranges[i][0]) for i in range(14)))

    def solve_ranges(self, parsed_input: InputType) -> int:
        mem = {v: Node(lit=0) for v in 'wxyz'}
        z_vals = {}

        input_counter = 0
        z_counter = 0
        for line in parsed_input:
            # Skip.
            # All "eql" statements come in pairs of "eql x ?" then "eql x 0" which
            # can be combined and treated as "neq x ?".
            if line == ["eql", "x", "0"]:
                continue

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
                mem[a] = OPS[line[0]](mem[a], b)

            if line == ["add", "z", "y"]:
                z = Node(z=z_counter, val=mem["z"])
                mem["z"] = z
                self.debug(f"{z} = {z.val}")
                z_vals[z_counter] = z
                z_counter += 1
            
        counts = {1: 0, 0: 0}
        z_evaled = {}
        for z, n in z_vals.items():
            eql = n.val.find_eql()
            value = 1 if eql.eql_range_check_true() else 0
            counts[value] += 1
            n.val = n.val.eval_node_with(eql, value)
            self.debug(f"{n} = {n.val}")
            z_evaled[z] = {"eql": eql, "evaled": n, "is_eql": not value}
        self.debug(f"Shift counts: {counts}")
        assert counts[0] == counts[1]

        reduce_z_vals = []
        for z, n in z_vals.items():
            assert n.val.operator in ("+", "//"), n.val
            if n.val.operator == "+":
                reduce_z_vals.append(n.val)
            if n.val.operator == "//":
                assert n.val.parts[1] == 26
                v = n.val.parts[0].div26()
                while v.z is not None:
                    v = reduce_z_vals[v.z]
                reduce_z_vals.append(v)
                z_vals[z].val = v
            self.debug(f"{n} = {n.val} => {reduce_z_vals[-1]}")

        for z, n in z_vals.items():
            self.debug(f"{z}: {n.val}")

        input_ranges = {}
        for z in z_evaled:
            if not z_evaled[z]["is_eql"]:
                continue
            parts = z_evaled[z]["eql"].parts
            evaled = parts[0].eval()
            assert evaled.operator == "+" and evaled.parts[0].is_input and evaled.parts[1].is_lit
            offset = evaled.parts[1].lit
            self.debug(f"{parts[1]} = {evaled} {offset=}") 
            input_ranges[evaled.parts[0].inp] = (max(1, 1 - offset), min(9, 9 - offset))
            input_ranges[parts[1].inp] = (max(1, 1 + offset), min(9, 9 + offset))
        return input_ranges
        """
        z_00 = (Input_1 + 7)
        z_01 = ((z_0 * 26) + (Input_2 + 8))
        z_02 = ((z_1 * 26) + (Input_3 + 16))
        z_03 = ((z_2 * 26) + (Input_4 + 8))
        z_04 = (z_3 // 26)
        z_05 = ((z_4 * 26) + (Input_6 + 12))
        z_06 = (z_5 // 26)
        z_07 = ((z_6 * 26) + (Input_8 + 8))
        z_08 = (z_7 // 26)
        z_09 = (z_8 // 26)
        z_10 = ((z_9 * 26) + (Input_11 + 4))
        z_11 = (z_10 // 26)
        z_12 = (z_11 // 26)
        z_13 = (z_12 // 26)

        Input_5 = ((z_03 % 26) + -8)
        Input_7 = ((z_05 % 26) + -11)
        Input_9 = ((z_07 % 26) + -6)
        Input_10 = ((z_08 % 26) + -9)
        Input_12 = ((z_10 % 26) + -5)
        Input_13 = ((z_11 % 26) + -4)
        Input_14 = ((z_12 % 26) + -9)

        z_00 = Input_01 + 7
        z_01 = z_00 * 26 + Input_02 + 8
        z_02 = z_01 * 26 + Input_03 + 16
        z_03 = z_02 * 26 + Input_04 + 8
        z_04 = z_02
        z_05 = z_02 * 26 + Input_06 + 12
        z_06 = z_02
        z_07 = z_02 * 26 + Input_08 + 8
        z_08 = z_02
        z_09 = z_01
        z_10 = z_09 * 26 + Input_11 + 4
        z_11 = z_01
        z_12 = z_00
        z_13 = 0

        Input_05 = Input_04
        Input_07 = Input_06 + 1
        Input_09 = Input_08 + 2
        Input_10 = Input_03 + 7
        Input_12 = Input_11 - 1
        Input_13 = Input_02 + 4
        Input_14 = Input_01 - 2

        01: 3..9
        02: 1..5
        03: 1..2
        04: 1..9
        06: 1..8
        08: 1..7
        11: 2..9
        """
        # 95299897999897 == p1
        # 31111121382151 == p2
        

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return [line.split() for line in puzzle_input.splitlines()]


if __name__ == "__main__":
    typer.run(Day24().run)

# vim:expandtab:sw=4:ts=4
