#!/bin/python
"""Advent of Code, Day 4: Printing Department."""

from lib import aoc

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


class Day04(aoc.Challenge):
    """Day 4: Printing Department."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=13),
        aoc.TestCase(part=2, inputs=SAMPLE, want=43),
    ]
    INPUT_PARSER = aoc.CoordinatesParser(chars=None, origin_top_left=True)

    def solver(self, puzzle_input: aoc.Map, part_one: bool) -> int:
        papers = puzzle_input.coords["@"]

        def moveable():
            return {
                paper
                for paper in papers
                if sum(
                    neighbor in papers
                    for neighbor in puzzle_input.neighbors(paper, aoc.ALL_NEIGHBORS_T)
                ) < 4
            }

        if part_one:
            return len(moveable())

        initial = len(papers)
        while True:
            can_move = moveable()
            if not can_move:
                return initial - len(papers)
            papers -= can_move

# vim:expandtab:sw=4:ts=4
