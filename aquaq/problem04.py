"""Aquaq Day N."""
import math


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    num = int(data)
    return sum(
        i
        for i in range(1, num)
        if math.gcd(i, num) == 1
    )


TESTS = [(1, "15", 60)]
