"""Everyone Codes Day N."""
import collections
import string


def solve(part: int, data: str) -> int | str:
    """Solve the parts."""
    lines = data.splitlines()
    if part == 1:
        return solve_one_simple_block(data)
    if part == 2:
        blocks = [
            "\n".join(lines[line_idx][x:x + 8] for line_idx in range(y, y + 8))
            for x in range(0, len(lines[0]), 9)
            for y in range(0, len(lines), 9)
        ]
        return sum(ruin_power(solve_one_simple_block(block)) for block in blocks)

    # == Part Three ==

    # Shared char map which gets updated when "?" chars are solved.
    char_map = {(x, y): letter for y, line in enumerate(lines) for x, letter in enumerate(line)}

    def solve_one(corner_x: int, corner_y: int) -> int | None:
        """Attempt to solve one block."""
        # Rely on dict ordering to extract the chars in order by setting the keys in order.
        solved: dict[tuple[int, int], None | str] = {
            (x, y): None
            for y in range(corner_y + 2, corner_y + 6)
            for x in range(corner_x + 2, corner_x + 6)
        }
        used = {"?"}
        char_updates = {}

        # Solve for ruin symbols until progress is no longer happening.
        progress = True
        while progress:
            progress = False
            for (x, y), letter in solved.items():
                if letter is not None:
                    continue
                candidates_x = {(x, corner_y + n): char_map[x, corner_y + n] for n in [0, 1, 6, 7]}
                candidates_y = {(corner_x + n, y): char_map[corner_x + n, y] for n in [0, 1, 6, 7]}
                questions = [(x, y) for (x, y), char in (candidates_x | candidates_y).items() if char == "?"]
                candidates = (set(candidates_x.values()) & set(candidates_y.values())) - used
                if not candidates and not questions:
                    return None
                update_questions = False
                if not candidates and len(questions) == 1:
                    update_questions = True
                    if "?" in candidates_x.values():
                        candidates = set(candidates_y.values()) - used
                    else:
                        candidates = set(candidates_x.values()) - used
                if len(candidates) == 1:
                    letter = candidates.pop()
                    solved[x, y] = letter
                    used.add(letter)
                    progress = True
                    # Track ? that needs updating to a symbol.
                    if update_questions:
                        char_updates[*questions[0]] = letter

        if all(solved.values()):
            # Update the char map when we complete a block.
            char_map.update(char_updates)
            return ruin_power(i for i in solved.values() if i is not None)
        return None

    # Track all unsolved blocks.
    width = (len(lines[0]) - 2) // 6
    height = (len(lines) - 2) // 6
    todo = collections.deque((x * 6, y * 6) for x in range(width) for y in range(height))

    total = 0
    # Iterate through unsolved blocks until we've tried them all without solving any of them.
    misses = 0
    while misses < len(todo):
        if (power := solve_one(*todo[0])) is not None:
            todo.popleft()
            total += power
            misses = 0
        else:
            todo.rotate()
            misses += 1
    return total


def ruin_power(ruin: collections.abc.Iterable[str]) -> int:
    """Return the power of a ruin."""
    return sum(idx * (string.ascii_uppercase.index(letter) + 1) for idx, letter in enumerate(ruin, 1))


def solve_one_simple_block(data: str) -> str:
    """Return the ruin word for a block without any "?"."""
    rows = [set(row) - {"."} for row in (line for line in data.splitlines() if "." in line)]
    cols = [set(col) - {"."} for col in (line for line in zip(*data.splitlines()) if "." in line)]
    return "".join((rows[y] & cols[x]).pop() for y in range(4) for x in range(4))


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
NOTES = """\
I had a real hard time solving this because I initially thought that, for every 6x6 block,
you include an additional border made of the *very* first and *very* last row and column vs the adjacent blocks.
I had a hard time understanding why I couldn't get a solution to work.
"""
