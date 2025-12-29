#!/bin/python
"""Advent of Code, Day 5: Sunny with a Chance of Asteroids. 1202 Program Alarm."""

import intcode


def solve(data: str, part: int) -> int:
    """Solve the parts."""
    computer = intcode.Computer(data)
    computer.input.append(1 if part == 1 else 5)
    computer.run()
    return computer.output.pop()


TESTS = [
    # Part 1
    (1, "4,0,99", 4),
    (1, "04,2,99", 99),
    (1, "104,6,99", 6),
    (1, "1002,7,3,5,104,5,99,33", 99),
    # Part 2
    (2, "3,9,8,9,10,9,4,9,99,-1,8", 0),  # input == 8 POS Mode
    (2, "3,9,8,9,10,9,4,9,99,-1,5", 1),  # input == 5 POS Mode
    (2, "3,9,7,9,10,9,4,9,99,-1,8", 1),  # input  < 8 POS Mode
    (2, "3,9,7,9,10,9,4,9,99,-1,5", 0),  # input  < 5 POS Mode
    (2, "3,3,1108,-1,8,3,4,3,99", 0),    # input == 8 IMM Mode
    (2, "3,3,1108,-1,5,3,4,3,99", 1),    # input == 5 IMM Mode
    (2, "3,3,1107,-1,8,3,4,3,99", 1),    # input  < 8 IMM Mode
    (2, "3,3,1107,-1,5,3,4,3,99", 0),    # input  < 5 IMM Mode
]
