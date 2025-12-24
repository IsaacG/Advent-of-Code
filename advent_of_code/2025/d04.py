#!/bin/python
"""Advent of Code, Day 4: Printing Department."""
from lib import aoc


def solve(data: aoc.Map, part: int) -> int:
    papers = data.coords["@"]

    def moveable():
        return {
            paper
            for paper in papers
            if sum(
                neighbor in papers
                for neighbor in data.neighbors(paper, aoc.ALL_NEIGHBORS_T)
            ) < 4
        }

    if part == 1:
        return len(moveable())

    initial = len(papers)
    while True:
        can_move = moveable()
        if not can_move:
            return initial - len(papers)
        papers -= can_move


SAMPLE = """\
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""
TESTS = [(1, SAMPLE, 13), (2, SAMPLE, 43)]
# vim:expandtab:sw=4:ts=4
