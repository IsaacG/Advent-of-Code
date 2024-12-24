#!/bin/python
"""Advent of Code, Day 24: Crossed Wires."""
from __future__ import annotations

import collections
import dataclasses
import functools
import itertools
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
            case ["PRE", "OR", "UPPER"]:
                self.type = "CARRY"
            case ["INPUT", "XOR", "INPUT"]:
                self.type = "LOWER"
            case ["INPUT", "AND", "INPUT"]:
                self.type = "UPPER"
            case ["CARRY", "XOR", "LOWER"] if self.name.startswith("z"):
                self.type = "OUTPUT"
            case ["LOWER", "AND", "UPPER"] if self.a.num == "01" and self.b.num == "00":
                self.type = "PRE"
            case ["CARRY", "AND", "LOWER"]:
                self.type = "PRE"

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

    def get_bad(self, gates):
        candidates = self.test_gates(gates, 0, 2**46-1)
        candidates |= self.test_gates(gates, 2**23-1, 0)
        candidates |= self.test_gates(gates, (2**23-1) << 22, 0)
        x = 0
        for i in range(22):
            x <<= 2
            x += 1
        candidates |= self.test_gates(gates, x, 0)
        return candidates

    def part2(self, puzzle_input: InputType) -> int:
        raw_inputs, raw_gates = puzzle_input
        gates = {}
        for a, op, b, _, out in raw_gates:
            gates[out] = (a, op, b)

        swaps = [("z34", "wcb"), ("cvp", "wjb"), ("z14", "qbw"), ("z10", "mkk")]
        for a, b in swaps:
            gates[a], gates[b] = gates[b], gates[a]

        known = {a for a, b in raw_inputs}
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
            n = str(node)
            if n in ["z00", "z01", "z45"]:
                continue
            parents = sorted(str(i) for i in [node.a, node.b])
            if n.startswith("z") and not (parents[0].startswith("CARRY") and parents[1].startswith("LOWER")):
                print(n, node.name, parents)
            if n.startswith("CARRY") and not (parents[0].startswith("PRE") and parents[1].startswith("UPPER")):
                print(n, node.name, parents)
            if n.startswith("PRE") and not (parents[0].startswith("CARRY") and parents[1].startswith("LOWER")):
                print(n, node.name, parents)
        out.append("}")
        pathlib.Path("a.dot").write_text("\n".join(out))
        return ",".join(sorted(i for swap in swaps for i in swap))


        target = len(self.get_bad(gates))
        print(target)
        return
        weird = set("cbv mfk mkk qcn mcb fdg cvp fqv z25 z26 pnm mpd cgh wcb mpd wcb".split())
        for a, b in itertools.combinations(weird, 2):
            for c, d in itertools.combinations(weird - {a, b}, 2):
                g = gates.copy()
                swaps = [(a, b), (c, d)]
                for a, b in swaps:
                    g[a], g[b] = g[b], g[a]
                    try:
                        got = len(self.get_bad(g))
                        if got < target:
                            print(got, a, b, c, d)
                    except:
                        pass





# vim:expandtab:sw=4:ts=4
