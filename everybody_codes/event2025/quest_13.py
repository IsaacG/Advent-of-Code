"""Everyone Codes Day N."""

import collections
import logging
import time
from lib import helpers
from lib import parsers

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    if part == 1:
        nums = [d[0] for d in data]
        q = collections.deque()
        q.append(1)
        for idx, n in enumerate(nums):
            if idx % 2 == 0:
                q.append(n)
            else:
                q.appendleft(n)
        pos = (len(nums)) // 2
        q = list(q)
        nums = q[pos:] + q[:pos]
        print(nums)
        return nums[2025 % len(nums)]

    if part == 2:
        q = collections.deque()
        q.append(1)
        for idx, line in enumerate(data):
            a, b = line
            b = abs(b)
            if a > b:
                a, b = b, c
            if idx % 2 == 0:
                q.extend(range(a, b + 1))
            else:
                q.extendleft(range(a, b + 1))
        q = list(q)
        pos = q.index(1)
        nums = q[pos:] + q[:pos]
        # print( ",".join(str(i) for i in nums))
        # print("1,10,11,12,13,14,15,20,21,30,31,32,33,34,35,36,37,23,22,21,20,19,13,12")
        # assert ",".join(str(i) for i in nums) == "1,10,11,12,13,14,15,20,21,30,31,32,33,34,35,36,37,23,22,21,20,19,13,12"
        got = nums[(20252025 if part == 2 else 202520252025) % len(nums)]
        assert got != 9070
        return got

    nums = [[abs(i) for i in line] for line in data]
    total_nums = 1
    for a, b in nums:
        total_nums += b - a + 1
    offset = 202520252025 % total_nums
    assert offset < total_nums
    distance = 1
    for a, b in nums[::2]:
        nd = distance + (b - a) + 1
        if nd > offset:
            print(a, b, offset - distance)
        distance = nd
    for a, b in reversed(nums[1::2]):
        nd = distance + (b - a) + 1
        if nd > offset:
            return b - (offset - distance)
        distance = nd
    return 0

    


PARSER = parsers.parse_ints
TEST_DATA = [
    """\
72
58
47
61
67""",
    """\
10-15
12-13
20-21
19-23
30-37""",
]
TESTS = [
    (1, TEST_DATA[0], 67),
    (2, TEST_DATA[1], 30),
    # (3, TEST_DATA[2], None),
]

if __name__ == "__main__":
    for _part, _data, expected in TESTS:
        assert solve(_part, PARSER.parse(_data)) == expected
    print("Tests pass.")
    day = int(__file__.split("_", maxsplit=-1)[-1].split(".")[0])
    for _part in range(1, 4):
        with open(f"inputs/{day:02}.{_part}.txt", encoding="utf-8") as f:
            _input = PARSER.parse(f.read())  # type: list[list[int]]
            start = time.perf_counter_ns()
            got = solve(_part, _input)
            end = time.perf_counter_ns()
            print(f"{day:02}.{_part} {got:15} {helpers.format_ns(end - start):8}")
