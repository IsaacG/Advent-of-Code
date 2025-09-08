"""Aquaq Day N."""

LETTERS = ["abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz", " "]


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    out = []
    for line in data.splitlines():
        button, repeat = [int(i) for i in line.split()]
        letters = LETTERS[button - 2]
        out.append(letters[(repeat - 1) % len(letters)] if button else " ")
    return "".join(out)


TESTS = [
    (1, "7 3", "r"),
]
