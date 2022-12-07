#!/bin/python
"""Advent of Code: Day 07."""

import dataclasses
import collections
import functools
import math
import re

import typer
from lib import aoc

SAMPLE = [
    '$ system-update --please --pretty-please-with-sugar-on-top',  # 0
    ': No space left on device',  # 1
    """\
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
7214296 k""",  # 2
    '/',  # 3
    '$',  # 4
    'cd',  # 5
    'cd x',  # 6
    'x',  # 7
    'cd ..',  # 8
    'cd /',  # 9
    '/',  # 10
    'ls',  # 11
    '123 abc',  # 12
    'abc',  # 13
    '123',  # 14
    'dir xyz',  # 15
    'xyz',  # 16
    """\
- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)""",  # 17
    '/',  # 18
    'a',  # 19
    'd',  # 20
    '/',  # 21
    'e',  # 22
    'a',  # 23
    'e',  # 24
    'i',  # 25
    'a',  # 26
    'f',  # 27
    'g',  # 28
    'h.lst',  # 29
    'i',  # 30
    'a',  # 31
    'e',  # 32
    'i',  # 33
    'd',  # 34
    '/',  # 35
    'a',  # 36
    'e',  # 37
]

LineType = int
InputType = list[LineType]


class Dir:
    def __init__(self, pwd):
        self.pwd = pwd
        self.dirs = set()
        self.files = {}

    def __repr__(self):
        return f"{self.pwd} {self.dirs} {self.files}"

    def size(self, data):
        t = sum(self.files.values())
        t += sum(data[self.pwd + (i,)].size(data) for i in self.dirs)
        return t

class Day07(aoc.Challenge):
    """Day 7: No Space Left On Device."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[2], part=1, want=95437),
        aoc.TestCase(inputs=SAMPLE[2], part=2, want=24933642),
    ]

    # Convert lines to type:
    INPUT_TYPES = LineType
    # Split on whitespace and coerce types:
    # INPUT_TYPES = [str, int]
    # Apply a transform function
    # TRANSFORM = lambda _, l: (l[0], int(l[1:]))


    def part1(self, parsed_input: InputType) -> int:
        dirs = {}
        pwd = []
        lines = collections.deque(parsed_input)
        while lines:
            words = lines.popleft().split()
            if words[0] == "$":
                if words[1] == "cd":
                    if words[2] == "/":
                        pwd = []
                    elif words[2] == "..":
                        pwd.pop()
                    else:
                        pwd.append(words[2])
                    self.debug(f"{words} {pwd}")
                elif words[1] == "ls":
                    if tuple(pwd) not in dirs:
                        dirs[tuple(pwd)] = Dir(tuple(pwd))
                    while lines and not lines[0].startswith("$"):
                        a, name = lines.popleft().split()
                        if a == "dir":
                            dirs[tuple(pwd)].dirs.add(name)
                        else:
                            dirs[tuple(pwd)].files[name] = int(a)
        print(dirs)
        return sum(d.size(dirs) for name, d in dirs.items() if d.size(dirs) <= 100000)
                

    def part2(self, parsed_input: InputType) -> int:
        fs_size = 70000000
        need = 30000000
        dirs = {}
        pwd = []
        lines = collections.deque(parsed_input)
        while lines:
            words = lines.popleft().split()
            if words[0] == "$":
                if words[1] == "cd":
                    if words[2] == "/":
                        pwd = []
                    elif words[2] == "..":
                        pwd.pop()
                    else:
                        pwd.append(words[2])
                    self.debug(f"{words} {pwd}")
                elif words[1] == "ls":
                    if tuple(pwd) not in dirs:
                        dirs[tuple(pwd)] = Dir(tuple(pwd))
                    while lines and not lines[0].startswith("$"):
                        a, name = lines.popleft().split()
                        if a == "dir":
                            dirs[tuple(pwd)].dirs.add(name)
                        else:
                            dirs[tuple(pwd)].files[name] = int(a)
        root_size = dirs[tuple()].size(dirs)
        unused = fs_size - root_size
        to_free = need- unused
        return min(d.size(dirs) for name, d in dirs.items() if d.size(dirs) >= to_free)
                


    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return puzzle_input.splitlines()

    # def line_parser(self, line: str) -> LineType:
    #     """If defined, use this to parse single lines."""
    #     return (
    #         int(i) if i.isdigit() else i
    #         for i in PARSE_RE.findall(line)
    #     )


if __name__ == "__main__":
    typer.run(Day07().run)

# vim:expandtab:sw=4:ts=4
