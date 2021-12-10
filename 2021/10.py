#!/bin/python
"""Advent of Code: Day 10."""

import collections
import functools
import math
import re
from typing import Any, Callable

import typer

from lib import aoc

InputType = list[int]

SAMPLE = ["""\
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
"""]

class Day10(aoc.Challenge):

    DEBUG = True

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=26397),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=288957),
    )

    # Convert lines to type:
    INPUT_TYPES = str
    # Split on whitespace and coerce types:
    # INPUT_TYPES = [str, int]
    # Apply a transform function
    # TRANSFORM = lambda _, l: (l[0], int(l[1:]))

    def part1(self, lines: InputType) -> int:
        value = {')': 3, ']': 57, '}': 1197, '>': 25137}
        sums = 0
        for line in lines:
          stack = []
          r = {')': '(', ']': '[', '}': '{', '>': '<'}
          for c in line:
            if c in '[{(<':
              stack.append(c)
            if c in ']})>':
              if not stack:
                sums += value[c]
                break
              elif stack[-1] == r[c]:
                stack.pop()
              else:
                sums += value[c]
                break
        return sums

    def part2(self, lines: InputType) -> int:
        value = {')': 3, ']': 57, '}': 1197, '>': 25137}
        sums = 0
        invalid_lines = []
        for line in lines:
          stack = []
          r = {')': '(', ']': '[', '}': '{', '>': '<'}
          for c in line:
            if c in '[{(<':
              stack.append(c)
            if c in ']})>':
              if not stack:
                sums += value[c]
                invalid_lines.append(line)
                break
              elif stack[-1] == r[c]:
                stack.pop()
              else:
                sums += value[c]
                invalid_lines.append(line)
                break
        
        scores = []
        for line in lines:
          if line in invalid_lines:
            continue
          stack = []
          r = {')': '(', ']': '[', '}': '{', '>': '<'}
          for c in line:
            if c in '[{(<':
              stack.append(c)
            if c in ']})>':
              if not stack:
                print("error")
              elif stack[-1] == r[c]:
                stack.pop()
              else:
                print("error")
          vals = {'(': 1, '[': 2, '{':3, '<': 4}
          sums = 0
          for c in reversed(stack):
            sums *= 5
            sums += vals[c]
          scores.append(sums)
        return sorted(scores)[len(scores)//2]
        return sums
                
        

    def parse_input(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return super().parse_input(puzzle_input)

        return puzzle_input.splitlines()
        return puzzle_input
        return [int(i) for i in puzzle_input.splitlines()]

        mutate = lambda x: (x[0], int(x[1])) 
        return [mutate(line.split()) for line in puzzle_input.splitlines()]


if __name__ == "__main__":
    typer.run(Day10().run)
