#!/bin/python
"""Advent of Code, Day 2: 1202 Program Alarm."""

import itertools

import intcode
from lib import aoc

SAMPLE = ["1,9,10,3,2,3,11,0,99,30,40,50"]


class Day02(aoc.Challenge):
    """Day 2: 1202 Program Alarm."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=3500),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    def run_with_inputs(self, program: str, noun: int, verb: int) -> int:
        computer = intcode.Computer(program)
        if not self.testing:
            computer.memory[1] = noun
            computer.memory[2] = verb
        computer.run()
        return computer.memory[0]

    def part1(self, puzzle_input: str) -> int:
        return self.run_with_inputs(puzzle_input, 12, 2)

    def part2(self, puzzle_input: str) -> int:
        for noun, verb in itertools.product(range(100), repeat=2):
            if self.run_with_inputs(puzzle_input, noun, verb) == 19690720:
                return 100 * noun + verb

# vim:expandtab:sw=4:ts=4
