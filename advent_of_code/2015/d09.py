#!/bin/python
"""Advent of Code: Day 09. All in a Single Night. Compute the cost of visiting all cities.."""
import itertools
import re


def solve(data: list[int], part: int) -> int:
    """Return the shortest/longest route."""
    if part == 1:
        return min(data)
    return max(data)


def input_parser(data: str) -> list[int]:
    """Parse the input and generate the total cost for each route."""
    distances = {}
    line_re = re.compile(r"^(.+) to (.+) = (\d+)$")
    locations: set[str] = set()
    for line in data.splitlines():
        m = line_re.match(line)
        assert m
        src, dst, dist_raw = m.groups()
        dist = int(dist_raw)

        distances[src, dst] = dist
        distances[dst, src] = dist
        locations.add(src)
        locations.add(dst)

    return [
        sum(
            distances[src, dst]
            for src, dst in zip(order, order[1:])
        )
        for order in itertools.permutations(locations, len(locations))
    ]


SAMPLE = """\
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
"""
TESTS = [(1, SAMPLE, 605), (2, SAMPLE, 982)]
