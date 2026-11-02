"""Everyone Codes Event 2026 Day N."""

import logging
from lib import helpers
from lib import parsers

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    components = {}
    for line in data:
        a, b = line.split(":")
        components[a] = b.split(",")

    def uses(target):
        todo = {target}
        used = set()
        seen = set()
        while todo:
            component = todo.pop()
            used.add(component)
            if component in components:
                for i in components[component]:
                    if i not in seen:
                        seen.add(i)
                        todo.add(i)
        return used

    if part == 1:
        return len(uses("NULL") - {"NULL"})
    if part == 2:
        return sum("NULL" in uses(i) for i in components if i != "NULL")

    return sum(
        sum(n in uses(i) for n in ["NULLv1", "NULLv2", "NULLv3"]) > 1
        for i in components if i != "NULL"
    )


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
