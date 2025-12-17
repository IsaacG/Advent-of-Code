"""FlipFlop Codes: Day 3: Bush Salesman."""
import collections
from lib import parsers


def solve(part: int, data: list[str]) -> int | str:
    """Solve the parts."""
    if part == 1:
        return ",".join(str(i) for i in collections.Counter(tuple(i) for i in data).most_common(1)[0][0])
    if part == 2:
        return sum(line[1] == max(line) and len(set(line)) == 3 for line in data)

    total = 0
    for line in data:
        if len(set(line)) != 3:
            total += 10
        else:
            total += [5, 2, 4][line.index(max(line))]
    return total


PARSER = parsers.parse_ints
TEST_DATA = [
    """\
10,20,30
20,10,30
30,20,10
10,50,10
50,10,50
10,20,30""",
]
TESTS = [
    (1, TEST_DATA[0], "10,20,30"),
    (2, TEST_DATA[0], 0),
]
