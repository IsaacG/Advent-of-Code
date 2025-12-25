#!/bin/python
"""Advent of Code: Day 07. No Space Left On Device. Parse filesystem output info."""
import collections
import pathlib

from lib import aoc
InputType = dict[pathlib.Path, int]
ROOT = pathlib.Path("/")


def input_parser(data: str) -> InputType:
    """Return the parsed filesystem details."""
    dirs: InputType = collections.defaultdict(int)
    pwd = ROOT
    for line in data.splitlines():
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


def solve(data: InputType, part: int) -> int:
    """Solve the parts."""
    if part == 1:
        # Return the sum of all dirs over 100000 in size.
        return sum(
            size
            for size in data.values()
            if size <= 100000
        )

    # Return the smallest directory to remove which gives the needed space.
    # space_total = 70000000
    # target = 30000000
    # space_used = dirs[tuple()].rsize()
    # already_free = space_total - space_used
    # to_free = target - already_free
    to_free = 30000000 - 70000000 + data[ROOT]

    return min(
        size
        for size in data.values()
        if size >= to_free
    )

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
TESTS = [(1, SAMPLE, 95437), (2, SAMPLE, 24933642)]
