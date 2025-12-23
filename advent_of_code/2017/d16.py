#!/bin/python
"""Advent of Code, Day 16: Permutation Promenade."""

import collections
import string

SPIN = 0
EXCHANGE = 1
PARTNER = 2


def solve(data: list[tuple[int, str | int, str | int]], part: int, testing: bool) -> str:
    """Do the dance shuffle on a lineup."""

    size = 5 if testing else 16
    dances = 1 if part == 1 else 1_000_000_000
    cmds = data
    dance_line = collections.deque(string.ascii_lowercase[:size])

    def dance():
        for op, first, second in cmds:
            if op == SPIN:
                dance_line.rotate(first)
            elif op == EXCHANGE:
                dance_line[first], dance_line[second] = dance_line[second], dance_line[first]
            else:
                a, b = dance_line.index(first), dance_line.index(second)
                dance_line[a], dance_line[b] = dance_line[b], dance_line[a]

    seen: dict[tuple[str, ...], int] = {}
    for count in range(dances):
        dance()
        t = tuple(dance_line)
        if t in seen:
            remaining = (dances - 1 - count) % (count - seen[t])
            want = seen[t] + remaining
            dance_line = next(
                collections.deque(line)
                for line, seen_count in seen.items()
                if seen_count == want
            )
            break
        seen[t] = count

    return "".join(dance_line)


def input_parser(data: str) -> list[tuple[int, str | int, str | int]]:
    """Parse the input data."""
    cmds = list[tuple[int, str | int, str | int]]()
    for word in data.split(","):
        match word[0], word[1:].split("/"):
            case "s", [step]:
                cmds.append((SPIN, int(step), 0))
            case "x", (first, second):
                cmds.append((EXCHANGE, int(first), int(second)))
            case "p", (first, second):
                cmds.append((PARTNER, first, second))
    return cmds


TESTS = [(1, 's1,x3/4,pe/b', 'baedc')]
# vim:expandtab:sw=4:ts=4
