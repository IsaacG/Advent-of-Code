#!/bin/python
"""Advent of Code, Day 22: Sand Slabs."""
from __future__ import annotations

import collections
import copy
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9""",  # 0
]

LineType = int
InputType = list[LineType]


class Day22(aoc.Challenge):
    """Day 22: Sand Slabs."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=5),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=7),
        # aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    # INPUT_PARSER = aoc.parse_one_str_per_line
    # INPUT_PARSER = aoc.parse_one_str
    # INPUT_PARSER = aoc.parse_one_int
    # INPUT_PARSER = aoc.parse_one_str_per_line
    # INPUT_PARSER = aoc.parse_one_int_per_line
    # INPUT_PARSER = aoc.parse_multi_str_per_line
    # INPUT_PARSER = aoc.parse_re_group_str(r"(a) .* (b) .* (c)")
    # INPUT_PARSER = aoc.parse_re_findall_str(r"(a|b|c)")
    # INPUT_PARSER = aoc.parse_multi_int_per_line
    # INPUT_PARSER = aoc.parse_re_group_int(r"(\d+)")
    INPUT_PARSER = aoc.parse_re_findall_int(r"\d+")
    # INPUT_PARSER = aoc.parse_multi_mixed_per_line
    # INPUT_PARSER = aoc.parse_re_group_mixed(r"(foo) .* (\d+)")
    # INPUT_PARSER = aoc.parse_re_findall_mixed(r"\d+|foo|bar")
    # INPUT_PARSER = aoc.ParseBlocks([aoc.parse_one_str_per_line, aoc.parse_re_findall_int(r"\d+")])
    # INPUT_PARSER = aoc.ParseOneWord(aoc.Board.from_int_block)
    # INPUT_PARSER = aoc.parse_ascii_bool_map("#")
    # ---
    # INPUT_PARSER = aoc.CharCoordinatesParser("S.#")
    # (width, height), start, garden, rocks = parsed_input
    # max_x, max_y = width - 1, height - 1

    def part1(self, parsed_input: InputType) -> int:
        bricks = {num: [x1, y1, z1, x2, y2, z2] for num, (x1, y1, z1, x2, y2, z2) in enumerate(parsed_input)}
        assert all(a < 10 and b < 10 and d < 10 and e < 10 for a, b, c, d, e, f in bricks.values())
        assert all(x1 <= x2 and y1 <= y2 and z1 <= z2 for x1, y1, z1, x2, y2, z2 in bricks.values())
        
        brick_by_x_y = collections.defaultdict(list)
        for num, (x1, y1, z1, x2, y2, z2) in bricks.items():
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    brick_by_x_y[x, y].append(num)

        holding = collections.defaultdict(list)
        holding = {brick: [] for brick in bricks}
        todo = list(bricks)
        settled = set()
        step = 0
        while todo:
            step += 1
            if step > 10000:
                raise RuntimeError
            by_bottom = sorted(bricks, key=lambda x: bricks[x][2])
            by_top = sorted(bricks, key=lambda x: bricks[x][5])
            todo.sort(key=lambda x: bricks[x][2])
            for brick in todo:
                x1, y1, z1, x2, y2, z2 = bricks[brick]
                if bricks[brick][2] == 1:
                    todo.remove(brick)
                    settled.add(brick)
                    # print(f"Settled on ground: {brick} {bricks[brick]}")
                else:
                    potential_tops = {other for (x, y), others in brick_by_x_y.items() if x1 <= x <= x2 and y1 <= y <= y2 for other in others}
                    landed = {other for other in potential_tops & settled if bricks[other][5] + 1 == z1}
                    if landed:
                        todo.remove(brick)
                        settled.add(brick)
                        for other in landed:
                            holding[other].append(brick)
                        # print(f"{brick} {bricks[brick]} landed on {landed}")
                    else:
                        new_bottom = max((bricks[other][5] for other in potential_tops if bricks[other][5] < z1), default=0) + 1
                        if new_bottom < z1:
                            dist = z1 - new_bottom
                            bricks[brick][2] -= dist
                            bricks[brick][5] -= dist
                            # print(f"Move down {brick} {bricks[brick]} by {dist}")
                            break
        count = 0
        for brick in bricks:
            if all(
                bool({i for i, j in holding.items() if other in j and i != brick})
                for other in holding[brick]
            ):
                count += 1

        return count


    def part2(self, parsed_input: InputType) -> int:
        bricks = {num: [x1, y1, z1, x2, y2, z2] for num, (x1, y1, z1, x2, y2, z2) in enumerate(parsed_input)}
        assert all(a < 10 and b < 10 and d < 10 and e < 10 for a, b, c, d, e, f in bricks.values())
        assert all(x1 <= x2 and y1 <= y2 and z1 <= z2 for x1, y1, z1, x2, y2, z2 in bricks.values())
        
        brick_by_x_y = collections.defaultdict(list)
        for num, (x1, y1, z1, x2, y2, z2) in bricks.items():
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    brick_by_x_y[x, y].append(num)

        holding = {brick: [] for brick in bricks}
        todo = list(bricks)
        settled = set()
        step = 0
        while todo:
            step += 1
            if step > 10000:
                raise RuntimeError
            by_bottom = sorted(bricks, key=lambda x: bricks[x][2])
            by_top = sorted(bricks, key=lambda x: bricks[x][5])
            todo.sort(key=lambda x: bricks[x][2])
            for brick in todo:
                x1, y1, z1, x2, y2, z2 = bricks[brick]
                if bricks[brick][2] == 1:
                    todo.remove(brick)
                    settled.add(brick)
                    # print(f"Settled on ground: {brick} {bricks[brick]}")
                else:
                    potential_tops = {other for (x, y), others in brick_by_x_y.items() if x1 <= x <= x2 and y1 <= y <= y2 for other in others}
                    landed = {other for other in potential_tops & settled if bricks[other][5] + 1 == z1}
                    if landed:
                        todo.remove(brick)
                        settled.add(brick)
                        for other in landed:
                            holding[other].append(brick)
                        # print(f"{brick} {bricks[brick]} landed on {landed}")
                    else:
                        new_bottom = max((bricks[other][5] for other in potential_tops if bricks[other][5] < z1), default=0) + 1
                        if new_bottom < z1:
                            dist = z1 - new_bottom
                            bricks[brick][2] -= dist
                            bricks[brick][5] -= dist
                            # print(f"Move down {brick} {bricks[brick]} by {dist}")
                            break

        def fall_count(brick, holding):
            holding = holding.copy()

            chain = 0
            todo = set(holding.pop(brick))
            while todo:
                brick = todo.pop()
                alt_support = {alt_b for alt_b, alt_s in holding.items() if brick in alt_s}
                if not alt_support:
                    chain += 1
                    todo.update(holding.pop(brick))
            return chain


        count = 0
        for brick in bricks:
            count += fall_count(brick, holding)

        return count

# vim:expandtab:sw=4:ts=4
