"""Codyssi Day N."""

import collections
import logging
import operator

log = logging.info
MOD = 1073741824
OPS = {"ADD": operator.add, "SUB": operator.sub, "MULTIPLY": operator.mul}

def solve(part: int, data: str, testing: bool) -> int:
    """Solve the parts."""
    initial_r, instructions_r, flow_r = data.split("\n\n")
    flows = flow_r.splitlines()
    heights = {
        (x, y): int(val)
        for y, row in enumerate(initial_r.splitlines())
        for x, val in enumerate(row.split())
    }
    size = len(initial_r.splitlines())

    positions_all = list(heights)
    positions = {
        "ROW": {y: [(x, y) for x in range(size)] for y in range(size)},
        "COL": {x: [(x, y) for y in range(size)] for x in range(size)},
    }
    

    if part == 1 and testing:
        for y in range(size):
            log(" ".join(str(heights[x, y]).rjust(5) for x in range(size)))
        log("")

    instructions = collections.deque(instructions_r.splitlines())

    if part != 1:
        taken = None
        actions = []
        while taken is None or (part == 3 and instructions):
            for flow in flows:
                if flow == "TAKE":
                    if not instructions:
                        break
                    taken = instructions.popleft()
                elif flow == "ACT":
                    actions.append(taken)
                elif flow == "CYCLE":
                    instructions.append(taken)
        instructions = actions

    for line in instructions:
        words = line.split()
        if words[0] in OPS:
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
        else:
            # SHIFT {ROW/COL} {number} BY {shift amount}
            _, rc, number, _, amount_s = words
            amount = size - (int(amount_s) % size)
            targets = positions[rc][int(number) - 1]
            vals = [heights[t] for t in targets[amount:] + targets[:amount]]
            assert len(vals) == size
            for t, v in zip(targets, vals):
                heights[t] = v
        if part == 1 and testing:
            log(line)
            for y in range(size):
                log(" ".join(str(heights[x, y]).rjust(5) for x in range(size)))
            log("")

    got = max(sum(heights[pos] for pos in targets) for rc in positions.values() for targets in rc.values())
    assert got != 14477269239
    return got


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
