#!/bin/python
"""Advent of Code: Day 07."""

from __future__ import annotations
import collections
import pathlib

import typer
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

LineType = str
InputType = list[LineType]
ROOT = pathlib.Path("/")


class DirectoryEntry:
    """Information about a directory."""

    def __init__(self, pwd: pathlib.Path, data: dir[pathlib.Path, DirectoryEntry]):
        self.pwd = pwd
        self.dirs = set()
        self.files = {}
        self.data = data

    def __repr__(self) -> str:
        return f"{self.pwd} {self.dirs} {self.files}"

    def size(self) -> int:
        """Return the recursive directory size."""
        size = sum(self.files.values())
        size += sum(self.data[self.pwd / child].size() for child in self.dirs)
        return size


class Day07(aoc.Challenge):
    """Day 7: No Space Left On Device. Parse filesystem output info."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=95437),
        aoc.TestCase(inputs=SAMPLE, part=2, want=24933642),
    ]

    INPUT_TYPES = LineType

    def directory_data(self, stdout: list[str]) -> dict[tuple, DirectoryEntry]:
        """Return the parsed filesystem details."""
        dirs = {}
        pwd = ROOT
        lines = collections.deque(stdout)
        while lines:
            words = lines.popleft().split()
            if words[0] == "$" and words[1] == "cd":
                if words[2] == "/":
                    pwd = ROOT
                elif words[2] == "..":
                    pwd = pwd.parent
                else:
                    pwd /= words[2]
            elif words[0] == "$" and words[1] == "ls":
                if pwd not in dirs:
                    dirs[pwd] = DirectoryEntry(pwd, dirs)
                while lines and not lines[0].startswith("$"):
                    type_or_size, name = lines.popleft().split()
                    if type_or_size == "dir":
                        dirs[pwd].dirs.add(name)
                    else:
                        dirs[pwd].files[name] = int(type_or_size)
            else:
                raise ValueError("Unrecognized command. {words}")
        return dirs

    def part1(self, parsed_input: InputType) -> int:
        """Return the sum of all dirs over 100000 in size."""
        dirs = self.directory_data(parsed_input)
        return sum(
            directory.size()
            for directory in dirs.values()
            if directory.size() <= 100000
        )

    def part2(self, parsed_input: InputType) -> int:
        """Return the smallest directory to remove which gives the needed space."""
        dirs = self.directory_data(parsed_input)

        # space_total = 70000000
        # target = 30000000
        # space_used = dirs[tuple()].size()
        # already_free = space_total - space_used
        # to_free = target - already_free
        to_free = 30000000 - 70000000 + dirs[ROOT].size()

        return min(
            directory.size()
            for directory in dirs.values()
            if directory.size() >= to_free
        )


if __name__ == "__main__":
    typer.run(Day07().run)

# vim:expandtab:sw=4:ts=4
