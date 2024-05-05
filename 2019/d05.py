#!/bin/python
"""Advent of Code, Day 5: Sunny with a Chance of Asteroids."""

import itertools

import intcode
from lib import aoc

SAMPLE = ["1002,4,3,4,33"]


class Day05(aoc.Challenge):
    """Day 2: 1202 Program Alarm."""

    TESTS = (
        # Part 1
        aoc.TestCase(inputs='4,0,99', part=1, want=4),
        aoc.TestCase(inputs='04,2,99', part=1, want=99),
        aoc.TestCase(inputs='104,6,99', part=1, want=6),
        aoc.TestCase(inputs='1002,7,3,5,104,5,99,33', part=1, want=99),
        # Part 2
        aoc.TestCase(inputs='3,9,8,9,10,9,4,9,99,-1,8', part=2, want=0),  # input == 8 POS Mode
        aoc.TestCase(inputs='3,9,8,9,10,9,4,9,99,-1,5', part=2, want=1),  # input == 5 POS Mode
        aoc.TestCase(inputs='3,9,7,9,10,9,4,9,99,-1,8', part=2, want=1),  # input  < 8 POS Mode
        aoc.TestCase(inputs='3,9,7,9,10,9,4,9,99,-1,5', part=2, want=0),  # input  < 5 POS Mode
        aoc.TestCase(inputs='3,3,1108,-1,8,3,4,3,99', part=2, want=0),    # input == 8 IMM Mode
        aoc.TestCase(inputs='3,3,1108,-1,5,3,4,3,99', part=2, want=1),    # input == 5 IMM Mode
        aoc.TestCase(inputs='3,3,1107,-1,8,3,4,3,99', part=2, want=1),    # input  < 8 IMM Mode
        aoc.TestCase(inputs='3,3,1107,-1,5,3,4,3,99', part=2, want=0),    # input  < 5 IMM Mode
    )
    INPUT_PARSER = aoc.parse_one_str

    def part1(self, parsed_input: str) -> int:
        computer = intcode.Computer(parsed_input)
        if not self.testing:
            computer.io.append(1)
        computer.run()
        *results, output = computer.io
        if any(results):
            raise RuntimeError("Test Failed")
        return output

    def part2(self, parsed_input: str) -> int:
        computer = intcode.Computer(parsed_input)
        computer.io.append(5)
        computer.run()
        return computer.io.popleft()


# vim:expandtab:sw=4:ts=4
