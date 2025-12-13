#!/bin/python
"""Advent of Code, Day 24: Crossed Wires."""

import collections
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
Circuit = dict[str, tuple[str, collections.abc.Callable[[bool, bool], bool], str]]
SolverState = tuple[dict[str, bool], dict[str, bool]]


class Day24(aoc.Challenge):
    """Day 24: Crossed Wires. Simulate a digital circuit then swap gates to make it a valid adder."""

    TESTS = [
        aoc.TestCase(part=1, inputs=SAMPLE[0], want=4),
        aoc.TestCase(part=1, inputs=SAMPLE[1], want=2024),
        aoc.TestCase(part=2, inputs=SAMPLE[0], want=aoc.TEST_SKIP),
    ]
    # Split the input into two blocks. Convert each block into a list of words for each line.
    INPUT_PARSER = aoc.ParseBlocks([aoc.ParseDict(separator=": ", scalar=True), aoc.parse_multi_str_per_line])

    def compute(self, circuit: Circuit, values: dict[str, bool]):
        """Propagate values through a bunch of gates to compute the final z value."""
        values = values.copy()
        todo = set(circuit)
        while todo:
            out = next(out for out in todo if circuit[out][0] in values and circuit[out][2] in values)
            a, op, b = circuit[out]
            todo.remove(out)
            values[out] = op(values[a], values[b])
        z_vals = sorted(((i, j) for i, j in values.items() if i.startswith("z")), reverse=True)
        z_bits = "".join("1" if val else "0" for _, val in z_vals)
        return int(z_bits, 2)

    def build_state(self) -> list[SolverState]:
        """Generate circuit inputs/states used to test/repair the circuit."""
        max_input = (1 << 45) - 1
        state = []
        for _ in range(20):
            x = random.randint(0, max_input)
            y = random.randint(0, max_input)
            z = x + y
            gate_values = {}
            want_values = {}
            for idx, (char_x, char_y, char_z) in enumerate(zip(*[reversed(f"{i:046b}") for i in [x, y, z]])):
                j = f"{idx:02}"
                gate_values["x" + j] = bool(int(char_x))
                gate_values["y" + j] = bool(int(char_y))
                want_values["z" + j] = bool(int(char_z))
            state.append((gate_values, want_values))
        return state

    def required_gates(self, target_nodes: set[str], circuit: Circuit, solved_gates: set[str]) -> set[str]:
        """Return which unsolved gates need to be resolved to compute specific target nodes."""
        todo = target_nodes.copy()
        required_gates = set()
        seen = set()
        while todo:
            gate = todo.pop()
            seen.add(gate)
            if gate not in solved_gates:
                required_gates.add(gate)
            if gate not in circuit:
                continue
            for parent in circuit[gate][::2]:
                if parent not in solved_gates and parent not in seen:
                    todo.add(parent)
        return required_gates

    def solve_for_bit(self, bit: int, circuit: Circuit, solved_gates: set[str], state: list[SolverState]):
        """Compute one bit of output for each state and check if the output is correct, returning an updated state."""
        bit_n = f"{bit:02}"
        valid = True
        required_gates = self.required_gates({f"z{bit_n}"}, circuit, solved_gates)

        solutions = []
        for gate_values, want_values in state:
            gate_values = gate_values.copy()
            todo = required_gates.copy()
            while todo:
                gate = next((i for i in todo if all(parent in gate_values for parent in circuit[i][::2])), None)
                if gate is None:
                    return [], False
                todo.remove(gate)
                op = circuit[gate][1]
                vals = [gate_values[parent] for parent in circuit[gate][::2]]
                gate_values[gate] = op(*vals)
            valid = valid and (gate_values[f"z{bit_n}"] == want_values[f"z{bit_n}"])
            solutions.append((gate_values, want_values))
        return solutions, valid

    def solve_from(
        self,
        start_bit: int,
        swaps_remaining: int,
        solved_gates: set[str],
        circuit: Circuit,
        state: list[SolverState],
    ) -> tuple[list[tuple[str, str]], bool]:
        """Test and repair a circuit, starting from a given point with a max number of swaps."""
        for bit in range(start_bit, 46):
            bit_n = f"{bit:02}"
            solutions, valid = self.solve_for_bit(bit, circuit, solved_gates, state)
            if valid:
                state = solutions
            elif not swaps_remaining:
                return [], False
            else:
                candidates = self.required_gates({f"z{bit_n}", f"z{bit + 1:02}"} & set(circuit), circuit, solved_gates)
                viable = []
                for a, b in itertools.combinations(sorted(candidates), 2):
                    try_gates = circuit.copy()
                    try_gates[a], try_gates[b] = try_gates[b], try_gates[a]

                    solutions, valid = self.solve_for_bit(bit, try_gates, solved_gates, state)
                    if valid:
                        viable.append((a, b))
                if viable:
                    self.debug(f"Bit {bit} is broken. Swaps which fix this bit: {viable}")

                for a, b in viable:
                    try_gates = circuit.copy()
                    try_gates[a], try_gates[b] = try_gates[b], try_gates[a]

                    subswaps, valid = self.solve_from(
                        bit,
                        swaps_remaining - 1,
                        solved_gates.copy(),
                        try_gates.copy(),
                        [(a.copy(), b.copy()) for a, b in state],
                    )
                    if valid:
                        return sorted([(a, b)] + subswaps), True
                return [], False
            required_gates = self.required_gates({f"z{bit_n}"}, circuit, solved_gates)
            solved_gates.update(required_gates)
        return [], True

    def part1(self, puzzle_input: tuple[list[list[str]], list[list[str]]]) -> int:
        """Return the output of the circuit for a given input."""
        raw_values, raw_gates = puzzle_input
        values = {k: bool(v) for k, v in raw_values.items()}
        circuit = {out: (a, OPS[op], b) for a, op, b, _, out in raw_gates}
        return self.compute(circuit, values)

    def part2(self, puzzle_input: tuple[list[list[str]], list[list[str]]]) -> str:
        """Return which wires need to be swapped to turn a circuit into a working adder."""
        _, raw_gates = puzzle_input
        circuit = {out: (a, OPS[op], b) for a, op, b, _, out in raw_gates}

        state = self.build_state()
        known_values = set(state[0][0])
        swaps, _ = self.solve_from(0, 4, known_values, circuit, state)

        self.debug(f"Validating swaps {swaps}...")
        return ",".join(sorted(a for swap in swaps for a in swap))

# vim:expandtab:sw=4:ts=4
