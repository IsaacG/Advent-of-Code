#!/bin/python
"""Advent of Code, Day 25: Full of Hot Air."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

import typer
from lib import aoc

SAMPLE = [
    """\
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122""",  """\
1 1              
2 2              
1= 3             
1- 4             
10 5             
11 6             
12 7             
2= 8             
2- 9             
20 10             
1=0 15            
1-0 20            
1=11-2 2022         
1-0---0 12345        
1121-1110-1=0 314159265  
1=-0-2     1747
 12111      906
  2=0=      198
    21       11
  2=01      201
   111       31
 20012     1257
   112       32
 1=-1=      353
  1-12      107
    12        7
    1=        3
   122       37"""
]

LineType = int
InputType = list[LineType]


class Day25(aoc.Challenge):
    """Day 25: Full of Hot Air."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want="2=-1=0"),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=0),
    ]

    INPUT_PARSER = aoc.parse_one_str_per_line

    def encode(self, dec: int) -> str:
        out = []
        while dec:
            dec, rem = divmod(dec, 5)
            if rem in (0, 1, 2):
                out.append(str(rem))
            if rem == 3:
                out.append("=")
                dec += 1
            if rem == 4:
                out.append("-")
                dec += 1
        out.reverse()
        return "".join(out)

    def to_dec(self, snafu: str) -> int:
        total = 0
        for char in snafu:
            total *= 5
            total += {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}[char]
        return total

    def part1(self, parsed_input: InputType) -> int:
        for line in SAMPLE[1].splitlines():
            sn, dc = line.strip().split()
            assert int(dc) == self.to_dec(sn)
            assert sn == self.encode(int(dc)), f"encode({dc}) = {self.encode(int(dc))}, want {sn}"
        s = sum(self.to_dec(line) for line in parsed_input)
        print(s)

        return self.encode(s)
        

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

    # def line_parser(self, line: str):
    #     pass


if __name__ == "__main__":
    typer.run(Day25().run)

# vim:expandtab:sw=4:ts=4
