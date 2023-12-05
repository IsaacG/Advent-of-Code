#!/bin/python
"""Advent of Code, Day 5: If You Give A Seed A Fertilizer."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4""",  # 2
    '79',  # 3
    '14',  # 4
    '55',  # 5
    '13',  # 6
    'seed-to-soil map:',  # 7
    'seed-to-soil map',  # 8
    """\
50 98 2
52 50 48""",  # 9
    '50',  # 10
    '98',  # 11
    '2',  # 12
    '98',  # 13
    '98',  # 14
    '99',  # 15
    '50',  # 16
    '50',  # 17
    '51',  # 18
    '98',  # 19
    '50',  # 20
    '99',  # 21
    '51',  # 22
    '50',  # 23
    '48',  # 24
    '50',  # 25
    '51',  # 26
    '96',  # 27
    '97',  # 28
    '52',  # 29
    '48',  # 30
    '52',  # 31
    '53',  # 32
    '98',  # 33
    '99',  # 34
    '53',  # 35
    '55',  # 36
    '10',  # 37
    '10',  # 38
    """\
seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51""",  # 39
    '79',  # 40
    '81',  # 41
    '14',  # 42
    '14',  # 43
    '55',  # 44
    '57',  # 45
    '13',  # 46
    '13',  # 47
    '79',  # 48
    '81',  # 49
    '81',  # 50
    '81',  # 51
    '74',  # 52
    '78',  # 53
    '78',  # 54
    '82',  # 55
    '14',  # 56
    '14',  # 57
    '53',  # 58
    '49',  # 59
    '42',  # 60
    '42',  # 61
    '43',  # 62
    '43',  # 63
    '55',  # 64
    '57',  # 65
    '57',  # 66
    '53',  # 67
    '46',  # 68
    '82',  # 69
    '82',  # 70
    '86',  # 71
    '13',  # 72
    '13',  # 73
    '52',  # 74
    '41',  # 75
    '34',  # 76
    '34',  # 77
    '35',  # 78
    '35',  # 79
]

LineType = int
InputType = list[LineType]


class Day05(aoc.Challenge):
    """Day 5: If You Give A Seed A Fertilizer."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=35),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=46),
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
    # INPUT_PARSER = aoc.parse_re_findall_int(r"\d+")
    # INPUT_PARSER = aoc.parse_multi_mixed_per_line
    # INPUT_PARSER = aoc.parse_re_group_mixed(r"(foo) .* (\d+)")
    # INPUT_PARSER = aoc.parse_re_findall_mixed(r"\d+|foo|bar")
    # INPUT_PARSER = aoc.ParseBlocks([aoc.parse_one_str_per_line, aoc.parse_re_findall_int(r"\d+")])
    # INPUT_PARSER = aoc.ParseOneWord(aoc.Board.from_int_block)
    # INPUT_PARSER = aoc.parse_ascii_bool_map("#")

    def part1(self, parsed_input: InputType) -> int:
        seeds, data = parsed_input
        vals = set(seeds)
        for block in data:
            new = set()
            for dst, src, rang in block:
                for val in list(vals):
                    if src <= val < src + rang:
                        vals.remove(val)
                        new.add(val + dst - src)
            new.update(vals)
            vals = new
        return min(vals)

        print(f"{parsed_input!r}")
        return 0

    def part2(self, parsed_input: InputType) -> int:
        seeds, data = parsed_input
        vals = []
        for i in range(0, len(seeds), 2):
            vals.append((seeds[i], seeds[i] + seeds[i + 1] - 1))
        vals.sort()
        new = vals

        for block in data:
            block.sort(key=lambda x: x[1])
            block_q = collections.deque(block)
            src_end = -1

            vals_q = collections.deque(sorted(new))
            print(vals_q)
            new = []

            while vals_q:
                start, end = vals_q.popleft()
                while block_q and start > src_end:
                    dst_start, src_start, rang = block_q.popleft()
                    src_end = src_start + rang - 1
                    dst_delta = dst_start - src_start
                    print(f"TRANS {src_start}-{src_end} > {dst_delta}")
                if start > src_end:
                    assert not block_q
                    print(f"Copy {start}-{end}")
                    new.append((start, end))
                elif end < src_start:
                    print(f"Copy {start}-{end}")
                    new.append((start, end))
                else:
                    overlap_start = max(start, src_start)
                    overlap_end = min(end, src_end)
                    if start < overlap_start:
                        print(f"Copy {start}-{overlap_start - 1}")
                        new.append((start, overlap_start - 1))
                    print(f"Shift {overlap_start}-{overlap_end} to {overlap_start + dst_delta}-{overlap_end + dst_delta}")
                    new.append((overlap_start + dst_delta, overlap_end + dst_delta))
                    if end > overlap_end:
                        print(f"Reprocess {overlap_end + 1}-{end}")
                        vals_q.appendleft((overlap_end + 1, end))

            print("===")
        result = min(v[0] for v in new)
        assert result != 18458048
        return result

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        blocks = puzzle_input.split("\n\n")
        seeds = [int(i) for i in blocks[0].removeprefix("seeds:").strip().split()]
        data = []
        for block in blocks[1:]:
            data.append([[int(i) for i in line.split()] for line in sorted(block.splitlines()[1:])])
        return seeds, data

# vim:expandtab:sw=4:ts=4
