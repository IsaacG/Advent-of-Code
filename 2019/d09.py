#!/bin/python
"""Advent of Code, Day 9: Sensor Boost."""

import intcode
from lib import aoc

SAMPLE = [
    "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99",
    "1102,34915192,34915192,7,4,7,99,0",
    "104,1125899906842624,99",
]


class Day09(aoc.Challenge):
    """Day 9: Sensor Boost."""

    TESTS = (
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=SAMPLE[0]),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want="1219070632396864"),
        aoc.TestCase(inputs=SAMPLE[2], part=1, want="1125899906842624"),
        aoc.TestCase(inputs="", part=2, want=aoc.TEST_SKIP),
    )
    INPUT_PARSER = aoc.parse_one_str

    def part1(self, parsed_input: str) -> int:
        computer = intcode.Computer(parsed_input, debug=self.DEBUG)
        if self.testing:
            computer.run()
            return ",".join(str(i) for i in computer.output)

        computer.input.append(1)
        computer.run()
        *results, output = computer.output
        if any(results):
            raise RuntimeError(f"Test Failed! {results, output}")
        return output

    def part2(self, parsed_input: str) -> int:
        computer = intcode.Computer(parsed_input, debug=self.DEBUG)
        computer.input.append(2)
        computer.run()
        return computer.output.popleft()

# vim:expandtab:sw=4:ts=4
