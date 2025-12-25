#!/bin/python
"""Advent of Code, Day 21: Monkey Math."""

import operator
from typing import Any

from lib import aoc

USE_SYMPY = False
if USE_SYMPY:
    import sympy

LineType = Any
InputType = list[LineType]
DIV = operator.truediv if USE_SYMPY else operator.floordiv
OPS = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": DIV}
REV = {"+": operator.sub, "-": operator.add, "*": DIV, "/": operator.mul}


class Symbol:
    """Symbol in a symbolic equation."""


class Variable(Symbol):
    """Variable symbol; an unknown."""

    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other: Any) -> bool:
        """Return if this is the same as other."""
        return isinstance(other, Variable) and self.name == other.name


class BinaryOp(Symbol):
    """A binary operator. Expected one int, one symbol and one operation."""

    def __init__(self, left: int | Symbol, operation: str, right: int | Symbol):
        assert (
            isinstance(left, Symbol) and isinstance(right, int)
            or isinstance(left, int) and isinstance(right, Symbol)
        )
        self.left = left
        self.operation = operation
        self.right = right

    def reverse(self, other: int) -> tuple[Symbol, int]:
        """Reverse an operation, applying the inverse to both sides."""
        if isinstance(self.right, int):
            return self.left, REV[self.operation](other, self.right)  # type: ignore

        assert isinstance(self.left, int)
        if self.operation == "+":
            # a + x = b   =>   x = b - a
            return self.right, other - self.left
        if self.operation == "-":
            # a - x = b   =>   x = a - b
            return self.right, self.left - other
        if self.operation == "*":
            # a * x = b   =>   x = b / a
            return self.right, other // self.left
        if self.operation == "/":
            # a / x = b   =>   x = a / b
            return self.right, self.left // other
        raise ValueError




def solve(data: InputType, part: int) -> int:
    """Solve for the root value of an equation."""
    monkeys = data
    solved = {}

    # Resolve the integer literals.
    for monkey, job in monkeys.items():
        if len(job) == 1:
            solved[monkey] = job[0]

    if part == 2:
        solved["humn"] = sympy.symbols("humn") if USE_SYMPY else Variable("humn")

    # Resolve until "root" is solved.
    unsolved = set(monkeys) - set(solved)
    while "root" not in solved:
        for monkey in list(unsolved):
            left, operation, right = monkeys[monkey]
            if left not in solved or right not in solved:
                continue
            if USE_SYMPY or isinstance(solved[left], int) and isinstance(solved[right], int):
                solved[monkey] = OPS[operation](solved[left], solved[right])
            else:
                solved[monkey] = BinaryOp(solved[left], operation, solved[right])
            unsolved.remove(monkey)

    if part == 1:
        return int(solved["root"])
    # Part 2: Isolate humn
    left, right = solved[monkeys["root"][0]], solved[monkeys["root"][2]]
    if USE_SYMPY:
        return int(sympy.solve(left - right)[0].round())
    # Unwind operators to isolate humn.
    if isinstance(left, int):
        left, right = right, left
    while isinstance(left, BinaryOp):
        assert isinstance(right, int)
        left, right = left.reverse(right)
    assert left == Variable("humn")
    return right


SAMPLE = """\
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""
TESTS = [(1, SAMPLE, 152), (2, SAMPLE, 301)]
