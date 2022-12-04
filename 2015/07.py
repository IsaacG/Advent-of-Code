#!/bin/python
"""Advent of Code: Day 07."""

import typer
from lib import aoc

SAMPLE = ["""\
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> a
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
"""]

LineType = tuple[str, str, str, str]
InputType = list[LineType]


class Day07(aoc.Challenge):
    """Day 7: Some Assembly Required. Solve circuit outputs."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=492),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=492),
    ]

    def part1(self, parsed_input: InputType) -> int:
        """Solve for wire a."""
        unresolved_parts = set(parsed_input)
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

    def part2(self, parsed_input: InputType) -> int:
        """Solve for wire a after updating b."""
        val_a = self.part1(parsed_input)
        v2 = []
        for out, op, a, b in parsed_input:
            if op == "VAL" and out == "b":
                a = str(val_a)
            v2.append((out, op, a, b))
        return self.part1(v2)

    def line_parser(self, line: str) -> LineType:
        """Parse one line."""
        inp, out = line.split(" -> ")
        parts = inp.split()
        if len(parts) == 1:
            return (out, "VAL", parts[0], "0")
        if len(parts) == 2:
            return (out, "NOT", parts[1], "0")
        return (out, parts[1], parts[0], parts[2])


if __name__ == "__main__":
    typer.run(Day07().run)

# vim:expandtab:sw=4:ts=4
