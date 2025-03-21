"""Codyssi Day N."""

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    if part == 1:
        count = 0
        for pair in data.split():
            a, b = (int(i) for i in pair.split("-"))
            count += b - a + 1
        return count

    if part == 2:
        count = 0
        for line in data.splitlines():
            a, b, c, d = (int(j) for i in line.split() for j in i.split("-"))
            if a <= c <= b or c <= b <= d or a <= d <= b or c <= a <= d:
                count += max(b, d) - min(a, c) + 1
            else:
                count += b - a + d - c + 2
        return count

    if part == 3:
        count = 0
        lines = data.splitlines()
        for la, lb in zip(lines, lines[1:]):
            boxes: set[int] = set()
            for pair in f"{la} {lb}".split():
                a, b = (int(i) for i in pair.split("-"))
                boxes.update(range(a, b + 1))
            count = max(count, len(boxes))
        return count

    raise RuntimeError("Not reachable")


TEST_DATA = """\
8-9 9-10
7-8 8-10
9-10 5-10
3-10 9-10
4-8 7-9
9-10 2-7"""
TESTS = [
    (1, TEST_DATA, 43),
    (2, TEST_DATA, 35),
    (3, TEST_DATA, 9),
]
