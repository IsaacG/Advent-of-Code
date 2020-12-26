#!/bin/pypy3
"""Day 2: 1202 Program Alarm."""


import typer
from typing import List

import aoc
import intcode


SAMPLE = ['1,9,10,3,2,3,11,0,99,30,40,50']


class Day02(aoc.Challenge):
  """Implement an Intcode computer."""

  TRANSFORM = str

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=3500),
  )

  def run_computer(self, memory: List[int], noun: int, verb: int) -> int:
    """Run the computer with a given noun, verb."""
    memory[1] = noun
    memory[2] = verb
    computer = intcode.Intcode(memory)
    return computer.run()

  def part1(self, memory: List[int]) -> int:
    """Run the computer with fixed noun, verb."""
    if self.testing:
      noun, verb = memory[1:3]
    else:
      noun, verb = 12, 2
    return self.run_computer(memory, noun, verb)

  def part2(self, memory: List[int]) -> int:
    """Brute force the noun, verb to get the computer to generate `want`."""
    want = 19690720  # https://en.wikipedia.org/wiki/Apollo_11
    for noun in range(100):
      for verb in range(100):
        if self.run_computer(memory, noun, verb) == want:
          return 100 * noun + verb

  def preparse_input(self, x) -> List[int]:
    """Return the first row as a list of ints."""
    return [int(num) for num in x[0].split(',')]


if __name__ == '__main__':
  typer.run(Day02().run)

# vim:ts=2:sw=2:expandtab
