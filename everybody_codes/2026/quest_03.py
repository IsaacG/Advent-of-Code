"""Everyone Codes Event 2026 Day 3."""

import itertools

from lib import helpers


def compute(iso: int, number: int) -> int:
    return sum(
        int(b) * int(a) ** idx
        for idx, (a, b) in enumerate(zip(itertools.cycle(str(abs(iso))[::-1]), str(number)[::-1]))
    )


def solve(part: int, data: str, testing) -> int:
    """Solve the parts."""
    if part < 3:
        return sum(compute(iso, number) for iso, number in data)

    total = 0
    for _, iso, number in data:
        value = compute(iso, number)
        if not any(compute(iso, i) == value for i in range(number)):
            total += value
                
    return total


if __name__ == "__main__":
    helpers.run_solution(globals())
