import itertools
import pathlib

DAY = 1
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


want_raw = next((line.split() for line in pathlib.Path(f"solutions/2024.txt").read_text().splitlines() if line.startswith(f"{DAY:02} ")), None)
if want_raw:
    want = [int(i) for i in want_raw[1:]]

got = []
for part in range(1, 4):
    data_path = pathlib.Path(f"inputs/{DAY:02}.{part}.txt")
    if not data_path.exists():
        continue
    data = data_path.read_text().rstrip()
    for test_part, test_data, test_want in TESTS:
        if test_part == part:
            assert solve(test_part, test_data) == test_want
    got.append(solve(part, data))

if want_raw:
    assert want == got, f"{want=}, {got=}"
print(got)
