#!/bin/python
"""Advent of Code: Day 08."""

import collections
import functools
import math
import re
from typing import Any, Callable

import typer

from lib import aoc

InputType = list[int]

SAMPLE = """\
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""

class Day08(aoc.Challenge):

    DEBUG = True

    TESTS = (
        aoc.TestCase(inputs=SAMPLE, part=1, want=26),
        aoc.TestCase(inputs=SAMPLE, part=2, want=61229),
    )

    # Convert lines to type:
    INPUT_TYPES = int
    # Split on whitespace and coerce types:
    # INPUT_TYPES = [str, int]
    # Apply a transform function
    # TRANSFORM = lambda _, l: (l[0], int(l[1:]))

    def part1(self, lines: InputType) -> int:
        x = []
        for line in lines:
          a, b = line
          for p in b:
            if len(p) in (2, 3, 4, 7):
              x.append(p)
        return len(x)
            
    def part2(self, lines: InputType) -> int:
        x = []
        for line in lines:
          x1 = []
          known = {}
          a, b = line
          for p in a:
            if len(p) == 2:
              known[1] = set(p)
            if len(p) == 3:
              known[7] = set(p)
            if len(p) == 4:
              known[4] = set(p)
            if len(p) == 7:
              known[8] = set(p)
          for p in a:
            if len(p) == 6:
              if set(p).issuperset(known[4]):
                known[9] = set(p)
              elif known[1] < set(p):
                known[0] = set(p)
              else:
                known[6] = set(p)
          for p in a:
            if len(p) == 5:
              if known[1] < set(p):
                known[3] = set(p)
              elif set(p).issubset(known[6]):
                known[5] = set(p)
              else:
                known[2] = set(p)
          assert len(known) >= 9, sorted(known)
          default = None
          if len(known) == 9:
            default = [i for i in range(10) if i not in known][0]
            print(f"len 9 => {known.keys()} => {default}")

          for p in b:
            y = [k for k, v in known.items() if v == set(p)]
            if y:
              x1.append(y[0])
            else:
              x1.append(default)
          print("".join(str(s) for s in  x1))
          x.append(int("".join(str(s) for s in  x1)))

        return sum(x)
            

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        out = []
        for line in puzzle_input.splitlines():
            a, b = line.split(" | ")
            out.append((a.split(), b.split()))
        return out


if __name__ == "__main__":
    typer.run(Day08().run)
