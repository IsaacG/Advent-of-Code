#!/bin/python
"""Advent of Code, Day 12: Subterranean Sustainability."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

import typer
from lib import aoc

SAMPLE = [
    """\
initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #""",  # 23
]

LineType = int
InputType = list[LineType]


class Day12(aoc.Challenge):
    """Day 12: Subterranean Sustainability."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=325),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]
    INPUT_PARSER = aoc.ParseBlocks([aoc.BaseParseReFindall(r"[.#]", lambda line: [i == "#" for i in line])] * 2)
    PARAMETERIZED_INPUTS = [20, 50000000000]

    def solver(self, parsed_input: InputType, *args, **kwargs) -> int:
        target_gen = args[0]
        state = {i for i, j in enumerate(parsed_input[0][0]) if j}
        rules = {tuple(rule[:5]) for rule in parsed_input[1] if rule[5]}
        seen = {}
        for gen in range(target_gen):
            new_state = set()
            for pot in range(min(state) - 2, max(state) + 3):
                    window = tuple(i in state for i in range(pot - 2, pot + 3))
                    if window in rules:
                        new_state.add(pot)
            state = new_state
            offset = min(state)
            shift_state = frozenset(pot - offset for pot in state)
            if shift_state in seen:
                prior_gen, prior_offset = seen[shift_state]
                gen_delta, offset_delta = (gen - prior_gen, offset - prior_offset)
                steps = target_gen - gen - 1
                total_shift = steps * offset_delta
                assert gen_delta == 1
                state = {pot + total_shift for pot in state}
                break
            seen[shift_state] = gen, offset
            if gen % 10000 == 0:
                print(f"{gen=}, {len(state)=}")
        assert sum(state) > 0
        assert sum(state) < 1150000000381
        return sum(state)


if __name__ == "__main__":
    typer.run(Day12().run)

# vim:expandtab:sw=4:ts=4
