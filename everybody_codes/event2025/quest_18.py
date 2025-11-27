"""Everyone Codes Day N.

Part three. Solve for the specific input.
The source plants with free branches all have exactly two output branches.
The thickness of the output branches are either both positive or both negative.
We can solve for optimal/maximal output by turning off plants with negative output branches and turning on the others.
"""

import collections
import re
from lib import helpers
from lib import parsers


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    input_plants = set()
    plant_in = collections.defaultdict(set)
    plant_out = collections.defaultdict(list)
    thickness = {}
    free_branch_plants = set()
    if part == 1:
        plants = data
        scema = []
    else:
        plants, schemas_chunk = data.split("\n\n\n")
        schemas = []
        for line in schemas_chunk.splitlines():
            schemas.append([int(i) for i in line.split()])

    for chunk in plants.split("\n\n"):
        a, *b = chunk.splitlines()
        m = re.match(r"Plant (\d+) with thickness (-?\d+):", a)
        i, t = [int(i) for i in m.groups()]
        thickness[i] = t
        for line in b:
            if line == "- free branch with thickness 1":
                input_plants.add(i)
            else:
                m = re.match(r"- branch to Plant (\d+) with thickness (-?\d+)", line)
                s, t = [int(i) for i in m.groups()]
                plant_in[i].add((s, t))
                plant_out[s].append(t)
                
                free_branch_plants.add(s)

    if part == 1:
        schemas = [[1] * len(input_plants)]

    final = set(thickness) - free_branch_plants
    target = final.pop()

    def solve_for(schema):
        return solve_for_a(target, {i: j for i, j in enumerate(schema, 1)})

    def solve_for_a(target, solved):
        todo = set(thickness) - set(solved)
        total = len(thickness)
        while todo:
            i = next(i for i in todo if all(j in solved for j, _ in plant_in[i]))
            todo.remove(i)
            incoming = sum(t * solved[s] for s, t in plant_in[i])
            if incoming < thickness[i]:
                solved[i] = 0
            else:
                solved[i] = incoming
            if i == target:
                return solved[i]

    res = []
    for schema in schemas:
        res.append(solve_for(schema))
    if part < 3:
        return sum(res)

    def max_for(c):
        a, b = [s for s, _ in plant_in[c]]
        da = dict(plant_in[a])
        db = dict(plant_in[b])
        common = set(da) & set(db)
        solved = {}
        for i, j in da.items():
            solved[i] = 1 if j > 0 else 0
        for i, j in db.items():
            solved[i] = 1 if j > 0 else 0
        shared = common.pop()
        return max(
            solve_for_a(c, solved | {shared: k})
            for k in [0, 1]
        )

    most = sum(
        max_for(i) * j
        for i, j in plant_in[target]
    )

    for i in input_plants:
        assert len(plant_out[i]) == 2
        assert (plant_out[i][0] > 0) == (plant_out[i][1] > 0)
    mosta = solve_for_a(target, {i: 1 if plant_out[i][0] > 0 else 0 for i in input_plants})
    assert most == mosta

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
    # (3, TEST_DATA[2], 946),
]

if __name__ == "__main__":
    helpers.run_solution(globals())
