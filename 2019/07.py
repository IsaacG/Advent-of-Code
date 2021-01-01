#!/usr/bin/env python
"""Day 7: Amplification Circuit.

Connect multiple Intcode Computers in a pipeline.
Brute force for initial inputs that generate the max output.
"""

import asyncio
import functools
import itertools
import typer
from typing import Iterable

import intcode
from lib import aoc

SAMPLE = [
  '3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0',
  '3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0',
  '3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0',
  '3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5',
  (
    '3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,'
    '1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10'
  ),
]


class Day07(intcode.Challenge):

  TESTS = (
    aoc.TestCase(inputs=SAMPLE[0], part=1, want=43210),      # phases = 4,3,2,1,0
    aoc.TestCase(inputs=SAMPLE[1], part=1, want=54321),      # phases = 0,1,2,3,4
    aoc.TestCase(inputs=SAMPLE[2], part=1, want=65210),      # phases = 1,0,4,3,2
    aoc.TestCase(inputs=SAMPLE[3], part=2, want=139629729),  # phases = 1,0,4,3,2
    aoc.TestCase(inputs=SAMPLE[4], part=2, want=18216),      # phases = 1,0,4,3,2
  )

  async def output_for_inputs(self, computer: intcode.Computer, phases: Iterable[int]) -> int:
    """Set up multiple computers in a pipeline. Run until all halt."""
    # One computer per phase, one pipe per computer.
    comps = [computer.copy() for _ in phases]
    pipes = [asyncio.Queue() for _ in phases]

    # Feed the initial input - the phase - into each computer.
    for i, phase in enumerate(phases):
      comps[i].phase = phase
      await pipes[i].put(phase)

    # Collect computers with their input and output and run.
    c_with_io = zip(comps, zip(pipes, pipes[1:] + pipes[0:1]))
    tasks = [asyncio.create_task(comp.run(io=io)) for comp, io in c_with_io]
    # Computer 0 needs an initial values 0.
    await pipes[0].put(0)
    # Wait for completion.
    for task in tasks:
      await task

    # Return whatever the last computer outputs.
    return comps[-1].output()[-1]

  def part1(self, computer: intcode.Computer) -> int:
    """Find the phase permutation that derives the highest thruster output."""
    f = functools.partial(self.output_for_inputs, computer)
    return max(asyncio.run(f(phases)) for phases in itertools.permutations(range(5)))

  def part2(self, computer: intcode.Computer) -> int:
    """Find the phase permutation that derives the highest thruster output."""
    f = functools.partial(self.output_for_inputs, computer)
    return max(asyncio.run(f(phases)) for phases in itertools.permutations(range(5, 10)))


if __name__ == '__main__':
  typer.run(Day07().run)

# vim:ts=2:sw=2:expandtab
