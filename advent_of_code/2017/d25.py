#!/bin/python
"""Advent of Code, Day 25: The Halting Problem."""

import re


def solve(data: tuple[str, int, dict[str, list[tuple[bool, int, str]]]], part: int) -> int:
    """Return the checksum of the program."""
    del part
    cursor = 0
    state, steps, rules = data
    tape = set()
    for _ in range(steps):
        write, move, state = rules[state][cursor in tape]
        if write:
            tape.add(cursor)
        else:
            tape.discard(cursor)
        cursor += move
    return len(tape)


def input_parser(data: str) -> tuple[str, int, dict[str, list[tuple[bool, int, str]]]]:
    """Parse the input data."""
    preamble, *rules = data.split("\n\n")
    patt = re.compile(r"Begin in state (.)\.\nPerform a diagnostic checksum after (\d+) steps.")
    m = patt.match(preamble)
    assert m, preamble
    initial_state = m.group(1)
    steps = int(m.group(2))

    patt = re.compile(r"""In state (.):
  If the current value is 0:
    - Write the value ([01])\.
    - Move one slot to the (left|right)\.
    - Continue with state (.)\.
  If the current value is 1:
    - Write the value ([01])\.
    - Move one slot to the (left|right)\.
    - Continue with state (.)\.""")

    res = {}
    for rule in rules:
        m = patt.match(rule)
        assert m, rule
        start, w0, m0, n0, w1, m1, n1 = m.groups()
        res[start] = [
                (w0 == "1", 1 if m0 == "right" else -1, n0),
                (w1 == "1", 1 if m1 == "right" else -1, n1),
        ]
    return initial_state, steps, res


SAMPLE = """\
Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A."""
TESTS = [(1, SAMPLE, 3)]
# vim:expandtab:sw=4:ts=4
