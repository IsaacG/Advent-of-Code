#!/bin/python
"""Advent of Code, Day 1: Inverse Captcha."""


def solve(data: int, part: int) -> int:
    """Sum all digits which match the corresponding digit."""
    # Part one: compare digits to subsequent digit.
    # Part two: compare digits to digits halfway around the list.
    numbers = str(data)
    offset = 1 if part == 1 else len(numbers) // 2
    shifted_list = numbers[offset:] + numbers[:offset]
    return sum(
        int(digit)
        for digit, corresponding in zip(numbers, shifted_list)
        if digit == corresponding
    )


TESTS = [
    (1, "1122", 3),
    (1, "1111", 4),
    (1, "1234", 0),
    (1, "91212129", 9),
    (2, "1212", 6),
    (2, "1221", 0),
    (2, "123425", 4),
    (2, "123123", 12),
    (2, "12131415", 4),
]
# vim:expandtab:sw=4:ts=4
