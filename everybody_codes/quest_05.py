import collections
import itertools


def solve(part: int, data: str) -> int:
    # Convert the input into columns.
    rows = [[int(i) for i in line.split()] for line in data.splitlines()]
    cols = [list(i) for i in zip(*rows)]

    # Tracking info.
    highest = 0
    counts = collections.defaultdict(int)
    seen = set()
    size = len(cols)

    for idx, (src, dst) in enumerate(itertools.cycle(zip(cols, cols[1:] + cols[:1]))):
        # Dance.
        clapper = src.pop(0)

        pos = (clapper - 1) % (len(dst) * 2)
        if pos < len(dst):
            dst.insert(pos, clapper)
        else:
            pos = 2 * len(dst) - pos
            dst.insert(pos, clapper)

        # Track the shout.
        shout = int("".join(str(col[0]) for col in cols))
        counts[shout] += 1
        highest = max(highest, shout)

        if part == 1 and idx + 1 == 10:
            return shout
        if part == 2 and counts[shout] == 2024:
            return (idx + 1) * shout
        if part == 3 and idx % size == 0:
            fp = tuple(tuple(col) for col in cols)
            if fp in seen:
                return highest
            seen.add(fp)


TEST_DATA = [
    """\
2 3 4 5
3 4 5 2
4 5 2 3
5 2 3 4""",
    """\
2 3 4 5
6 7 8 9""",
]
TESTS = [
    (1, TEST_DATA[0], 2323),
    (2, TEST_DATA[1], 50877075),
    (3, TEST_DATA[1], 6584),
]
