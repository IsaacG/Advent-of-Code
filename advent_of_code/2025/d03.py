#!/bin/python
"""Advent of Code, Day 3: Lobby."""
PARSER = str.splitlines


def solve(data: list[str], part: int) -> int:
    total = 0
    size = 2 if part == 1 else 12
    for line in data:
        digits = []
        for save in range(size)[::-1]:
            biggest = max(line[:-save] if save else line)
            digits.append(biggest)
            line = line[line.index(biggest) + 1:]

        total += int("".join(digits))
    return total


SAMPLE = """\
987654321111111
811111111111119
234234234234278
818181911112111"""
TESTS = [(1, SAMPLE, 357), (2, SAMPLE, 3121910778619)]
# vim:expandtab:sw=4:ts=4
