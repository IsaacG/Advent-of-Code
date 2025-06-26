#!/bin/python
"""Advent of Code, Day 6: Chronal Coordinates."""

from lib import aoc

SAMPLE = """\
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9"""

LineType = list[int]
InputType = list[LineType]


class Day06(aoc.Challenge):
    """Day 6: Chronal Coordinates."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=17),
        aoc.TestCase(inputs=SAMPLE, part=2, want=0),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    def part1(self, parsed_input: InputType) -> int:
        dist = max(
            abs(ax - bx) + abs(ay - by)
            for ax, ay in parsed_input
            for bx, by in parsed_input
        )
        self.debug(f"{dist=}")

        num = len(parsed_input)
        counts = [0] * num
        to_explore = [{i, } for i in parsed_input]
        processed: set[tuple[int, int]] = set()

        for _ in range(2 + dist // 2):
            for i in range(num):
                todo = to_explore[i]
                next_todo = set()
                for x, y in todo:
                    pass
