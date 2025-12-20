#!/bin/python
"""Advent of Code, Day 9: Stream Processing."""


def solve(data: str, part: int) -> int | str:
    """Parse bracket matching in a string."""
    tokens = iter(data)

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

    return total_score if part == 1 else garbage_count


TESTS = [
    (1, '{}', 1),
    (1, '{{{}}}', 6),
    (1, '{{},{}}', 5),
    (1, '{{{},{},{{}}}}', 16),
    (1, '{<a>,<a>,<a>,<a>}', 1),
    (1, '{{<ab>},{<ab>},{<ab>},{<ab>}}', 9),
    (1, '{{<!!>},{<!!>},{<!!>},{<!!>}}', 9),
    (1, '{{<a!>},{<a!>},{<a!>},{<ab>}}', 3),
    (2, '<>', 0),
    (2, '<random characters>', 17),
    (2, '<<<<>', 3),
    (2, '<{!>}>', 2),
    (2, '<!!>', 0),
    (2, '<!!!>>', 0),
    (2, '<{o"i!a,<{i<a>', 10),
]
# vim:expandtab:sw=4:ts=4
