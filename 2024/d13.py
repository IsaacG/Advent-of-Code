#!/bin/python
"""Advent of Code, Day 13: Claw Contraption."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import z3

from lib import aoc

SAMPLE = [
    """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279""",  # 8
]

LineType = int
InputType = list[LineType]


class Day13(aoc.Challenge):
    """Day 13: Claw Contraption."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=480),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    # INPUT_PARSER = aoc.ParseIntergers()
    # INPUT_PARSER = aoc.parse_one_str_per_line
    # INPUT_PARSER = aoc.parse_multi_str_per_line
    # INPUT_PARSER = aoc.parse_one_int
    # INPUT_PARSER = aoc.parse_one_int_per_line
    # INPUT_PARSER = aoc.parse_ints_one_line
    # INPUT_PARSER = 
    # INPUT_PARSER = aoc.parse_re_group_str(r"(a) .* (b) .* (c)")
    # INPUT_PARSER = aoc.parse_re_findall_str(r"(a|b|c)")
    # INPUT_PARSER = aoc.parse_multi_mixed_per_line
    # INPUT_PARSER = aoc.parse_re_group_mixed(r"(foo) .* (\d+)")
    # INPUT_PARSER = aoc.parse_re_findall_mixed(r"\d+|foo|bar")
    INPUT_PARSER = aoc.ParseBlocks([aoc.parse_re_findall_int(r"\d+")])
    # INPUT_PARSER = aoc.ParseOneWord(aoc.Board.from_int_block)
    # INPUT_PARSER = aoc.CoordinatesParser(chars=None, origin_top_left=True)
    # ---
    # (width, height), start, garden, rocks = puzzle_input
    # max_x, max_y = width - 1, height - 1

    @functools.cache
    def bcost(self, b_a, b_b, dest, left) -> int:
        if dest == 0:
            self.tprint("Reached dest!")
            return 0
        if left == 0:
            self.tprint("Ran out of pushes!")
            return 10000
        if dest.real < 0 or dest.imag < 0:
            self.tprint("Overshot")
            return 10000
        c_a = self.bcost(b_a, b_b, dest - b_a, left - 1) + 3
        c_b = self.bcost(b_a, b_b, dest - b_b, left - 1) + 1
        return min(c_a, c_b)

    def art1(self, puzzle_input: InputType) -> int:
        tokens = 0
        wins = 0
        for chunk in puzzle_input:
            b_a = complex(*chunk[0])
            b_b = complex(*chunk[1])
            dest = complex(*chunk[2])
            # print(b_a, b_b, dest)
            cost = None
            for p_a, p_b in itertools.product(range(101), repeat=2):
                if (p_a == 80 and p_b == 40):
                    reach= p_a * b_a + p_b * b_b
                    # print(reach, dest, reach == dest)
                if p_a * b_a + p_b * b_b == dest:
                    if cost is None:
                        cost = p_a * 3 + p_b
                    else:
                        cost = min(cost, p_a * 3 + p_b)

            if cost is not None:
                tokens += cost
                wins += 1
        print("Wins:", wins, tokens)
        return tokens

    def solver(self, puzzle_input: InputType, part_one: bool) -> int | str:
        tokens = 0
        wins = 0
        for idx, chunk in enumerate(puzzle_input):
            b_a = tuple(chunk[0])
            b_b = tuple(chunk[1])
            dest = tuple(chunk[2])
            if not part_one:
                dest = tuple(i + 10000000000000 for i in dest)
            # Linear Diophantine equations
            if dest[0] % math.gcd(b_a[0], b_b[0]) or dest[1] % math.gcd(b_a[1], b_b[1]):
                continue

            p_a = z3.Int("p_a")
            p_b = z3.Int("p_b")
            cost = z3.Int("cost")
            solver = z3.Optimize()
            solver.add(b_a[0] * p_a + b_b[0] * p_b == dest[0])
            solver.add(b_a[1] * p_a + b_b[1] * p_b == dest[1])
            solver.add(cost == 3 * p_a + p_b)
            h = solver.minimize(cost)
            if solver.check() != z3.sat:
                print("Not solved")
            else:
                print("Solved")
                tokens += solver.model()[cost].as_long()
            continue

            kv = tuple(l // math.gcd(l, h) for l, h in zip(low, hi))
            ku = tuple(h // math.gcd(l, h) for l, h in zip(low, hi))


            start = int(min(d / l for d, l in zip(dest, low)))
            steps = math.prod(kv)
            # print("Steps", steps)
            print(f"{b_a=}, {b_b=}, {dest=}, {hi=}, {low=}, {start=}, {steps}")
            for s in range(start, start - steps -1, -1):
            # for s in range(min(gcp), max(gcp) + 1):
                p = start - s
                a = tuple(d - l * p for d, l in zip(dest, low))
                if a[0] % hi[0] == 0 and a[1] % hi[1] == 0 and a[0] // hi[0] == a[1] // hi[1]:
                    cost = l_cost * p + hi_cost * a[0] // hi[0]
                    print(p, a[0] // hi[0])
                    break

            if cost is not None:
                tokens += cost
                wins += 1
        return tokens

    def input_parser(self, puzzle_input: str) -> InputType:
        """Parse the input data."""
        return super().input_parser(puzzle_input)
        return puzzle_input.splitlines()
        return puzzle_input
        return [int(i) for i in puzzle_input.splitlines()]
        mutate = lambda x: (x[0], int(x[1])) 
        return [mutate(line.split()) for line in puzzle_input.splitlines()]
        # Words: mixed str and int
        return [
            tuple(
                int(i) if i.isdigit() else i
                for i in line.split()
            )
            for line in puzzle_input.splitlines()
        ]
        # Regex splitting
        patt = re.compile(r"(.*) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.")
        return [
            tuple(
                int(i) if i.isdigit() else i
                for i in patt.match(line).groups()
            )
            for line in puzzle_input.splitlines()
        ]

# vim:expandtab:sw=4:ts=4
