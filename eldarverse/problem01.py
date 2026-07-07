"""Eldarverse Day N."""

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    lines = data.splitlines()
    return "\n".join(
        f"Case #{idx}: {100 - 5 * len(set(line.lower()))}"
        for idx, line in enumerate(lines[1:], 1)
    )


TESTS = [
    (1, "2\nAna\nKonstantine", "Case #1: 90\nCase #2: 60"),
]
