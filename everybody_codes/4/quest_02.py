"""Everyone Codes: Quest 4, Day 2."""

import itertools
from lib import helpers


def solve(part: int, data: list[str]) -> int:
    """Solve the parts."""
    # Parse the input
    parsed = {}
    for line in data:
        key, val = line.split("=")
        if val.startswith("[") and val.endswith("]"):
            val = tuple(eval(val))
        parsed[key] = val

    pos = parsed["START"]
    seen = {pos}
    todo = [pos]
    # Parts 1, 2: follow the MOVES. Part 3: try all possible moves.
    targets_generator = itertools.repeat("ABC") if part == 3 else parsed["MOVES"]

    for targets in targets_generator:
        ax, ay = todo.pop()
        for target in targets:
            bx, by = parsed[target]
            pos = (ax + bx) // 2, (ay + by) // 2
            # Part 1, 2: position can move to a repeated location.
            # Part 3: do not queue a repeat.
            if part < 3 or pos not in seen:
                seen.add(pos)
                todo.append(pos)
        if not todo:
            break
    if part == 1:
        return len(seen)
    fireflies = {(x + dx, y + dy) for dx, dy in helpers.FOUR_DIRECTIONS_T for x, y in seen}
    return len(fireflies - seen)


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
