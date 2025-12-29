#!/bin/python
"""Advent of Code, Day 2: 1202 Program Alarm."""
import itertools
import intcode


def run_with_inputs(program: str, noun: int, verb: int, testing: int) -> int:
    computer = intcode.Computer(program)
    if not testing:
        computer.memory[1] = noun
        computer.memory[2] = verb
    computer.run()
    return computer.memory[0]


def solve(data: str, part: int, testing: bool) -> int:
    if part == 1:
        return run_with_inputs(data, 12, 2, testing)
    for noun, verb in itertools.product(range(100), repeat=2):
        if run_with_inputs(data, noun, verb, testing) == 19690720:
            return 100 * noun + verb


TESTS = [(1, "1,9,10,3,2,3,11,0,99,30,40,50", 3500)]
# vim:expandtab:sw=4:ts=4
