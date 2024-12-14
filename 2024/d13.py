#!/bin/python
"""Advent of Code, Day 13: Claw Contraption."""
import math
import z3

from lib import aoc

SAMPLE = """\
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
Prize: X=18641, Y=10279"""


class Day13(aoc.Challenge):
    """Day 13: Claw Contraption."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE, want=480),
        aoc.TestCase(part=2, inputs=SAMPLE, want=aoc.TEST_SKIP),
    ]
    INPUT_PARSER = aoc.ParseBlocks([aoc.parse_re_findall_int(r"\d+")])

    def _part1(self, puzzle_input: list[list[int]]) -> int:
        tokens = 0
        wins = 0
        for chunks in puzzle_input:
            b_a = complex(*chunks[0])
            b_b = complex(*chunks[1])
            dest = complex(*chunks[2])
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

    def solver(self, puzzle_input: list[list[int]], part_one: bool) -> int | str:
        tokens = 0
        for chunks in puzzle_input:
            if not part_one:
                chunks[2] = [i + 10000000000000 for i in chunks[2]]
            k, l, s = (i[0] for i in chunks)  # x values for a, b, dest
            m, n, t = (i[1] for i in chunks)  # y values for a, b, dest
            # Linear Diophantine equations?
            if chunks[2][0] % math.gcd(chunks[0][0], chunks[1][0]) or chunks[2][1] % math.gcd(chunks[0][1], chunks[1][1]):
                continue

            push_a = z3.Int("push_a")
            push_b = z3.Int("push_b")
            cost = z3.Int("cost")
            solver = z3.Optimize()
            solver.add(chunks[0][0] * push_a + chunks[1][0] * push_b == chunks[2][0])
            solver.add(chunks[0][1] * push_a + chunks[1][1] * push_b == chunks[2][1])
            solver.add(cost == 3 * push_a + push_b)
            solver.minimize(cost)
            if solver.check() != z3.sat:
                continue

            cost = solver.model()[cost].as_long()
            tokens += cost

            b = (l * t - m * s) / (n * k - m * l)
            a = (s - b * l) / k
            got = 3 * a + b
            if a != round(a) or b != round(b):
                print(f"Rounding doesn't work. {a=}, {b=}")
            if got == cost:
                print("Yes")
            else:
                print("No")

        return tokens

# vim:expandtab:sw=4:ts=4
