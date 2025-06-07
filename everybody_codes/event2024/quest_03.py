"""Everyone Codes Day Three."""

def solve(part: int, data: str) -> int:
    """Solve puzzle."""
    pos = {
        complex(x, y)
        for y, line in enumerate(data.splitlines())
        for x, char in enumerate(line)
        if char == "#"
    }
    remove = 0
    offsets = [1j ** i for i in range(4)]
    if part == 3:
        offsets.extend(complex(1, 1) * 1j ** i for i in range(4))
    while pos:
        remove += len(pos)
        pos = {i for i in pos if all(i + offset in pos for offset in offsets)}
    return remove


TEST_DATA = """\
..........
..###.##..
...####...
..######..
..######..
...####...
.........."""
TESTS = [
    (1, TEST_DATA, 35),
    # (2, TEST_DATA, None),
    (3, TEST_DATA, 29),
]
