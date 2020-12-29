#!/usr/bin/env pypy

import collections
import functools
import math
import re
import typer
from typing import Any, Callable, Dict, List

import intcode
from lib import aoc

SAMPLE = [""]

class Day05(aoc.Challenge):

  TESTS = (
    aoc.TestCase(inputs='4,0,99', part=1, want=4),
    aoc.TestCase(inputs='04,2,99', part=1, want=99),
    aoc.TestCase(inputs='104,6,99', part=1, want=6),
    aoc.TestCase(inputs='1002,7,3,5,104,5,99,33', part=1, want=99),
  )

  def run_computer(self, memory: List[int]) -> int:
    """Run the computer with a given noun, verb."""
    computer = intcode.Computer(memory, debug=0)
    # First input: 1
    computer.inputs.append(1)
    computer.run()
    # Read the last output.
    return computer.outputs.pop()

  def part1(self, memory: List[int]) -> int:
    """Run the computer with fixed noun, verb."""
    return self.run_computer(memory)

  def part2(self, memory: List[int]) -> int:
    return 0

  def preparse_input(self, x) -> List[int]:
    """Return the first row as a list of ints."""
    return [int(num) for num in x[0].split(',')]


if __name__ == '__main__':
  typer.run(Day05().run)

# vim:ts=2:sw=2:expandtab
