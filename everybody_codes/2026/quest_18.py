"""Everyone Codes Event 2026 Day N."""

import logging
from lib import helpers
from lib import parsers

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    data.sort()
    if part > 1:
        new_data = []
        for x, y, width in data:
            new_data.append((x, y))
            if width > 1:
                new_data.append((x + width - 1, y))
        data = new_data

    total = 0
    a, b = 0, len(data) - 1
    ml = 0
    mr = 0
    prior_height = 0
    while a <= b:
        # print(f"{a}: {data[a]};  {b}: {data[b]}")
        new_height = max(prior_height, min(data[a][1], data[b][1]))
        height = max(0, new_height - prior_height)
        prior_height = new_height
        width = data[b][0] - data[a][0] + 1
        if data[a][1] < data[b][1]:
            a += 1
        else:
            b -= 1
        # print(f"  Add {height=} * {width=} ==> {height * width}")
        total += height * width

    return total


# PARSER = parsers.parse_one_str
TEST_DATA = [
    """\
""",
    """\
""",
    """\
""",
    """\
""",
    """\
""",
]
TESTS = [
    # (1, TEST_DATA[0], None),
    # (2, TEST_DATA[1], None),
    # (3, TEST_DATA[2], None),
]

if __name__ == "__main__":
    helpers.run_solution(globals())
