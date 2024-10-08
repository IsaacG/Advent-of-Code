#!/bin/python
"""Advent of Code: Day 07."""

from __future__ import annotations
import collections
import pathlib

from lib import aoc

SAMPLE = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

InputType = dict[pathlib.Path, int]
ROOT = pathlib.Path("/")


class Day07(aoc.Challenge):
    """Day 7: No Space Left On Device. Parse filesystem output info."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=95437),
        aoc.TestCase(inputs=SAMPLE, part=2, want=24933642),
    ]

    def input_parser(self, puzzle_input: str) -> InputType:
        """Return the parsed filesystem details."""
        dirs: InputType = collections.defaultdict(int)
        pwd = ROOT
        for line in puzzle_input.splitlines():
            match line.split():
                case ["$", "cd", ".."]:
                    pwd = pwd.parent
                case ["$", "cd", name]:
                    pwd /= name
                case [maybe_size, _] if maybe_size.isdigit():
                    size = int(maybe_size)
                    dirs[pwd] += size
                    for p in pwd.parents:
                        dirs[p] += size
        return dirs

    def part1(self, puzzle_input: InputType) -> int:
        """Return the sum of all dirs over 100000 in size."""
        return sum(
            size
            for size in puzzle_input.values()
            if size <= 100000
        )

    def part2(self, puzzle_input: InputType) -> int:
        """Return the smallest directory to remove which gives the needed space."""
        # space_total = 70000000
        # target = 30000000
        # space_used = dirs[tuple()].rsize()
        # already_free = space_total - space_used
        # to_free = target - already_free
        to_free = 30000000 - 70000000 + puzzle_input[ROOT]

        return min(
            size
            for size in puzzle_input.values()
            if size >= to_free
        )
