#!/bin/python
"""Advent of Code, Day 9: Sensor Boost."""

import intcode


def solve(data: str, part: int, testing: bool) -> int:
    """Solve the parts."""
    computer = intcode.Computer(data)
    if testing:
        computer.run()
        return ",".join(str(i) for i in computer.output)

    computer.input.append(part)
    computer.run()
    return computer.output.pop()


SAMPLE = [
    "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99",
    "1102,34915192,34915192,7,4,7,99,0",
    "104,1125899906842624,99",
]
TESTS = [
    (1, SAMPLE[0], SAMPLE[0]),
    (1, SAMPLE[1], "1219070632396864"),
    (1, SAMPLE[2], "1125899906842624"),
]
