#!/bin/python
"""Advent of Code, Day 24: Crossed Wires."""

import collections
import copy
import itertools
import operator
import random
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
x02 OR y02 -> z02""",
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
tnw OR pbm -> gnj""",
]

OPS = {"AND": operator.and_, "OR": operator.or_, "XOR": operator.xor}


def compute(gates, values):
    gates = gates.copy()
    values = values.copy()
    assert len(values) == 2 * 45
    todo = set(gates)
    while todo:
        out = next(out for out in todo if gates[out][0] in values and gates[out][2] in values)
        a, op, b = gates[out]
        del gates[out]
        todo.remove(out)
        values[out] = OPS[op](values[a], values[b])
    z_vals = sorted(((i, j) for i, j in values.items() if i.startswith("z")), reverse=True)
    z_bits = "".join("1" if val else "0" for _, val in z_vals)
    return int(z_bits, 2)


def validate(gates, swaps):
    gates = gates.copy()
    for a, b in swaps:
        gates[a], gates[b] = gates[b], gates[a]
    inputs = {}
    patterns = [(random.randint(0, (1 << 45) - 1), random.randint(0, (1 << 45) - 1)) for _ in range(20)]
    for x, y in patterns:
        for idx, (char_x, char_y) in enumerate(zip(reversed(f"{x:045b}"), reversed(f"{y:045b}"))):
            inputs[f"x{idx:02}"] = bool(int(char_x))
            inputs[f"y{idx:02}"] = bool(int(char_y))
        got = compute(gates, inputs)
        want = x + y
        if got != x + y:
            print(f"Adder does not compute. {x} + {y} = {want} but got {got}")
            return False
    return True


class Solver:

    def build_state(self):
        every_other = 0
        for i in range(22):
            every_other <<= 2
            every_other += 1
        state = []
        patterns = [(random.randint(0, (1 << 45) - 1), random.randint(0, (1 << 45) - 1)) for _ in range(20)]
        for x, y in patterns:
            z = x + y
            assert x & (1 << 45) == 0
            assert y & (1 << 45) == 0
            gate_values = {}
            want_values = {}
            assert x & (1 << 45) == 0
            assert y & (1 << 45) == 0
            for idx, (char_x, char_y, char_z) in enumerate(zip(reversed(f"{x:046b}"), reversed(f"{y:046b}"), reversed(f"{z:046b}"))):
                j = f"{idx:02}"
                gate_values["x" + j] = bool(int(char_x))
                gate_values["y" + j] = bool(int(char_y))
                want_values["z" + j] = bool(int(char_z))
            state.append((gate_values, want_values))
        return state

    def required_gates(self, to_compute, gates, solved_gates):
        todo = to_compute.copy()
        required_gates = set()
        seen = set()
        while todo:
            gate = todo.pop()
            seen.add(gate)
            if gate not in solved_gates:
                required_gates.add(gate)
            if gate not in gates:
                continue
            for parent in gates[gate][::2]:
                if parent not in solved_gates and parent not in seen:
                    todo.add(parent)
        return required_gates

    def solve_for_bit(self, bit, gates, solved_gates, state):
        bit_n = f"{bit:02}"
        valid = True
        required_gates = self.required_gates({f"z{bit_n}"}, gates, solved_gates)

        solutions = []
        for gate_values, want_values in state:
            new_values = {}
            combined = collections.ChainMap(gate_values, new_values)
            todo = required_gates.copy()
            assert required_gates.isdisjoint(gate_values), required_gates - set(gate_values)
            while todo:
                gate = next((i for i in todo if all(parent in combined for parent in gates[i][::2])), None)
                if gate is None:
                    return [], False
                todo.remove(gate)
                op = OPS[gates[gate][1]]
                vals = [combined[parent] for parent in gates[gate][::2]]
                new_values[gate] = op(*vals)
            assert set(new_values) == required_gates
            valid = valid and (new_values[f"z{bit_n}"] == want_values[f"z{bit_n}"])
            solutions.append(new_values)
        return solutions, valid

    def solve_from(self, start_bit, swaps_left, solved_gates, gates, state):
        swaps = []

        for bit in range(start_bit, 46):
            bit_n = f"{bit:02}"
            solutions, valid = self.solve_for_bit(bit, gates, solved_gates, state)
            if valid:
                for (gate_values, _), new_values in zip(state, solutions):
                    gate_values.update(new_values)
            elif not swaps_left:
                return [], False
            else:
                candidates = self.required_gates({f"z{bit_n}", f"z{bit + 1:02}"} & set(gates), gates, solved_gates)
                viable = []
                for a, b in itertools.combinations(sorted(candidates), 2):
                    try_gates = gates.copy()
                    try_gates[a], try_gates[b] = try_gates[b], try_gates[a]

                    solutions, valid = self.solve_for_bit(bit, try_gates, solved_gates, state)
                    if valid:
                        viable.append((a, b))
                if viable:
                    print(f"Bit {bit} is broken. Swaps which fix this bit: {viable}")

                for a, b in viable:
                    try_gates = gates.copy()
                    try_gates[a], try_gates[b] = try_gates[b], try_gates[a]

                    subswaps, valid = self.solve_from(bit, swaps_left - 1, solved_gates.copy(), try_gates.copy(), copy.deepcopy(state))
                    if valid:
                        return sorted([(a, b)] + subswaps), True
                return [], False
            required_gates = self.required_gates({f"z{bit_n}"}, gates, solved_gates)
            solved_gates.update(required_gates)
        return [], validate(gates, [])


class Day24(aoc.Challenge):
    """Day 24: Crossed Wires."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=4),
        aoc.TestCase(part=1, inputs=SAMPLE[1], want=2024),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]
    INPUT_PARSER = aoc.ParseBlocks([aoc.BaseParseMultiPerLine(word_separator=": "), aoc.parse_multi_str_per_line])

    def part1(self, puzzle_input: tuple[list[str], list[str]]) -> int:
        raw_inputs, raw_gates = puzzle_input
        values = {a: bool(int(b)) for a, b in raw_inputs}
        gates = {}
        for a, op, b, _, out in raw_gates:
            gates[out] = (a, op, b)
        return compute(gates, values)

    def part2(self, puzzle_input: tuple[list[str], list[str]]) -> int:
        raw_inputs, raw_gates = puzzle_input
        gates = {}
        for a, op, b, _, out in raw_gates:
            gates[out] = (a, op, b)

        solver = Solver()
        state = solver.build_state()
        known_values = set(state[0][0])
        swaps, _ = solver.solve_from(0, 4, known_values, gates, state)

        print(f"Validating swaps {swaps}...")
        print(validate(gates, swaps))
        return ",".join(sorted(a for swap in swaps for a in swap))

# vim:expandtab:sw=4:ts=4
