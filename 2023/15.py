#!/bin/python
"""Advent of Code, Day 15: Lens Library."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    '0',  # 0
    '17',  # 1
    '256',  # 2
    'HASH',  # 3
    '0',  # 4
    'H',  # 5
    '72',  # 6
    '72',  # 7
    '17',  # 8
    '1224',  # 9
    '1224',  # 10
    '256',  # 11
    'A',  # 12
    '65',  # 13
    '265',  # 14
    '17',  # 15
    '4505',  # 16
    '4505',  # 17
    '256',  # 18
    'S',  # 19
    '83',  # 20
    '236',  # 21
    '17',  # 22
    '4012',  # 23
    '4012',  # 24
    '256',  # 25
    'H',  # 26
    '72',  # 27
    '244',  # 28
    '17',  # 29
    '4148',  # 30
    '4148',  # 31
    '256',  # 32
    'HASH',  # 33
    'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7',  # 34
    'rn=1',  # 35
    'cm-',  # 36
    'qp=3',  # 37
    'cm=2',  # 38
    'qp-',  # 39
    'pc=4',  # 40
    'ot=9',  # 41
    'ab=5',  # 42
    'pc-',  # 43
    'pc=6',  # 44
    'ot=7',  # 45
]

LineType = int
InputType = list[LineType]


class Day15(aoc.Challenge):
    """Day 15: Lens Library."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs="HASH", part=1, want=52),
        aoc.TestCase(inputs="rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7", part=1, want=1320),
        aoc.TestCase(inputs="rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7", part=2, want=145),
    ]

    # INPUT_PARSER = aoc.parse_one_str_per_line
    INPUT_PARSER = aoc.parse_one_str
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

    def hash(self, word: str) -> int:
        value = 0
        for char in word:
            value += ord(char)
            value *= 17
            value %= 256
        return value

    def part1(self, parsed_input: InputType) -> int:
        return sum(self.hash(word) for word in parsed_input.split(","))

    def part2(self, parsed_input: InputType) -> int:
        boxes = [[] for _ in range(256)]
        for word in parsed_input.split(","):
            if word.endswith("-"):
                label = word.removesuffix("-")
                box = self.hash(label)
                boxes[box] = [(lens_label, length) for lens_label, length in boxes[box] if lens_label != label]
            else:
                label, length = word.split("=")
                box = self.hash(label)
                if any(l_label == label for l_label, _ in boxes[box]):
                    boxes[box] = [(l_label, length if l_label == label else l_length) for l_label, l_length in boxes[box]]
                else:
                    boxes[box].append((label, length))
            # print(f"{word}:\n{', '.join(str((idx, box)) for idx, box in enumerate(boxes) if box)}\n")
        result = 0
        for idx_box, box in enumerate(boxes, start=1):
            # result += sum(idx_box * idx_lens * int(length) for idx_lens, (_, length) in enumerate(box, start=1))
            for idx_lens, (_, length) in enumerate(box, start=1):
                # print(f"{idx_box=} * {idx_lens=} * {length=}")
                result += idx_box * idx_lens * int(length)
        return result


    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        raise NotImplementedError

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return super().input_parser(puzzle_input)
        return puzzle_input.splitlines()
        return puzzle_input
        return [int(i) for i in puzzle_input.splitlines()]
        mutate = lambda x: (x[0], int(x[1])) 
        return [mutate(line.split()) for line in puzzle_input.splitlines()]
        # Words: mixed str and int
        return [
            tuple(
                int(i) if i.isdigit() else i
                for i in line.split()
            )
            for line in puzzle_input.splitlines()
        ]
        # Regex splitting
        patt = re.compile(r"(.*) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.")
        return [
            tuple(
                int(i) if i.isdigit() else i
                for i in patt.match(line).groups()
            )
            for line in puzzle_input.splitlines()
        ]

# vim:expandtab:sw=4:ts=4
