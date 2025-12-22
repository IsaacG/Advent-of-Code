#!/usr/bin/env python
"""Math parser.

Initial messy code: 0.177/6.108/4.791 ms
I could reverse the tokens to make life easier but that feels like cheating.
Part 1, non-parameterized conds test: 3.313 ms
With the tree parser: 0.178/4.177/4.783 ms
"""

from typing import Callable


class Node:
    """A node can either be a single number or two nodes with an operator."""

    def __init__(self, a, op=None, b=None):
        self.a = a
        self.op = op
        self.b = b
        assert (op is None) == (b is None)
        if op is None:
            assert a.isnumeric()
            assert b is None
        else:
            assert isinstance(a, type(self))
            assert isinstance(b, type(self))

    def compute(self) -> int:
        """Compute the operation."""
        if self.op is None:
            return int(self.a)
        # Moving these for a map kills runtime.
        if self.op == '*':
            return self.a.compute() * self.b.compute()
        if self.op == '+':
            return self.a.compute() + self.b.compute()
        raise RuntimeError("Invalid op")

    def __str__(self):
        if self.op is None:
            return self.a
        return f'({self.a} {self.op} {self.b})'


def input_parser(puzzle_input: str) -> list[str]:
    """Drop whitespace."""
    return [line.replace(" ", "") for line in puzzle_input.split('\n')]


def solve(data: list[str], part: int) -> int:
    """Evaluate an expression."""
    if part == 1:
        # Treat + and * equally.
        conds = [lambda x: x in '+*']
    else:
        # Split on * first making it lower precendent than +.
        conds = [lambda x: x == '*', lambda x: x == '+']
    # Tokenize, create tree and math the tree.
    return sum(make_tree(tokenize(i), conds).compute() for i in data)


def get_split_for(tokens: list[str], conds: list[Callable[[str], bool]]) -> int | None:
    """Return the split-point, respecting (x) as one block."""
    for cond in conds:
        i = len(tokens) - 1
        depth = 0
        while i >= 0:
            if depth == 0 and cond(tokens[i]):
                return i
            if tokens[i] == ')':
                depth += 1
            elif tokens[i] == '(':
                depth -= 1
            i -= 1
    return None


def make_tree(tokens: list[str], conds: list[Callable[[str], bool]]):
    """Build a tree, arbitrary ordering based on the conds."""
    def _go(tkns):
        if len(tkns) == 1:
            return Node(tkns[0])
        # Find the right-most operator and split on that. Treat parens as a block.
        i = get_split_for(tkns, conds)
        if i is None:
            # Ran out of tokens. Must be "(exp)".
            assert tkns[0] == '(' and tkns[-1] == ')'
            return _go(tkns[1:-1])
        left = _go(tkns[:i])
        op = tkns[i]
        right = _go(tkns[i + 1:])
        return Node(left, op, right)
    return _go(tokens)


def tokenize(line: str) -> list[str]:
    """Tokenize the input into strings of nums/+/*/()."""
    tokens = []
    i = 0
    ll = len(line)
    while i < ll:
        ss = line[i]
        if ss in '()+*':
            tokens.append(ss)
            i += 1
        else:
            j = i + 1
            while j < ll and line[j] not in '()+*':
                j += 1
            tokens.append(line[i:j])
            i = j
    return tokens


TESTS = [
    (1, "2 * 3 + (4 * 5)", 26),
    (1, "5 + (8 * 3 + 9 + 3 * 4 * 3)", 437),
    (1, "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 12240),
    (1, "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 13632),
    (2, "1 + (2 * 3) + (4 * (5 + 6))", 51),
    (2, "2 * 3 + (4 * 5)", 46),
    (2, "5 + (8 * 3 + 9 + 3 * 4 * 3)", 1445),
    (2, "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 669060),
    (2, "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 23340),
]
