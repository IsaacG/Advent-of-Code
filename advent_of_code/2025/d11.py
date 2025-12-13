#!/bin/python
"""Advent of Code, Day 11: Reactor."""
import functools
from lib import aoc

SAMPLE = [
    """\
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out""",
    """\
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out""",
]


class Day11(aoc.Challenge):
    """Day 11: Reactor."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=5),
        aoc.TestCase(part=2, inputs=SAMPLE[1], want=2),
    ]

    def solver(self, puzzle_input: dict[str, list[str]], part_one: bool) -> int:
        """Return the total paths from a source to output."""

        @functools.cache
        def paths_via(node: str, seen: int) -> int:
            """Return how many ways from node to out. Seen indicates if we saw the needed nodes."""
            if node == "out":
                return 1 if seen == 2 else 0
            if node in ["dac", "fft"]:
                seen += 1
            return sum(paths_via(i, seen) for i in puzzle_input[node])

        if part_one:
            return paths_via("you", 2)
        return paths_via("svr", 0)

# vim:expandtab:sw=4:ts=4
