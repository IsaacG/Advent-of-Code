#!/bin/python
"""Advent of Code, Day 8: Haunted Wasteland."""

import itertools
import math

from lib import aoc

InputType = tuple[str, dict[str, tuple[str, str]]]
INDEX = {"L": 0, "R": 1}


def steps(
    instructions: str,
    mapping: dict[str, tuple[str, str]],
    location: str,
    part_two: bool,
) -> int:
    """Return the number of steps from a start location to a terminal node."""
    for step, direction in enumerate(itertools.cycle(instructions), start=1):
        location = mapping[location][INDEX[direction]]
        if location == "ZZZ" or part_two and location.endswith("Z"):
            return step
    raise RuntimeError("Unreachable")


def solve(data: InputType, part: int, testing: bool) -> int:
    """Compute the number of steps to get through the maze."""
    pre_run(data, testing)
    instructions, mapping = data
    if part == 1:
        locations = {"AAA"}
    else:
        locations = {i for i in mapping if i.endswith("A")}

    factors = [
        steps(instructions, mapping, location, part == 2)
        for location in locations
    ]
    return math.lcm(*factors)


def input_parser(data: str) -> InputType:
    """Parse the input data."""
    parser = aoc.ParseBlocks(
        [
            aoc.parse_one_str,
            aoc.parse_re_findall_str(r"[A-Z0-9]{3}")
        ]
    )
    instructions, nodes = parser.parse(data)
    mapping = {
        start: tuple(left_right)
        for start, *left_right in nodes
    }
    return instructions, mapping


def pre_run(data: InputType, testing: bool) -> None:
    """Verify assumptions.

    The part two solution using LCM assumes that:
    * first_Z == second_Z
    * distance(start_location, first_Z) == distance(first_Z, second_Z)
    * distance(start_location, first_Z) == n * length(instruction)`
    """
    if testing:
        return
    instructions, mapping = data
    locations = {i for i in mapping if i.endswith("A")}
    for location in locations:
        step = 0
        next_instruction = itertools.cycle(instructions)
        for step, direction in enumerate(next_instruction, start=1):
            location = mapping[location][INDEX[direction]]
            if location.endswith("Z"):
                break
        steps1, terminal1 = step, location
        for step, direction in enumerate(next_instruction, start=1):
            location = mapping[location][INDEX[direction]]
            if location.endswith("Z"):
                break
        steps2, terminal2 = step, location
        assert steps1 == steps2, f"{steps1} != {steps2}"
        assert terminal1 == terminal2
        assert steps1 % len(instructions) == 0


SAMPLE = [
    """\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)""",
    """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)""",
    """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)""",
]
TESTS = [(1, SAMPLE[0], 2), (1, SAMPLE[1], 6), (2, SAMPLE[2], 6)]
# vim:expandtab:sw=4:ts=4
