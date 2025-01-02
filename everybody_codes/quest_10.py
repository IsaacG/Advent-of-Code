"""Everyone Codes Day N."""
import collections
import string

def neighbors(x: int, y: int) -> set[tuple[int, int]]:
    return {(x + 6, y), (x - 6, y), (x, y + 6), (x, y - 6)}

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    if part == 1:
        return get_ruin(data)

    lines = data.splitlines()
    if part == 2:
        total = 0
        for x in range(0, len(lines[0]), 9):
            for y in range(0, len(lines), 9):
                block = "\n".join(lines[line_idx][x : x + 8] for line_idx in range(y, y + 8))
                ruin = get_ruin(block)
                total += ruin_power(ruin)
        return total

    if part == 3:
        return solve3(data)


def solve3(data):
    lines = data.splitlines()
    chars = {(x, y): letter for y, line in enumerate(lines) for x, letter in enumerate(line)}
    max_x = len(lines[0]) - 1
    max_y = len(lines) - 1
    width = (len(lines[0]) - 2) // 6
    height = (len(lines) - 2) // 6
    total_blocks = width * height
    ruins = []

    todo = collections.deque((x * 6, y * 6) for x in range(width) for y in range(height))
    # print("todo", len(todo), todo)

    def solve_one(corner_x, corner_y):
        spots = [(x, y) for y in range(corner_y + 2, corner_y + 6) for x in range(corner_x + 2, corner_x + 6)]
        # print(f"solve_one({corner_x}, {corner_y}): {spots}")
        # print(f"solve_one({corner_x}, {corner_y})")
        todo = set(spots)
        solved = {}
        used = {"?"}
        char_updates = {}
        progress = True
        while progress and todo:
            progress = False
            for x, y in todo.copy():
                candidates_x = {(x, corner_y + n): chars[x, corner_y + n] for n in [0, 1, 6, 7]}
                candidates_y = {(corner_x + n, y): chars[corner_x + n, y] for n in [0, 1, 6, 7]}
                questions = [(x, y) for (x, y), char in (candidates_x | candidates_y).items() if char == "?"]
                candidates = (set(candidates_x.values()) & set(candidates_y.values())) - used
                # print(f"{x,y}: col:{list(candidates_x.values())} row:{list(candidates_y.values())}, {candidates=}, {questions=}")
                if len(candidates) == 1:
                    letter = candidates.pop()
                    solved[x, y] = letter
                    used.add(letter)
                    todo.remove((x, y))
                    progress = True
                elif len(questions) == 1:
                    if "?" in candidates_x.values():
                        candidates = set(candidates_y.values()) - used
                    else:
                        candidates = set(candidates_x.values()) - used
                    if len(candidates) == 1:
                        letter = candidates.pop()
                        solved[x, y] = letter
                        used.add(letter)
                        todo.remove((x, y))
                        char_updates[*questions[0]] = letter
                        # print(f"Solve ? {x, y} - {questions[0]} = {letter}")
                        progress = True
        if not todo:
            # print("Solved", corner_x, corner_y, char_updates)
            chars.update(char_updates)
            return [solved[pos] for pos in spots]

    def solve_next():
        for _ in range(len(todo)):
            attempt = todo[0]
            # print(f"solve_next() {attempt=}")
            got = solve_one(*attempt)
            if got is not None:
                solved = todo.popleft()
                # print("solve_next() {solved=} {got}")
                return got
            else:
                # print(f"Did not solve {attempt}; rotate.")
                todo.rotate()
        return None

    count = 0
    total = 0
    while (ruin := solve_next()):
        # print(ruin)
        total += ruin_power(ruin)
        count += 1
    # print(f"{count=}, {total=}")
    return total


    updated = 0
    for corner_x, corner_y in ((x * 6 + 1, y * 6 + 1) for x in range(width) for y in range(height)):
        for x, y in ((x, y) for y in range(corner_y + 1, corner_y + 5) for x in range(corner_x + 1, corner_x + 5)):
            candidates_x = {(x, n): chars[x, n] for n in [0, max_y, corner_y, corner_y + 5]}
            candidates_y = {(n, y): chars[n, y] for n in [0, max_x, corner_x, corner_x + 5]}
            pos = [(x, y) for (x, y), char in (candidates_x | candidates_y).items() if char == "?"]
            if len(pos) == 1:
                q_x, q_y = pos[0]
                if "?" in candidates_x.values():
                    candidates = set(candidates_y.values()) - set(candidates_x.values())
                else:
                    candidates = set(candidates_x.values()) - set(candidates_y.values())
                if len(candidates) == 1:
                    chars[pos[0]] = candidates.pop()
                    updated += 1
    print(f"{updated=}")

    total = 0
    for corner_x, corner_y in ((x * 6 + 1, y * 6 + 1) for x in range(width) for y in range(height)):
        ruin = []
        for x, y in ((x, y) for y in range(corner_y + 1, corner_y + 5) for x in range(corner_x + 1, corner_x + 5)):
            candidates_x = {chars[x, n] for n in [0, max_y, corner_y, corner_y + 5]}
            candidates_y = {chars[n, y] for n in [0, max_x, corner_x, corner_x + 5]}
            if "?" in candidates_x | candidates_y:
                continue
            candidates = candidates_x & candidates_y
            if len(candidates) == 1:
                ruin.append(candidates.pop())
        if len(ruin) == 16:
            total += ruin_power(ruin)

    return total


    unsolved = collections.deque((x * 6 + 1, y * 6 + 1) for x in range(width) for y in range(height))
    solved_blocks = set()
    solved_words = []

    def corner(idx: int) -> int:
        c_x = x - 1
        return c_x - (c_x % 6) + 1

    def candidates(x, y, corner_x, corner_y):
        candidates_x = {chars[x, n] for n in [0, max_y, corner_y, corner_y + 5]}
        candidates_y = {chars[n, y] for n in [0, max_x, corner_x, corner_x + 5]}
        return candidates_x & candidates_y

    def solve_block(corner_x, corner_y):
        positions = [(x, y) for y in range(corner_y, corner_y + 5) for x in range(corner_x + 1, corner_x + 5)]
        to_solve = set(positions)
        letters = {}
        used_x = collections.defaultdict(set)
        used_y = collections.defaultdict(set)
        for x, y in positions:
            options = candidates(x, y, corner_x, corner_y)
            if len(options) == 1 and (letter := options.pop()) != "?":
                to_solve.remove((x, y))
                letters[x, y] = letter
                used_x[x].add(letter)
        while to_solve:
            found_letter = False
            for x, y in list(to_solve):
                candidates_x = {chars[x, n] for n in [0, max_y, corner_y, corner_y + 5]}
                candidates_y = {chars[n, y] for n in [0, max_x, corner_x, corner_x + 5]}
                assert "?" in candidates_x or "?" in candidates_y

    no_progress = 0
    while unsolved:
        if all(neighbors(*block) & solved_blocks for block in unsolved):
            return sum(ruin_power(ruin) for ruin in solved_words)
        if no_progress > total_blocks:
            raise RuntimeError("Unable to make progress")
        block = unsolved.popleft()
        ruin, updates_chars = solve_block(*block)
        if ruin is None:
            unsolved.append(block)
            no_progress += 1
        else:
            chars.update(updates_chars)
            solved_blocks.add(block)
            solved_words.append(ruin)
            no_progress = 0




def ruin_power(ruin: str) -> int:
    return sum(idx * (string.ascii_uppercase.index(letter) + 1) for idx, letter in enumerate(ruin, 1))

def get_ruin(data: str) -> str:
    rows = []
    cols = []
    for row in (line for line in data.splitlines() if "." in line):
        rows.append(set(row))
    for col in (line for line in zip(*data.splitlines()) if "." in line):
        cols.append(set(col))
    for row in rows:
        row.remove(".")
    for col in cols:
        col.remove(".")
    out = []
    for y in range(4):
        for x in range(4):
            intersects = rows[y] & cols[x]
            assert len(intersects) == 1
            out.append(intersects.pop())
    return "".join(out)



TEST_DATA = [
    """\
**PCBS**
**RLNW**
BV....PT
CR....HZ
FL....JW
SG....MN
**FTZV**
**GMJH**""",
    """\
**XFZB**DCST**
**LWQK**GQJH**
?G....WL....DQ
BS....H?....CN
P?....KJ....TV
NM....Z?....SG
**NSHM**VKWZ**
**PJGV**XFNL**
WQ....?L....YS
FX....DJ....HV
?Y....WM....?J
TJ....YK....LP
**XRTK**BMSP**
**DWZN**GCJV**
"""
]
TESTS = [
    (1, TEST_DATA[0], "PTBVRCZHFLJWGMNS"),
    (2, TEST_DATA[0], 1851),
    (3, TEST_DATA[1], 3889),
]
