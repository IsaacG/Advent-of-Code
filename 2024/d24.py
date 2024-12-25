#!/bin/python
"""Advent of Code, Day 24: Crossed Wires."""
from __future__ import annotations

import collections
import copy
import dataclasses
import functools
import itertools
import operator
import pathlib
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
OPS = {"AND": operator.and_, "OR": operator.or_, "XOR": operator.xor}


class Solver:
    def __init__(self, gates):
        self.gates = gates

    def build_state(self):
        every_other = 0
        for i in range(22):
            every_other <<= 2
            every_other += 1
        patterns = [(2**46 - 1, 2**46 - 1), (0, 0), (0, 2**46 - 1), (every_other, every_other), (every_other << 1, every_other << 1)]
        state = []
        for x, y in patterns:
            z = x + y
            gate_values = {}
            want_values = {}
            for i in range(46):
                j = f"{i:02}"
                if i != 45:
                    gate_values[f"x{j}"] = bool(x & (1 << i))
                    gate_values[f"y{j}"] = bool(y & (1 << i))
                want_values[f"z{j}"] = bool(z & (1 << i))
            # print(x, y, z)
            # print(gate_values, want_values)
            state.append((gate_values, want_values))
        return state

    def required_gates(self, to_compute, all_gates, solved_gates, parents):
        todo = to_compute.copy()
        required_gates = set()
        seen = set()
        while todo:
            gate = todo.pop()
            seen.add(gate)
            if gate not in solved_gates:
                required_gates.add(gate)
            if gate not in all_gates:
                continue
            for parent in parents[gate]:
                if parent not in solved_gates and parent not in seen:
                    todo.add(parent)
        return required_gates

    def solve_for_bit(self, bit, solved_gates, required_gates, state, ops, parents):
        bit_n = f"{bit:02}"
        valid = True

        solutions = []
        for gate_values, want_values in state:
            new_values = {}
            combined = collections.ChainMap(gate_values, new_values)
            todo = required_gates.copy()
            assert required_gates.isdisjoint(gate_values), required_gates - set(gate_values)
            while todo:
                gate = next((i for i in todo if all(parent in combined for parent in parents[i])), None)
                if gate is None:
                    return [], False
                todo.remove(gate)
                op = ops[gate]
                vals = [combined[parent] for parent in parents[gate]]
                new_values[gate] = op(*vals)
            assert set(new_values) == required_gates
            valid = valid and (new_values[f"z{bit_n}"] == want_values[f"z{bit_n}"])
            # if not valid:
            #     print(gate_values[f"x{bit_n}"], gate_values[f"y{bit_n}"], new_values[f"z{bit_n}"])
            #     print(f'{new_values[f"z{bit_n}"]} != {want_values[f"z{bit_n}"]}')
            solutions.append(new_values)
        return solutions, valid

    def solve_from(self, start_bit, swaps_left, solved_gates, gates, state):
        parents = {gate: [a, b] for gate, (a, _, b) in gates.items()}
        ops = {gate: OPS[op] for gate, (_, op, _) in gates.items()}
        swaps = []

        for bit in range(start_bit, 45):
            bit_n = f"{bit:02}"
            required_gates = self.required_gates({f"z{bit_n}"}, gates, solved_gates, parents)
            solutions, valid = self.solve_for_bit(bit, solved_gates, required_gates, state, ops, parents)
            if valid:
                # print(f"Successfully computed bit {bit}")
                for (gate_values, _), new_values in zip(state, solutions):
                    gate_values.update(new_values)
            elif not swaps_left:
                return [], False
            else:
                candidates = self.required_gates({f"z{bit_n}", f"z{bit + 1:02}"} & set(gates), gates, solved_gates, parents)
                viable = []
                # print(f"Failed to compute bit {bit}: {candidates} has an issue")
                for a, b in itertools.combinations(candidates, 2):
                    try_gates = self.gates.copy()
                    try_gates[a], try_gates[b] = try_gates[b], try_gates[a]

                    parents = {gate: [a, b] for gate, (a, _, b) in try_gates.items()}
                    ops = {gate: OPS[op] for gate, (_, op, _) in try_gates.items()}
                    required_gates = self.required_gates({f"z{bit_n}"}, try_gates, solved_gates, parents)
                    solutions, valid = self.solve_for_bit(bit, solved_gates, required_gates, state, ops, parents)
                    if not valid: continue
                    print("Try swapping", a, b, swaps_left)

                    subswaps, valid = self.solve_from(bit, swaps_left - 1, solved_gates.copy(), try_gates.copy(), copy.deepcopy(state))
                    if valid:
                        print(f"{a=}, {b=}, {subswaps=}")
                        return [a, b] + subswaps, True
                return [], False
            solved_gates.update(required_gates)
        return [], True

    def solve(self):
        solved_gates = {f"x{bit:02}" for bit in range(45)}
        solved_gates |= {f"y{bit:02}" for bit in range(45)}
        state = self.build_state()

        return self.solve_from(0, 4, solved_gates, self.gates, self.build_state())


@dataclasses.dataclass
class Node:
    a: Node | None
    b: Node | None
    op: str
    name: str

    def __post_init__(self):
        self.type = "XXX"
        self.num = None
        if not self.a:
            self.num = self.name.removeprefix("x").removeprefix("y")
            self.type = "INPUT"
            return
        self.num = max(self.a.num, self.b.num)
        if self.a.type > self.b.type:
            self.a, self.b = self.b, self.a

        match self.a.type, self.op, self.b.type:
            case ["CARRY", "XOR", "LOWER"] if self.name.startswith("z"):
                self.type = "OUTPUT"
            case ["LOWER", "AND", "UPPER"] if self.a.num == "01" and self.b.num == "00":
                self.type = "PRE"
        patterns = {
            ("PRE", "OR", "UPPER"): "CARRY",
            ("INPUT", "XOR", "INPUT"): "LOWER",
            ("INPUT", "AND", "INPUT"): "UPPER",
            ("CARRY", "AND", "LOWER"): "PRE",
        }
        for (a, op, b), n_type in patterns.items():
            if {self.a.type, self.b.type} < {"XXX", a, b} and self.op == op:
                self.type = n_type

        if self.name == "z00" or self.name == "z01":
            self.type = "OUTPUT"
        self.num = max(self.a.num, self.b.num)

        if self.type == "XXX":
            print(f"Bad node {self.a.type}, {self.op}, {self.b.type}, {self.name}")

    def __str__(self):
        parts = [self.type, self.name]
        if self.num:
            parts.append(self.num)
        return "_".join(parts)
        

class Day24(aoc.Challenge):
    """Day 24: Crossed Wires."""

    DEBUG = True
    # Default is True. On live solve, submit one tests pass.
    # SUBMIT = {1: False, 2: False}

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=4),
        aoc.TestCase(part=1, inputs=SAMPLE[1], want=2024),
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

    def part2(self, puzzle_input: InputType) -> int:
        raw_inputs, raw_gates = puzzle_input
        gates = {}
        for a, op, b, _, out in raw_gates:
            gates[out] = (a, op, b)

        solver = Solver(gates)
        return ",".join(sorted(solver.solve()[0]))
        known = {a for a, b in raw_inputs}
        unknown = set(gates)

        swaps = [("z10", "mkk"), ("z14", "qbw"), ("cvp", "wjb"), ("z34", "wcb")]
        for a, b in swaps:
            gates[a], gates[b] = gates[b], gates[a]

        solver = Solver(gates)
        solver.solve()

        todo = set(gates)
        nodes = {}
        for g in known:
            nodes[g] = Node(None, None, "SET", g)
        while todo:
            do = next(g for g in todo if gates[g][0] in known and gates[g][2] in known)
            a, op, b = gates[do]
            todo.remove(do)
            known.add(do)
            nodes[do] = Node(nodes[a], nodes[b], op, do)

        out = []
        out.append("digraph {")
        for node in nodes.values():
            color = {"INPUT": "blue", "UPPER": "red", "LOWER": "green", "PRE": "yellow", "OUTPUT": "brown", "CARRY": "coral3", "XXX": "black"}
            out.append(f'{node} [style=filled color="{color[node.type]}"]')
            if node.a is None:
                continue
            out.append(f"{node.a} -> {node}")
            out.append(f"{node.b} -> {node}")
        out.append("}")
        pathlib.Path("a.dot").write_text("\n".join(out))
        return ",".join(sorted(i for swap in swaps for i in swap))




# vim:expandtab:sw=4:ts=4
