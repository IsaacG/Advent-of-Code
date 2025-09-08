"""Aquaq Day N."""

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    items = [int(i) for i in data.split()]
    while True:
        for i in items:
            if items.count(i) > 1:
                first = items.index(i)
                last = list(reversed(items)).index(i) + 1
                items[first:-last] = []
                break
        else:
            return sum(items)


TESTS = [
    (1, "1 4 3 2 4 7 2 6 3 6", 20),
]
