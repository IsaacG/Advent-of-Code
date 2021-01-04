#!/usr/bin/env python
"""Day 2: 1202 Program Alarm.

Implement an Intcode computer.
"""

import asyncio
import typer

import intcode
from lib import aoc


SAMPLE = ['1,9,10,3,2,3,11,0,99,30,40,50']


class Day02(intcode.Challenge):

  TESTS = (aoc.TestCase(inputs=SAMPLE[0], part=1, want=3500),)

  def run_with(self, computer: intcode.Computer, noun, verb) -> int:
    """Run a copy of the computer, with a given noun, verb and return mem[0]."""
    computer = computer.copy()
    computer.memory[1], computer.memory[2] = noun, verb
    asyncio.run(computer.run())
    return computer.memory[0]

  def part1(self, computer: intcode.Computer) -> int:
    """Run the computer with fixed noun, verb."""
    if self.testing:
      noun, verb = 9, 10
    else:
      noun, verb = 12, 2
    return self.run_with(computer, noun, verb)

  def part2(self, computer: intcode.Computer) -> int:
    """Brute force the noun, verb to get the computer to generate `want`."""
    want = 19690720  # https://en.wikipedia.org/wiki/Apollo_11
    for noun in range(100):
      for verb in range(100):
        if self.run_with(computer, noun, verb) == want:
          return 100 * noun + verb
    raise ValueError('Should not get here.')


if __name__ == '__main__':
  typer.run(Day02().run)

# vim:ts=2:sw=2:expandtab
