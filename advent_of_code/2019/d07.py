#!/bin/python
"""Advent of Code, Day 7: Amplification Circuit."""

import collections
import itertools
import intcode


def solve(data: str, part: int) -> int:
    """Find the max output for any given input."""
    largest = 0
    input_shift = 0 if part == 1 else 5
    # Try all permutations of initial inputs.
    for values in itertools.permutations(range(5)):
        queues = [collections.deque[int]() for _ in range(5)]
        # Chain five programs in serial.
        computers = [
            intcode.Computer(data, input_q=queues[i], output_q=queues[(i + 1) % 5])
            for i in range(5)
        ]
        for computer, value in zip(computers, values, strict=True):
            computer.input.append(value + input_shift)
        computers[0].input.append(0)  # Initial input: 0
        # Run all the programs until the last one is stopped.
        while not computers[-1].stopped:
            for computer in computers:
                computer.run()
        # print([c.state for c in computers])
        # print([len(q) for q in queues])
        assert len(queues[0]) == 1
        assert all(len(q) == 0 for q in queues[1:])
        largest = max(largest, computers[-1].output.pop())

    return largest


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
TESTS = [
    (1, SAMPLE[0], 43210),      # phases = 4,3,2,1,0
    (1, SAMPLE[1], 54321),      # phases = 0,1,2,3,4
    (1, SAMPLE[2], 65210),      # phases = 1,0,4,3,2
    (2, SAMPLE[3], 139629729),  # phases = 1,0,4,3,2
    (2, SAMPLE[4], 18216),      # phases = 1,0,4,3,2
]
