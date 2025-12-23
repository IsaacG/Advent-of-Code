#!/bin/python
"""Advent of Code, Day 21: Keypad Conundrum."""

import collections
import functools
import itertools

from lib import aoc
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


def solve(data: list[str], part: int) -> int:
    """Figure out the shortest way to open a door through multiple indirections."""

    def walk_pad(pad: dict[str, complex], src: str, dst: str) -> set[str]:
        """Return the possible ways to get from one char to another on the keypad."""
        p_src = pad[src]
        offset = pad[dst] - p_src
        pos_x = pad["X"]
        h_sign = aoc.sign(offset.real)
        v_sign = aoc.sign(offset.imag)

        parts = []
        parts.append({1: ">", -1: "<", 0: ""}[h_sign] * (int(offset.real) * h_sign))
        parts.append({1: "v", -1: "^", 0: ""}[v_sign] * (int(offset.imag) * v_sign))

        options = set()
        if p_src + complex(offset.real, 0) != pos_x:
            options.add(parts[0] + parts[1])
        if p_src + complex(0, offset.imag) != pos_x:
            options.add(parts[1] + parts[0])
        return options

    @functools.cache
    def explode_seq(sequence: str, indirections: int) -> int:
        """Return the minimum keypresses to enter a key sequence through a number of indirections."""
        if indirections == 0:
            return len(sequence) + 1
        # Memoize these two lines for 4x faster code.
        paths = [walk_pad(ARROW_PAD, src, dst) for src, dst in zip("A" + sequence, sequence + "A")]
        ways = [collections.Counter(i) for i in itertools.product(*paths)]
        return min(
            sum((explode_seq(subsequence, indirections - 1)) * count for subsequence, count in way.items())
            for way in ways
        )

    steps = 2 if part == 1 else 25
    total = 0
    for line in data:
        paths = [walk_pad(DIGIT_PAD, src, dst) for src, dst in zip("A" + line, line)]
        digit_paths = [frozenset(collections.Counter(i).items()) for i in itertools.product(*paths)]
        size = min(
            sum(explode_seq(sequence, steps) * count for sequence, count in one_input)
            for one_input in digit_paths
        )
        complexity = size * int(line.removesuffix("A"))
        total += complexity

    return total


SAMPLE = """\
029A
980A
179A
456A
379A"""
TESTS = [(1, SAMPLE, 126384)]
# vim:expandtab:sw=4:ts=4
