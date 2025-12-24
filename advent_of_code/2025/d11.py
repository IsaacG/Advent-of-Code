#!/bin/python
"""Advent of Code, Day 11: Reactor."""
import functools


def solve(data: dict[str, list[str]], part: int) -> int:
    """Return the total paths from a source to output."""

    @functools.cache
    def paths_via(node: str, seen: int) -> int:
        """Return how many ways from node to out. Seen indicates if we saw the needed nodes."""
        if node == "out":
            return 1 if seen == 2 else 0
        if node in ["dac", "fft"]:
            seen += 1
        return sum(paths_via(i, seen) for i in data[node])

    if part == 1:
        return paths_via("you", 2)
    return paths_via("svr", 0)


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
TESTS = [(1, SAMPLE[0], 5), (2, SAMPLE[1], 2)]
# vim:expandtab:sw=4:ts=4
