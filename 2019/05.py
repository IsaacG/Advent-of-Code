#!/usr/bin/env pypy
"""Day 5: Sunny with a Chance of Asteroids

Run a computer with more operations: equality, control flow, address modes.
"""

import typer

import asyncio
import intcode
from lib import aoc


class Day05(intcode.Challenge):

  TESTS = (
    aoc.TestCase(inputs='4,0,99', part=1, want=4),
    aoc.TestCase(inputs='04,2,99', part=1, want=99),
    aoc.TestCase(inputs='104,6,99', part=1, want=6),
    aoc.TestCase(inputs='1002,7,3,5,104,5,99,33', part=1, want=99),
    aoc.TestCase(inputs='3,9,8,9,10,9,4,9,99,-1,8', part=2, want=0),  # input == 8 POS Mode
    aoc.TestCase(inputs='3,9,8,9,10,9,4,9,99,-1,5', part=2, want=1),  # input == 5 POS Mode
    aoc.TestCase(inputs='3,9,7,9,10,9,4,9,99,-1,8', part=2, want=1),  # input  < 8 POS Mode
    aoc.TestCase(inputs='3,9,7,9,10,9,4,9,99,-1,5', part=2, want=0),  # input  < 5 POS Mode
    aoc.TestCase(inputs='3,3,1108,-1,8,3,4,3,99', part=2, want=0),    # input == 8 IMM Mode
    aoc.TestCase(inputs='3,3,1108,-1,5,3,4,3,99', part=2, want=1),    # input == 5 IMM Mode
    aoc.TestCase(inputs='3,3,1107,-1,8,3,4,3,99', part=2, want=1),    # input  < 8 IMM Mode
    aoc.TestCase(inputs='3,3,1107,-1,5,3,4,3,99', part=2, want=0),    # input  < 5 IMM Mode
  )

  def part1(self, computer: intcode.Computer) -> int:
    asyncio.run(computer.run(inputs=[1]))
    return computer.output()[-1]

  def part2(self, computer: intcode.Computer) -> int:
    asyncio.run(computer.run(inputs=[5]))
    return computer.output()[-1]


if __name__ == '__main__':
  typer.run(Day05().run)

# vim:ts=2:sw=2:expandtab
