#!/bin/python
"""Advent of Code, Day 17: Chronospatial Computer."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import random
import re

from lib import aoc

SAMPLE = [
    """\
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0""",  # 76
    """\
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""
]

LineType = int
InputType = list[LineType]


class Day17(aoc.Challenge):
    """Day 17: Chronospatial Computer."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want="4,6,3,5,6,3,5,2,1,0"),
        # aoc.TestCase(part=2, inputs=SAMPLE[1], want=117440),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.ParseBlocks([aoc.parse_ints, aoc.parse_re_findall_int(r"\d+")])

    def simulate(self, reg, instructions) -> list[int]:
        ptr = 0

        def val(i, combo):
            if not combo:
                return i
            if 0 <= i <= 3:
                return i
            return reg[{4: "a", 5: "b", 6: "c"}[i]]

        out = []
        # print(ptr, len(instructions))
        while ptr < len(instructions) - 1:
            instruction, op = instructions[ptr], instructions[ptr + 1]
            ptr += 2
            # print("a", "_".join("".join(i) for i in itertools.batched(bin(reg["a"])[2:], n=3)))

            if instruction == 0: # adv
                reg["a"] = reg["a"] // (2 ** val(op, True))
            if instruction == 1: # bxl
                reg["b"] = reg["b"] ^ op
            if instruction == 2: # bst
                reg["b"] = val(op, True) % 8
            if instruction == 3: # jnz
                if reg["a"] != 0:
                    ptr = op
            if instruction == 4: # bxc
                reg["b"] = reg["b"] ^ reg["c"]
            if instruction == 5: # out
                # print(f"{ptr=}, {op=}, {val(op, True)}")
                # print("a", "_".join("".join(i) for i in itertools.batched(bin(reg["a"])[2:], n=3)))
                # print("Output", (val(op, True) % 8))
                out.append((val(op, True) % 8))
            if instruction == 6: # bdv
                reg["b"] = reg["a"] // (2 ** val(op, True))
            if instruction == 7: # cdv
                reg["c"] = reg["a"] // (2 ** val(op, True))
                # print(f"cdv dist = {reg['b']}, val = {reg['c'] % 8=}, inverted = {7 - (reg['c'] % 8)}",)
            # print(instruction, op)
            # for i in "abc":
                # print(i, reg[i] % 8, bin(reg[i] % 8))

        return out

    def part1(self, puzzle_input: InputType) -> int:
        reg = {char: puzzle_input[0][i][0] for i, char in enumerate("abc")}
        instructions = puzzle_input[1][0]
        return ",".join(str(i) for i in self.simulate(reg, instructions))


    def part2(self, puzzle_input: InputType) -> int:

        instructions = puzzle_input[1][0]

        def simulate(reg_a: int) -> list[int]:
            out = []
            while reg_a:
                shift = reg_a & 7 ^ 7
                digit = (3 ^ reg_a ^ (reg_a >> shift)) & 7
                out.append(digit)
                reg_a = reg_a >> 3
            return out

        test_val = 0b111_111_010_101
        assert self.simulate({"a": test_val, "b": 0, "c": 0}, instructions) == [3, 6, 3, 3]
        assert simulate(test_val) == [3, 6, 3, 3]

        if True:
            mask = (1 << 13) - 8
            def solve(given, digits):
                # print(f"solve({given=}, {digits=})")
                given <<= 3
                options = set()
                for i, shift in itertools.product(range(8), repeat=2):
                    shifted = (i << shift) & mask
                    last_3 = shift ^ 7
                    # digit = 3 ^ last_3 ^ (shifted >> shift)
                    # if digit != instructions[-digits]:
                    #     continue
                    new_num = given | shifted | last_3
                    got = simulate(new_num)
                    # print(got)
                    if len(got) == digits and got == instructions[-len(got):]:
                        options.add(new_num)
                if digits != 16:
                    new_opts = set()
                    for option in options:
                        if (got := solve(option, digits + 1)) is not None:
                            new_opts.add(got)
                    options = new_opts
                if digits == 16:
                    for option in options:
                        if (got := simulate(option)) == instructions:
                            print(f"{option} yields {got}")
                return min(options) if options else None

            return solve(0, 1)
                    




        if False:
            for a in [0b111_111_010_101]:
                print("Test", a)
                print("Sim out", "".join(str(i) for i in self.simulate({"a": a, "b": 0, "c": 0}, instructions)))
                print("Run")
                print("a", "_".join("".join(i) for i in itertools.batched(bin(a)[2:], n=3)))
                out = ""
                while a:
                    print("a", "_".join("".join(i) for i in itertools.batched(bin(a)[2:], n=3)))
                    shift = a & 7 ^ 7
                    # print("shift", b)
                    digit = (3 ^ a ^ (a >> shift)) & 7
                    out += str(digit)
                    a = a >> 3
                print("Simple out", out)
            return

        if False:
            want = instructions[:]
            want_str = "".join(str(i) for i in want)
            shifts = itertools.product(range(8), repeat=len(want))
            protected = 0
            for s in shifts:
                num = 0
                for digit, a_part in zip(reversed(want), s):
                    num <<= 3
                    protected <<= 3
                    do_not_touch = num & protected

                    shift = a_part ^ 7
                    shift_part = digit ^ 3 ^ a
                    # shift_part = (shift_part << shift) ^ 




                    neg_dist = dist ^ 7
                    num |= neg_dist | (digit ^ 7) << dist
                    if num & 7 != neg_dist:
                        break
                    if num & (7 << dist) != (digit ^ 7):
                        break
                    if do_not_touch != num & protected:
                        break
                    protected |= 7 | 7 << dist
                else:
                    print(num)
                    a = num
                    out = ""
                    while a:
                        bits = a & 7
                        b = bits ^ 7
                        out += str(7 ^ ((a >> b) & 7))
                        a = a >> 3
                    if out == want_str:
                        assert num < 266582694363549
                        return num

            return


        else:
            for i in itertools.count():
                if not i % 1000000:
                    print(i)
                a = i
                outcount = 0
                while a:
                    b = (a % 8) ^ 7
                    c = a >> b
                    b ^= c
                    b ^= a
                    out = b % 8
                    if out == want[outcount]:
                        outcount += 1
                        if outcount == len_want:
                            return i
                    else:
                        break
                    a //= 8

        reg = {char: puzzle_input[0][i][0] for i, char in enumerate("abc")}
        instructions = puzzle_input[1][0]
        want = [str(i) for i in instructions]

        for i in itertools.count():
            reg["a"] = i
            got = self.simulate(reg.copy(), instructions)
            if got == instructions:
                return i
            if got[:-4] == [0,3,3,0]:
                print(i, got)

# vim:expandtab:sw=4:ts=4
