#!/bin/python
"""Advent of Code, Day 21: Keypad Conundrum."""

import collections
import functools
import itertools

from lib import aoc

SAMPLE = """\
029A
980A
179A
456A
379A"""
DIGITS_LAYOUT = """\
789
456
123
X0A"""
ARROWS_LAYOUT = """\
X^A
<v>"""


def pad_parse(layout: str) -> tuple[dict[str, complex], complex]:
    """Parse a keypad layout."""
    pad = {
        char: complex(x, y)
        for y, line in enumerate(layout.splitlines())
        for x, char in enumerate(line)
    }
    return pad, pad["X"]


DIGIT_PAD, DIGIT_X = pad_parse(DIGITS_LAYOUT)
ARROW_PAD, ARROW_X = pad_parse(ARROWS_LAYOUT)


class Day21(aoc.Challenge):
    """Day 21: Keypad Conundrum."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=126384),
        aoc.TestCase(part=2, inputs=SAMPLE, want=aoc.TEST_SKIP),
    ]

    def solver(self, puzzle_input: list[str], part_one: bool) -> int:

        def digipad(src, dst):
            p_src = DIGIT_PAD[src]
            offset = DIGIT_PAD[dst] - p_src
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
            if p_src + complex(offset.real, 0) != DIGIT_X:
                options.append(parts[0] + parts[1] + "A")
            if p_src + complex(0, offset.imag) != DIGIT_X:
                options.append( parts[1] + parts[0] + "A")
            return options

        def arrpad(src, dst):
            p_src = ARROW_PAD[src]
            offset = ARROW_PAD[dst] - p_src
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
            if p_src + complex(offset.real, 0) != ARROW_X:
                options.add(parts[0] + parts[1])
            if p_src + complex(0, offset.imag) != ARROW_X:
                options.add( parts[1] + parts[0])
            return options

        @functools.cache
        def arrseq_a(seq):
            v = [arrpad(src, dst) for src, dst in zip("A" + seq, seq + "A")]
            return [collections.Counter(i) for i in itertools.product(*v)]

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
            total += complexity

        return total




# vim:expandtab:sw=4:ts=4
