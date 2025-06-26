#!/usr/bin/env python
"""Day 9: Sensor Boost

Extend Intcode computer with relative base addresses and infinite memory space.
"""

import asyncio

import intcode
from lib import aoc


SAMPLE = [
  '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99',
  '1102,34915192,34915192,7,4,7,99,0',
  '104,1125899906842624,99',
]


class Day09(intcode.Challenge):

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=0, want=SAMPLE[0]),
    aoc.TestCase(inputs=SAMPLE[1], part=0, want='1219070632396864'),
    aoc.TestCase(inputs=SAMPLE[2], part=0, want='1125899906842624'),
  )

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.funcs[0] = self.test_part

  def test_part(self, computer: intcode.Computer) -> str:
    if not self.testing:
      return ''
    asyncio.run(computer.run())
    return ','.join(str(i) for i in computer.output())

  def part1(self, computer: intcode.Computer) -> str:
    asyncio.run(computer.run(inputs=[1]))
    return computer.output()[0]

  def part2(self, computer: intcode.Computer) -> int:
    asyncio.run(computer.run(inputs=[2]))
    return computer.output()[0]
