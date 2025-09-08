"""Aquaq Day N."""

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    data = [i if i in "1234567890abcdefgh" else "0" for i in data.lower()]
    while len(data) % 3:
        data.append("0")
    segment = len(data) // 3
    parts = [j for i in range(0, len(data), segment) for j in data[i:i + 2]]
    return "".join(parts)


TESTS = [
    (1, "kdb4life", "0d40fe"),
]
