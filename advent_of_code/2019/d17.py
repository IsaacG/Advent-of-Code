#!/bin/python
"""Advent of Code, Day 17: Set and Forget."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

import intcode
from lib import aoc

SAMPLE = """\
..#..........
..#..........
#######...###
#.#...#...#.#
#############
..#...#...#..
..#####...^.."""

LineType = int
InputType = list[LineType]


class Day17(aoc.Challenge):
    """Day 17: Set and Forget."""

    DEBUG = False
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(inputs=SAMPLE, part=1, want=aoc.TEST_SKIP),
        aoc.TestCase(inputs=SAMPLE, part=2, want=0),
    ]
    INPUT_PARSER = aoc.parse_one_str

    def solver(self, puzzle_input: InputType, part_one: bool) -> int | str:
        computer = intcode.Computer(puzzle_input, debug=self.DEBUG)
        computer.run()
        data = [chr(i) for i in computer.output]
        # print("".join(data))
        display = aoc.CoordinatesParserC(chars="#<>^v").parse("".join(data))
        scaffolding = display.coords["#"]
        if part_one:
            return sum(
                int(pos.real * pos.imag)
                for pos in scaffolding
                if all(pos + direction in scaffolding for direction in aoc.FOUR_DIRECTIONS)
            )
        for char, delta in aoc.ARROW_DIRECTIONS.items():
            if char in display.coords:
                direction = delta
                pos = display.coords[char].pop()
                break
        # print(pos, direction)
        steps = []
        while pos + direction * 1j in scaffolding or pos + direction * -1j in scaffolding:
            if pos + direction * 1j in scaffolding:
                steps.append("R")
                direction *= 1j
            else:
                steps.append("L")
                direction *= -1j
            count = 0
            while pos + direction in scaffolding:
                pos += direction
                count += 1
            steps.append(str(count))
        segments = [steps]
        subprograms = {}
        for program in "ABC":
            for size in range(len(segments[0]), 0, -1):
                if size % 2:
                    continue
                block = segments[0][:size]
                count = sum(block == segment[i:i + size] for segment in segments for i in range(len(segment) - size + 1))
                if count > 2:
                    # print(block, size, count)
                    subprograms[program] = block
                    new_segments = []
                    for segment in segments:
                        idx = 0
                        while idx < len(segment):
                            start = idx
                            while idx < len(segment) and segment[idx:idx + size] != block:
                                idx += 2
                            if start != idx:
                                new_segments.append(segment[start:idx])
                            idx += size
                    segments = new_segments
                    # print(segments)
                    break
                            
        assert not segments
        print(subprograms)

        idx = 0
        program = []
        while idx < len(steps):
            for name, sub in subprograms.items():
                if steps[idx:idx + len(sub)] == sub:
                    program.append(name)
                    idx += len(sub)
                    break
        print(program)
        computer.reset()
        computer.memory[0] = 2
        write = ",".join(program) + "\n"
        for name in "ABC":
            write += ",".join(subprograms[name]) + "\n"
        write += "n\n"
        computer.input.extend([ord(i) for i in write])
        computer.run()
        return computer.output.pop()
        
        computer.run()
        
        # <A>,<A>,<B>,<C>,<C>,<A>,<B>,<C>,<A>,<B>
        # :%s/L,10,R,8,R,12/<C>
        # :%s/L,8,L,8,R,12,L,8,L,8/<B>
        # :%s/L,12,L,12,R,12/<A>




# vim:expandtab:sw=4:ts=4
