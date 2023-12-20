#!/bin/python
"""Advent of Code, Day 20: Pulse Propagation."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re
import time

from lib import aoc

SAMPLE = [
    """\
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a""",  # 10
    """\
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output""",  # 23
]

LineType = int
InputType = list[LineType]


class Day20(aoc.Challenge):
    """Day 20: Pulse Propagation."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}
    # PARAMETERIZED_INPUTS = [5, 50]

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=32000000),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=11687500),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    def part1(self, parsed_input: InputType) -> int:
        modules = parsed_input
        flipflops = {name: False for name, (mtype, _) in modules.items() if mtype == "%"}

        conjs = {name: {} for name, (mtype, _) in modules.items() if mtype == "&"}
        for name, (_, targets) in modules.items():
            for target in targets:
                if target in conjs:
                    conjs[target][name] = False

        sent = {True: 0, False: 0}
        for step in range(1000):
            inputs = collections.deque([("button", "broadcaster", False)])
            # print("Step", step)
            while inputs:
                src, dest, signal = inputs.popleft()
                dest_type, targets = modules[dest]
                sent[signal] += 1
                # print(f"{src} {'high' if signal else 'low'} => {dest}")

                out = None
                if dest_type == "broadcaster":
                    out = signal
                elif dest_type == "%" and not signal:
                    out = not flipflops[dest]
                    flipflops[dest] = out
                elif dest_type == "&":
                    conjs[dest][src] = signal
                    out = not all(conjs[dest].values())

                if out is not None:
                    for target in targets:
                        inputs.append((dest, target, out))

        # print(sent)
        return math.prod(sent.values())

    def part2(self, parsed_input: InputType) -> int:
        # print(f"{parsed_input!r}")
        modules = parsed_input
        flipflops = {name: False for name, (mtype, _) in modules.items() if mtype == "%"}

        conjs = {name: {} for name, (mtype, _) in modules.items() if mtype == "&"}
        for name, (_, targets) in modules.items():
            for target in targets:
                if target in conjs:
                    conjs[target][name] = False

        # Part two
        # --------
        # We need a LOW sent to "rx".
        #
        # Reverse engineering the instructions, there should be one conjunction module
        # (first level) which feeds into "rx".
        # That module will send a LOW when all its inputs are HIGH.
        #
        # There should be a small number of (second level) modules which feed into that one
        # first level conjunction module.
        # Those second level modules should output HIGH cyclically.
        # If those modules all output HIGH cyclically, on the lowest-common-multiple cycle
        # they should all output HIGH on the same cycle which would trigger a LOW to "rx".
        #
        # Find the second level modules.
        # Run the simulation until they each output three HIGH values.
        # Validate the HIGH output is cyclical.
        # Return the product.
        rx_inputs = [name for name, (_, targets) in modules.items() if "rx" in targets]
        assert len(rx_inputs) == 1 and rx_inputs[0] in conjs
        rx_input = rx_inputs[0]
        second_level_inputs = [name for name, (_, targets) in modules.items() if rx_input in targets]
        second_level_highs = {name: [] for name in second_level_inputs}

        sent = {True: 0, False: 0}
        for step in itertools.count(start=1):
            inputs = collections.deque([("button", "broadcaster", False)])
            while inputs:
                src, dest, signal = inputs.popleft()
                dest_type, targets = modules[dest]
                sent[signal] += 1

                out = None
                if dest_type == "broadcaster":
                    out = signal
                elif dest_type == "%" and not signal:
                    out = not flipflops[dest]
                    flipflops[dest] = out
                elif dest_type == "&":
                    conjs[dest][src] = signal
                    out = not all(conjs[dest].values())

                if out is not None:
                    for target in targets:
                        inputs.append((dest, target, out))

                # Track the HIGH outputs of the second level inputs.
                if out is True and dest in second_level_highs:
                    second_level_highs[dest].append(step)
                    if all(len(vals) >= 3 for vals in second_level_highs.values()):
                        # Verify the outputs are all cyclical. Return the product.
                        for vals in second_level_highs.values():
                            first = vals[0]
                            assert all(first * idx == value for idx, value in enumerate(vals, start=1))
                            return math.prod(vals[0] for vals in second_level_highs.values())



    def solver(self, parsed_input: InputType, param: bool) -> int | str:
        raise NotImplementedError

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        modules = collections.defaultdict(lambda: ("NA", []))
        for line in puzzle_input.splitlines():
            name, targets = line.split(" -> ")
            if name[0] in "%&":
                mtype, name = name[0], name[1:]
            elif name == "broadcaster":
                mtype = "broadcaster"
            else:
                raise RuntimeError(f"Unknown type, {line}")
            modules[name] = (mtype, targets.split(", "))
        return modules

# vim:expandtab:sw=4:ts=4
