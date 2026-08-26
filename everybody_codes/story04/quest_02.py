"""Everyone Codes Day N."""

import logging
from lib import helpers
from lib import parsers

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    d = {}
    for line in data:
        k, v = line.split("=")
        if v.startswith("[") and v.endswith("]"):
            v = eval(v)
        d[k] = v
    pos = tuple(d["START"])
    seen = {pos}
    if part < 3:
        for target in d["MOVES"]:
            ax, ay = pos
            bx, by = d[target]
            pos = (ax + bx) // 2, (ay + by) // 2
            seen.add(pos)
        if part == 1:
            return len(seen)
        ff = {(x + dx, y + dy) for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)] for x, y in seen}
        return len(ff - seen)

    todo = [pos]
    while todo:
        ax, ay = todo.pop()
        for target in "ABC":
            bx, by = d[target]
            pos = (ax + bx) // 2, (ay + by) // 2
            if pos not in seen:
                seen.add(pos)
                todo.append(pos)
    ff = {(x + dx, y + dy) for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)] for x, y in seen}
    return len(ff - seen)


# PARSER = parsers.parse_one_str
TEST_DATA = [
    """\
START=[5,0]
A=[0,0]
B=[10,0]
C=[5,10]
MOVES=ABCCBABCA""",
    """\
START=[5,0]
A=[0,0]
B=[10,0]
C=[5,10]
MOVES=BABCAABBCABCCCBBABCCCAAACABABCBCBBCAABBABBCACCBAABCBCBBBCBBBBBCCCAACAACB""",
    """\
START=[5,0]
A=[0,0]
B=[10,0]
C=[5,10]""",
    """\
START=[0,0]
A=[0,0]
B=[80,15]
C=[5,30]""",
    """\
""",
]
TESTS = [
    (1, TEST_DATA[0], 8),
    (2, TEST_DATA[0], 25),
    (2, TEST_DATA[1], 46),
    (3, TEST_DATA[2], 42),
    (3, TEST_DATA[3], 432),
]

if __name__ == "__main__":
    helpers.run_solution(globals())
