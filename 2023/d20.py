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

CONJUNCTION = "&"
FLIP_FLIP = "%"
InputType = tuple[dict[str, str], dict[str, list[str]]]


class Day20(aoc.Challenge):
    """Day 20: Pulse Propagation."""

    TESTS = [
        aoc.TestCase(inputs=SAMPLE[0], part=1, want=32000000),
        aoc.TestCase(inputs=SAMPLE[1], part=1, want=11687500),
        aoc.TestCase(inputs=SAMPLE[0], part=2, want=aoc.TEST_SKIP),
    ]

    def solver(self, parsed_input: InputType, part_one: bool) -> int:
        """Simulate the circuit."""
        module_types, outputs = parsed_input

        memory_flipflips = {
            name: False for name, module_type in module_types.items() if module_type == FLIP_FLIP
        }
        memory_conjucations = {
            name: {} for name, module_type in module_types.items() if module_type == CONJUNCTION
        }

        for name, targets in outputs.items():
            for target in targets:
                if module_types.get(target) == CONJUNCTION:
                    memory_conjucations[target][name] = False

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
        if not part_one:
            rx_inputs = [name for name, targets in outputs.items() if "rx" in targets]
            assert len(rx_inputs) == 1 and module_types[rx_inputs[0]] == CONJUNCTION
            rx_input = rx_inputs[0]
            second_level_highs = {name: [] for name, targets in outputs.items() if rx_input in targets}

        sent = {True: 0, False: 0}
        inputs = collections.deque()
        for step in itertools.count(start=1):
            # Push the button and send a LOW to the broadcaster!
            inputs.append(("button", "broadcaster", False))
            while inputs:
                src, current_module, signal = inputs.popleft()
                sent[signal] += 1
                if current_module not in module_types:
                    # Sink. Nothing to do here.
                    continue
                dest_type = module_types[current_module]
                targets = outputs[current_module]

                output = None
                if dest_type == "broadcaster":
                    output = signal
                elif dest_type == FLIP_FLIP and not signal:
                    output = not memory_flipflips[current_module]
                    memory_flipflips[current_module] = output
                elif dest_type == CONJUNCTION:
                    memory_conjucations[current_module][src] = signal
                    output = not all(memory_conjucations[current_module].values())

                # If there is an output signal, propagate it.
                if output is not None:
                    for target in targets:
                        inputs.append((current_module, target, output))

                # Track the HIGH outputs of the second level inputs.
                if not part_one and output and current_module in second_level_highs:
                    second_level_highs[current_module].append(step)
                    # Loop until we see N values for each second level module.
                    if all(len(vals) >= 2 for vals in second_level_highs.values()):
                        # Verify the outputs are all cyclical. Return the product.
                        for vals in second_level_highs.values():
                            assert all(vals[0] * idx == value for idx, value in enumerate(vals, start=1))
                        return math.prod(vals[0] for vals in second_level_highs.values())
            if part_one and step == 1000:
                return math.prod(sent.values())

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        outputs = {}
        module_types = {}
        for line in puzzle_input.splitlines():
            name, targets = line.split(" -> ")
            if name[0] in (CONJUNCTION, FLIP_FLIP):
                module_type, name = name[0], name[1:]
            else:
                module_type = name
            outputs[name] = targets.split(", ")
            module_types[name] = module_type
        return module_types, outputs

# vim:expandtab:sw=4:ts=4
