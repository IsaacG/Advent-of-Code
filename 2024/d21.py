#!/bin/python
"""Advent of Code, Day 21: Keypad Conundrum."""
from __future__ import annotations

import collections
import functools
import itertools

from lib import aoc

SAMPLE = [
    """\
029A
980A
179A
456A
379A""",  # 37
]

LineType = int
InputType = list[LineType]


class Day21(aoc.Challenge):
    """Day 21: Keypad Conundrum."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=126384),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    def solver(self, puzzle_input: InputType, part_one: bool) -> int:
        NUMPAD_LAYOUT = "789\n456\n123\nX0A"
        ARRPAD_LAYOUT = "X^A\n<v>"
        NUMPAD = {
            char: complex(x, y)
            for y, line in enumerate(NUMPAD_LAYOUT.splitlines())
            for x, char in enumerate(line)
        }
        ARRPAD = {
            char: complex(x, y)
            for y, line in enumerate(ARRPAD_LAYOUT.splitlines())
            for x, char in enumerate(line)
        }
        X_ARR = ARRPAD["X"]
        X_DIG = NUMPAD["X"]

        def digipad(src, dst):
            p_src = NUMPAD[src]
            offset = NUMPAD[dst] - p_src
            parts = []
            if offset.real > 0:
                parts.append( ">" * int(offset.real))
            else:
                parts.append( "<" * -int(offset.real))
            if offset.imag > 0:
                parts.append( "v" * int(offset.imag))
            else:
                parts.append( "^" * -int(offset.imag))

            options = []
            if p_src + complex(offset.real, 0) != X_DIG:
                options.append(parts[0] + parts[1] + "A")
            if p_src + complex(0, offset.imag) != X_DIG:
                options.append( parts[1] + parts[0] + "A")
            return options

        def arrpad(src, dst):
            p_src = ARRPAD[src]
            offset = ARRPAD[dst] - p_src
            parts = []
            if offset.real > 0:
                parts.append( ">" * int(offset.real))
            else:
                parts.append( "<" * -int(offset.real))
            if offset.imag > 0:
                parts.append( "v" * int(offset.imag))
            else:
                parts.append( "^" * -int(offset.imag))

            options = set()
            if p_src + complex(offset.real, 0) != X_ARR:
                options.add(parts[0] + parts[1])
            if p_src + complex(0, offset.imag) != X_ARR:
                options.add( parts[1] + parts[0])
            return options

        @functools.cache
        def arrseq_a(seq):
            v = [arrpad(src, dst) for src, dst in zip("A" + seq, seq + "A")]
            return [collections.Counter(i) for i in itertools.product(*v)]

        def arrseq(seq, count):
            return [{k: v * count for k, v in c.items()} for c in arrseq_a(seq)]

        @functools.cache
        def explode_seq(seq, remaining):
            if remaining == 0:
                return len(seq) + 1
            ways = arrseq_a(seq)
            return min(
                sum((explode_seq(s, remaining - 1)) * c for s, c in way.items())
                for way in ways
            )

        total = 0
        for lineno, line in enumerate(puzzle_input):
            options = {""}
            for src, dst in zip("A" + line, line):
                n = set()
                for opt_a in digipad(src, dst):
                    for opt_b in options:
                        n.add(opt_a + opt_b)
                options = n
            outputs = {frozenset(collections.Counter(o.rstrip("A").split("A")).items()) for o in options}

            steps = 2 if part_one else 25

            size = min(
                sum(explode_seq(seq, steps) * count for seq, count in one_input)
                for one_input in outputs
            )

            complexity = size * int(line.removesuffix("A"))
            print(f"{lineno=}, {line=}, {size=}, {complexity=}")
            total += complexity

        return total




# vim:expandtab:sw=4:ts=4
