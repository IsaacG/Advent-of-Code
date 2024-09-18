#!/bin/python
"""Advent of Code, Day 9: Stream Processing."""

from lib import aoc

SAMPLE: tuple[list[tuple[str, int]], ...] = (
    [
        ('{}', 1),
        ('{{{}}}', 6),
        ('{{},{}}', 5),
        ('{{{},{},{{}}}}', 16),
        ('{<a>,<a>,<a>,<a>}', 1),
        ('{{<ab>},{<ab>},{<ab>},{<ab>}}', 9),
        ('{{<!!>},{<!!>},{<!!>},{<!!>}}', 9),
        ('{{<a!>},{<a!>},{<a!>},{<ab>}}', 3),
    ],
    [
        ('<>', 0),
        ('<random characters>', 17),
        ('<<<<>', 3),
        ('<{!>}>', 2),
        ('<!!>', 0),
        ('<!!!>>', 0),
        ('<{o"i!a,<{i<a>', 10),
    ]
)


class Day09(aoc.Challenge):
    """Day 9: Stream Processing."""

    TESTS = [
        aoc.TestCase(inputs=data, part=part, want=int(val))
        for part, pairs in enumerate(SAMPLE, 1)
        for data, val in pairs
    ]
    INPUT_PARSER = aoc.parse_one_str

    def solver(self, parsed_input: str, part_one: bool) -> int | str:
        """Parse bracket matching in a string."""
        tokens = iter(parsed_input)

        total_score = 0
        bracket_depth = 0
        garbage_group = False
        garbage_count = 0

        for char in tokens:
            if char == "!":
                next(tokens)
            elif garbage_group:
                if char == ">":
                    garbage_group = False
                else:
                    garbage_count += 1
            elif char == "<":
                garbage_group = True
            elif char == "{":
                bracket_depth += 1
            elif char == "}":
                total_score += bracket_depth
                bracket_depth -= 1

        return total_score if part_one else garbage_count

# vim:expandtab:sw=4:ts=4
