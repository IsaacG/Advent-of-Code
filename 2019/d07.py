#!/bin/python
"""Advent of Code, Day 7: Amplification Circuit."""
from __future__ import annotations

import collections
import itertools

from lib import aoc
import intcode

SAMPLE = [
  "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0",
  "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0",
  "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0",
  "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5",
  (
    "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,"
    "1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"
  ),
]


class Day07(aoc.Challenge):
    """Day 7: Amplification Circuit."""

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=43210),      # phases = 4,3,2,1,0
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=54321),      # phases = 0,1,2,3,4
        aoc.TestCase(inputs=SAMPLE[2], part=1, want=65210),      # phases = 1,0,4,3,2
        aoc.TestCase(inputs=SAMPLE[3], part=2, want=139629729),  # phases = 1,0,4,3,2
        aoc.TestCase(inputs=SAMPLE[4], part=2, want=18216),      # phases = 1,0,4,3,2
    )
    INPUT_PARSER = aoc.parse_one_str
    PARAMETERIZED_INPUTS = [0, 5]

    def solver(self, program: str, input_shift: int) -> int:
        largest = 0
        # Try all permutations of initial inputs.
        for values in itertools.permutations(range(input_shift, 5 + input_shift)):
            queues = [collections.deque([i]) for i in values]
            queues[0].append(0)  # Initial input: 0
            # Chain five programs in serial.
            computers = [
                intcode.Computer(program, input_q=i, output_q=o)
                for i, o in zip(queues, queues[1:] + queues[:1])
            ]
            # Run all the programs until the last one is stopped.
            while not computers[-1].stopped:
                for computer in computers:
                    computer.run()
            value = queues[0].popleft()
            if value > largest:
                largest = value

        return largest

# vim:expandtab:sw=4:ts=4
