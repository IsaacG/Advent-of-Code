"""Codyssi Day N."""

import collections
import itertools
import operator

MOD = 1073741824
OPS = {"ADD": operator.add, "SUB": operator.sub, "MULTIPLY": operator.mul}

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    initial_r, instructions_r, flow_r = data.split("\n\n")
    heights = {
        (x, y): int(val)
        for y, row in enumerate(initial_r.splitlines())
        for x, val in enumerate(row.split())
    }
    size = len(initial_r.splitlines())
    instructions = collections.deque(instructions_r.splitlines())
    flows: collections.abc.Iterable[str] = flow_r.splitlines()

    positions_all = list(heights)
    positions = {
        "ROW": {y: [(x, y) for x in range(size)] for y in range(size)},
        "COL": {x: [(x, y) for y in range(size)] for x in range(size)},
    }

    # Apply flow control for parts 2 and 3.
    if part != 1:
        taken = ""
        actions = []
        if part == 3:
            # Part 2 runs through the flows once. Part 3 does so repeatedly.
            flows = itertools.cycle(flows)
        for flow in flows:
            if flow == "TAKE":
                if not instructions:
                    break
                taken = instructions.popleft()
            elif flow == "ACT":
                actions.append(taken)
            elif flow == "CYCLE":
                instructions.append(taken)
        instructions = collections.deque(actions)

    # Apply instructions
    for line in instructions:
        words = line.split()
        if words[0] == "SHIFT":
            # SHIFT {ROW/COL} {number} BY {shift amount}
            _, rc, number, _, amount_s = words
            amount = size - (int(amount_s) % size)
            # Get the positions we operate on.
            targets = positions[rc][int(number) - 1]
            # Copy the values in the new position.
            vals = [heights[t] for t in targets[amount:] + targets[:amount]]
            # Update values.
            for t, v in zip(targets, vals):
                heights[t] = v
        else:
            # {ADD/SUB/MULTIPLY} {amount} {ROW/COL} {number}
            # {ADD/SUB/MULTIPLY} {amount} ALL
            op_s, amount_s, *target = line.split()
            op = OPS[op_s]
            amount = int(amount_s)

            if target[0] == "ALL":
                targets = positions_all
            else:
                targets = positions[target[0]][int(target[1]) - 1]
            for pos in targets:
                heights[pos] = op(heights[pos], amount) % MOD

    return max(sum(heights[pos] for pos in targets) for rc in positions.values() for targets in rc.values())


TEST_DATA = """\
222 267 922 632 944
110 33 503 758 129
742 697 425 362 568
833 408 425 349 631
874 671 202 430 602

SHIFT COL 2 BY 1
MULTIPLY 4 COL 5
SUB 28 ALL
SHIFT COL 4 BY 2
MULTIPLY 4 ROW 4
ADD 26 ROW 3
SHIFT COL 4 BY 2
ADD 68 ROW 2

TAKE
CYCLE
TAKE
ACT
TAKE
CYCLE"""
TESTS = [
    (1, TEST_DATA, 18938),
    (2, TEST_DATA, 11496),
    (3, TEST_DATA, 19022),
]
