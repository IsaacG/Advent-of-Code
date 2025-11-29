"""Everyone Codes Day N."""


def counter(conversions: dict[str, list[str]], start: str, steps: int) -> int:
    """Return the number of termines after some steps."""
    counts = {start: 1}
    for _ in range(steps):
        next_counts = {src: 0 for src in conversions}
        for src, num in counts.items():
            for dst in conversions[src]:
                next_counts[dst] += num
        counts = next_counts
    return sum(next_counts.values())


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    conversions = {}
    for line in data.splitlines():
        src, dst = line.split(":")
        conversions[src] = dst.split(",")

    if part == 1:
        return counter(conversions, "A", 4)
    if part == 2:
        return counter(conversions, "Z", 10)

    counts = [counter(conversions, start, 20) for start in conversions]
    return max(counts) - min(counts)


TESTS = [
    (1, "A:B,C\nB:C,A\nC:A", 8),
    (3, "A:B,C\nB:C,A,A\nC:A", 268815),
]
