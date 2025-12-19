#!/bin/python
"""Advent of Code, Day 7: Some Assembly Required. Solve circuit outputs."""

from lib import aoc


def line_parser(line: str) -> tuple[str, str, str, str]:
    """Parse one line."""
    inp, out = line.split(" -> ")
    parts = inp.split()
    if len(parts) == 1:
        return (out, "VAL", parts[0], "0")
    if len(parts) == 2:
        return (out, "NOT", parts[1], "0")
    return (out, parts[1], parts[0], parts[2])


def get_wire(data: list[tuple[str, str, str, str]]) -> int:
    """Solve for wire a."""
    unresolved_parts = set(data)
    wire_val = {}
    prior = 0

    # Set up int values as "knowns".
    for out, op, a, b in list(unresolved_parts):
        if a.isdigit():
            wire_val[a] = int(a)
        if b.isdigit():
            wire_val[b] = int(b)

    # Resolve while progress can be made.
    while unresolved_parts:
        # Infinite loop check
        if prior == len(unresolved_parts):
            self.debug("No progress!")
            break
        prior = len(unresolved_parts)

        for out, op, a, b in list(unresolved_parts):
            # Check if the wire can be resolved.
            if a not in wire_val:
                continue
            if b not in wire_val and op in ("AND", "OR"):
                continue

            # Resolve wire.
            unresolved_parts.remove((out, op, a, b))
            match op:
                case "VAL":
                    wire_val[out] = wire_val[a]
                case "NOT":
                    wire_val[out] = ~wire_val[a] & 65535
                case "RSHIFT":
                    wire_val[out] = wire_val[a] >> int(b)
                case "LSHIFT":
                    wire_val[out] = wire_val[a] << int(b)
                case "AND":
                    wire_val[out] = wire_val[a] & wire_val[b]
                case "OR":
                    wire_val[out] = wire_val[a] | wire_val[b]
    else:
        return wire_val["a"]
    raise RuntimeError


def solve(data: list[tuple[str, str, str, str]], part: int) -> int:
    """Solve for wire a after updating b."""
    val_a = get_wire(data)
    if part == 1:
        return val_a
    v2 = []
    for out, op, a, b in data:
        if op == "VAL" and out == "b":
            a = str(val_a)
        v2.append((out, op, a, b))
    return get_wire(v2)


PARSER = aoc.ParseOneWordPerLine(line_parser)
SAMPLE = """\
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> a
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
"""
TESTS = [(1, SAMPLE, 492), (2, SAMPLE, 492)]
