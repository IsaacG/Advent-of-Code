"""Everyone Codes Day N."""

import collections
import itertools
import logging
import re
from lib import helpers
from lib import parsers

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    b_free = set()
    b_in = collections.defaultdict(set)
    thick = {}
    is_src = set()
    if part == 1:
        plants = data
        scema = []
    else:
        plants, schema_chunk = data.split("\n\n\n")
        schema = []
        for line in schema_chunk.splitlines():
            schema.append([int(i) for i in line.split()])

    for chunk in plants.split("\n\n"):
        a, *b = chunk.splitlines()
        m = re.match(r"Plant (\d+) with thickness (-?\d+):", a)
        assert m
        i, t = [int(i) for i in m.groups()]
        thick[i] = t
        for line in b:
            if line == "- free branch with thickness 1":
                b_free.add(i)
            else:
                m = re.match(r"- branch to Plant (\d+) with thickness (-?\d+)", line)
                assert m, line
                s, t = [int(i) for i in m.groups()]
                b_in[i].add((s, t))
                is_src.add(s)

    if part == 1:
        schema = [[1] * len(b_free)]

    final = set(thick) - is_src
    target = final.pop()

    def solve_for(schem):
        final = set(thick) - is_src
        assert len(final) == 1
        target = final.pop()
        solved = {i: 1 if schem[i-1] else 0 for i in b_free}
        todo = set(thick) - set(solved)
        total = len(thick)
        while todo:
            i = next(i for i in todo if all(j in solved for j, _ in b_in[i]))
            todo.remove(i)
            incoming = sum(t * solved[s] for s, t in b_in[i])
            if incoming < thick[i]:
                solved[i] = 0
            else:
                solved[i] = incoming
            if i == target:
                return solved[i]

    def solve_for_a(target, solved):
        todo = set(thick) - set(solved)
        total = len(thick)
        while todo:
            i = next(i for i in todo if all(j in solved for j, _ in b_in[i]))
            todo.remove(i)
            incoming = sum(t * solved[s] for s, t in b_in[i])
            if incoming < thick[i]:
                solved[i] = 0
            else:
                solved[i] = incoming
            if i == target:
                return solved[i]

    res = []
    for schem in schema:
        res.append(solve_for(schem))
    if part < 3:
        return sum(res)

    def max_for(c):
        a, b = [s for s, _ in b_in[c]]
        da = dict(b_in[a])
        db = dict(b_in[b])
        common = set(da) & set(db)
        print(f"{c} = {a} + {b}; {common=}")
        solved = {}
        for i, j in da.items():
            solved[i] = 1 if j > 0 else 0
        for i, j in db.items():
            solved[i] = 1 if j > 0 else 0
        shared = common.pop()
        assert not common
        return max(
            solve_for_a(c, solved | {shared: k})
            for k in [0, 1]
        )

    # print(target)
    # for i in b_in:
    #     print(i, " ".join(str(j) for j, _ in sorted(b_in[i])))
    for i in range(100, target):
        print("max", i, max_for(i))
    most = sum(
        max_for(i) * j
        for i, j in b_in[target]
    )
    assert most > max(res)

    total = 0
    for r in res:
        if r:
            total += most - r
    return total








PARSER = parsers.parse_one_str
TEST_DATA = [
    """\
Plant 1 with thickness 1:
- free branch with thickness 1

Plant 2 with thickness 1:
- free branch with thickness 1

Plant 3 with thickness 1:
- free branch with thickness 1

Plant 4 with thickness 17:
- branch to Plant 1 with thickness 15
- branch to Plant 2 with thickness 3

Plant 5 with thickness 24:
- branch to Plant 2 with thickness 11
- branch to Plant 3 with thickness 13

Plant 6 with thickness 15:
- branch to Plant 3 with thickness 14

Plant 7 with thickness 10:
- branch to Plant 4 with thickness 15
- branch to Plant 5 with thickness 21
- branch to Plant 6 with thickness 34""",
    """\
Plant 1 with thickness 1:
- free branch with thickness 1

Plant 2 with thickness 1:
- free branch with thickness 1

Plant 3 with thickness 1:
- free branch with thickness 1

Plant 4 with thickness 10:
- branch to Plant 1 with thickness -25
- branch to Plant 2 with thickness 17
- branch to Plant 3 with thickness 12

Plant 5 with thickness 14:
- branch to Plant 1 with thickness 14
- branch to Plant 2 with thickness -26
- branch to Plant 3 with thickness 15

Plant 6 with thickness 150:
- branch to Plant 4 with thickness 5
- branch to Plant 5 with thickness 6


1 0 1
0 0 1
0 1 1""",
    """\
Plant 1 with thickness 1:
- free branch with thickness 1

Plant 2 with thickness 1:
- free branch with thickness 1

Plant 3 with thickness 1:
- free branch with thickness 1

Plant 4 with thickness 1:
- free branch with thickness 1

Plant 5 with thickness 8:
- branch to Plant 1 with thickness -8
- branch to Plant 2 with thickness 11
- branch to Plant 3 with thickness 13
- branch to Plant 4 with thickness -7

Plant 6 with thickness 7:
- branch to Plant 1 with thickness 14
- branch to Plant 2 with thickness -9
- branch to Plant 3 with thickness 12
- branch to Plant 4 with thickness 9

Plant 7 with thickness 23:
- branch to Plant 5 with thickness 17
- branch to Plant 6 with thickness 18


0 1 0 0
0 1 0 1
0 1 1 1
1 1 0 1""",
]
TESTS = [
    (1, TEST_DATA[0], 774),
    (2, TEST_DATA[1], 324),
    (3, TEST_DATA[2], 946),
]

if __name__ == "__main__":
    helpers.run_solution(globals())
