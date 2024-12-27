TESTS = [
    (1, "ABBAC", 5),
    (2, "AxBCDDCAxD", 28),
    (3, "xBxAAABCDxCC", 30),
]

def solve(part: int, data: str) -> int:
    costs = {"A": 0, "B": 1, "C": 3, "D": 5, "x": 0}
    total = 0
    for i in range(0, len(data), part):
        chunk = data[i:i + part]
        total += sum(costs[char] for char in chunk)
        group_size = sum(char != "x" for char in chunk)
        if group_size == 2:
            total += 2
        elif group_size == 3:
            total += 6
    return total
