#!/bin/python
"""Advent of Code, Day 24: Crossed Wires."""
from __future__ import annotations

import collections
import functools
import itertools
import math
import re

from lib import aoc

SAMPLE = [
    """\
x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02""",  # 17
    """\
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj""",  # 37
]

LineType = int
InputType = list[LineType]


class Day24(aoc.Challenge):
    """Day 24: Crossed Wires."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=4),
        aoc.TestCase(part=1, inputs=SAMPLE[1], want=2024),
        # aoc.TestCase(part=2, inputs=SAMPLE[0], want=None),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]

    INPUT_PARSER = aoc.ParseBlocks([aoc.BaseParseMultiPerLine(word_separator=": "), aoc.parse_multi_str_per_line])

    def part1(self, puzzle_input: InputType) -> int:
        initial, gatesa = puzzle_input
        values = {a: bool(int(b)) for a, b in initial}
        gates = {}
        for a, op, b, _, out in gatesa:
            gates[out] = (a, op, b)
        todo = set(gates)
        while todo:
            out = next(out for out in todo if gates[out][0] in values and gates[out][2] in values)
            a, op, b = gates[out]
            # print(out, a, op, b)
            del gates[out]
            todo.remove(out)
            if op == "AND":
                values[out] = values[a] and values[b]
            elif op == "OR":
                values[out] = values[a] or values[b]
            elif op == "XOR":
                values[out] = values[a] ^ values[b]
        v = sorted((i for i in values if i.startswith("z")), reverse=True)
        s = 0
        for w in v:
            s = (s << 1) + int(values[w])
        return s

    def test_gates(self, gates, x, y):
        values = {}
        og = gates.copy()
        gates = gates.copy()
        for i in range(45):
            mask = 1 << i
            values[f"x{i:02}"] = x & mask
            values[f"y{i:02}"] = y & mask
        z = x + y
        want = {}
        for i in range(46):
            mask = 1 << i
            want[f"z{i:02}"] = z & (1 << i)

        todo = set(gates)
        while todo:
            done = []
            for out, (a, op, b) in gates.items():
                if out not in todo:
                    continue
                if a not in values or b not in values:
                    continue
                todo.remove(out)
                done.append(out)
                if op == "AND":
                    values[out] = values[a] and values[b]
                elif op == "OR":
                    values[out] = values[a] or values[b]
                elif op == "XOR":
                    values[out] = values[a] ^ values[b]
            if not done:
                raise ValueError("Cannot solve")
            for d in done:
                del gates[d]
        incorrect = {i for i, j in want.items() if values[i] != j}
        return incorrect

    def get_pot(self, gates):
        candidates = self.test_gates(gates, 0, 2**46-1)
        candidates |= self.test_gates(gates, 2**23-1, 0)
        candidates |= self.test_gates(gates, (2**23-1) << 22, 0)
        x = 0
        for i in range(22):
            x <<= 2
            x += 1
        candidates |= self.test_gates(gates, x, 0)
        return candidates

    def get_cand(self, gates):
        candidates = self.test_gates(gates, 0, 2**46-1)
        candidates &= self.test_gates(gates, 2**23-1, 0)
        candidates &= self.test_gates(gates, (2**23-1) << 22, 0)
        x = 0
        for i in range(22):
            x <<= 2
            x += 1
        candidates &= self.test_gates(gates, x, 0)
        return candidates

    def part2(self, puzzle_input: InputType) -> int:
        initial, gatesa = puzzle_input
        values = {a: bool(int(b)) for a, b in initial}
        gates = {}
        affects = collections.defaultdict(set)
        for a, op, b, _, out in gatesa:
            gates[out] = (a, op, b)
            affects[a].add(out)
            affects[b].add(out)


        def upstream(incorrect):
            incorrect = incorrect.copy()
            ups = set()
            while incorrect:
                n = incorrect.pop()
                ups.add(n)
                a, _, b = gates[n]
                if a in gates:
                    incorrect.add(a)
                if b in gates:
                    incorrect.add(b)
            return ups

        @functools.cache
        def get_downstream(gate):
            downstream = affects[gate]
            downstream |= {e for d in downstream for e in get_downstream(d)}
            return downstream

        all_downstream = {g: get_downstream(g) for g in gates}
        z_downstream = {g: {i for i in d if i.startswith("z")} for g, d in all_downstream.items()}
        z_downstream = {a: b for a, b in z_downstream.items() if b}

        broken = self.get_pot(gates)
        s_gates = set(gates)
        updated_gates = gates.copy()

        def find_pair(updated_gates, candidates, num):
            broken = self.get_pot(updated_gates)
            if num == 0:
                return set(), not broken
            for a, b in itertools.combinations(candidates, 2):
                try:
                    updated_gates[a], updated_gates[b] = updated_gates[b], updated_gates[a]
                    broken_a = self.get_pot(updated_gates)
                    if not broken > broken_a:
                        continue
                    new_candidates = candidates - {a, b}
                    swaps, solves = find_pair(updated_gates, new_candidates, num - 1)
                    if solves:
                        return swaps | {a, b}
                except:
                    continue
                finally:
                    updated_gates[a], updated_gates[b] = updated_gates[b], updated_gates[a]

        print(find_pair(updated_gates, set(gates), 4))




        for maybe in itertools.combinations(candidates, 4):
            for pair_one in itertools.combinations(maybe, 2):
                gatesm = gates.copy()
                a, b = pair_one
                c, d = set(maybe) - set(pair_one)
                gatesm[a], gatesm[b] = gatesm[b], gatesm[a]
                gatesm[c], gatesm[d] = gatesm[d], gatesm[c]
                if not self.get_cand(gatesm):
                    return ",".join(sorted(maybe))


        # print(test_gates(gates))

    # def solver(self, puzzle_input: InputType, part_one: bool) -> int | str:

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
