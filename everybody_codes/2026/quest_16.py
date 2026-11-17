"""Everyone Codes Event 2026 Day N."""

import collections
import io
import itertools
import logging
import platform

try:
    from lib import helpers
    from lib import parsers
except ModuleNotFoundError as e:
    if platform.python_implementation() != "PyPy":
        raise

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    # print(data)
    # data = "R123R456R7R"
    tabs = list(data)
    n = len(data)
    if part == 2:
        # tabs = tabs[:50]  # 612
        tabs = tabs * 10
    if part == 3:
        tabs = tabs * 100


    def show(m, s, a, b):
        return
        print(m)
        print(s)
        print(" " * a + "^" + " " * (b - a - 1) + "^")
        print()

    if True:
        count = 0
        while tabs:
            # print(set(tabs))
            color = tabs[0]
            post = io.StringIO()
            frnt = True
            a, b = 0, len(tabs) - 1
            # show("Start", tabs, a, b)
            while b > a and tabs[b] != color:
                post.write(tabs[b])
                b -= 1
            # show("Shift end for " + color, tabs, a, b)
            while a < b:
                # print(b - a)
                if frnt:
                    while a < len(tabs) and tabs[a] == color:
                        a += 1
                else:
                    while b > a and tabs[b] == color:
                        b -= 1
                # show(f"init shift {frnt=}", tabs, a, b)
                if a >= b:
                    break
                # print(f"Flips: {b - a + 1} from blocks {a // n}, {b // n}")
                if part == 1:
                    count += 1
                else:
                    count += b - a + 1
                # print(f"flip {a}-{b} == {b - a + 1}")
                if frnt:
                    while a < b and tabs[a] != color:
                        post.write(tabs[a])
                        a += 1
                else:
                    while b > a and tabs[b] != color:
                        post.write(tabs[b])
                        b -= 1
                frnt = not frnt
                # show(f"Moved to the end: {post.getvalue()}", tabs, a, b)
            tabs = "".join(reversed(post.getvalue()))
            # print("tabs", tabs)
        return count

    """
R123R456R7R
['R', '1', '2', '3', '4', '5', '6', '7']
RR7R654R321 10
RRR456R7321 16
RRRR6547321 20

123 7 456
"""


TEST_DATA = [
    """RRGGBBGRRGGBBG"""
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
    # (1, TEST_DATA[0], 3),
    # (2, TEST_DATA[1], None),
    # (3, TEST_DATA[2], None),
]

if __name__ == "__main__":
    helpers.run_solution(globals())
