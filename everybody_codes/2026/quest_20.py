"""Everyone Codes Event 2026 Day N."""

import collections
import itertools
import logging
from lib import helpers
from lib import parsers

import re

RE = re.compile("([0-9A]+)([+-])([0-9A]+)(=)([0-9A]+)([+-])([0-9A]+)")

log = logging.info

SEGMENTS = {
        "0": 6,
        "1": 2,
        "2": 5,
        "3": 5,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 3,
        "8": 7,
        "9": 6,
        "+": 2,
        "-": 1,
        "=": 2,
        "A": 6,
}

def decimal_to_base(num, base):
    if num == 0:
        return "0"

    chars = "0123456789A"
    result = ""

    while num:
        num, mod = divmod(num, base)
        result = chars[mod] + result

    return result


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    
    def segments(line):
        parts = RE.match("".join(line).replace(" ", "")).groups()
        o = parts
        a = []
        for i in parts:
            if i not in "+-=":
                a.append(str(int(i, 10 if part == 1 else 11)))
            else:
                a.append(i)
        parts = a
        if eval("".join(str(i) for i in parts).replace("=", "==")):
            # print(o, sum(SEGMENTS[str(i)] for i in "".join(o)))
            return sum(SEGMENTS[str(i)] for i in "".join(o))
        return 0

    if part < 3:
        t = 0
        for line in data:
            t += segments(line)
        return decimal_to_base(t, 10 if part == 1 else 11)


    # Swap within one char
    SWAPS = {
        "2": "3",
        "5": "3",
        "3": "25",
        "0": "69A",
        "6": "9A0",
        "9": "A06",
        "A": "069",
    }
    # Add to a char. Paired with DROP.
    ADD = {
        "-": "+",
        "0": "8",
        "1": "7",
        "3": "9",
        "5": "69",
        "A": "8",
        "6": "8",
        "9": "8",
    }
    # Remove from a char. Paired with ADD.
    DROP = {
        "+": "-",
        "8": "0A69",
        "7": "1",
        "9": "35",
        "6": "5",
    }

    # Verify the above maps
    bysize = collections.defaultdict(set)
    for a, b in SEGMENTS.items():
        bysize[b].add(a)

    for a, bs in SWAPS.items():
        for b in bs:
            assert a in SWAPS[b]

    tdrop = collections.defaultdict(str)
    for a, bs in ADD.items():
        for b in bs:
            assert SEGMENTS[a] + 1 == SEGMENTS[b]
            assert a in DROP[b]
            tdrop[b] += a
    assert dict(tdrop) == DROP

    for a, bs in DROP.items():
        for b in bs:
            assert SEGMENTS[a] - 1 == SEGMENTS[b]
            assert a in ADD[b]

    # End verify


    def segments2(line):
        return segments(line)

    def oneswap(line):
        for idx, char in enumerate(line):
            for alt in SWAPS.get(char, ""):
                line[idx] = alt
                if (s := segments2(line)):
                    return s
            line[idx] = char
        return 0

    def w_swap(line):
        for a, b in itertools.permutations(range(len(line)), r=2):
            assert a != b
            char_a, char_b = line[a], line[b]
            if not (char_a in ADD and char_b in DROP):
                continue
            for alt_a in ADD[char_a]:
                line[a] = alt_a
                for alt_b in DROP[char_b]:
                    line[b] = alt_b
                    # print("".join(line))
                    if (s := segments2(line)):
                        # print("true")
                        return s
                line[b] = char_b
            line[a] = char_a
        return 0


    t = 0
    for line in data:
        line = list("".join(str(i) for i in line))
        og = "".join(line)
        if (s := segments2(line)):
            # print(og, "no change needed")
            t += s
        elif (s := oneswap(line)):
            # print(og, "swap in one char")
            t += s
        elif (s := w_swap(line)):
            # print(og, "swap cross char")
            t += s
        else:
            # print(og, "no solution")
            pass

        
    got = decimal_to_base(t, 11)
    if got in {"47239"}:
        return "INCORRECT"
    return got



PARSER = parsers.parse_one_str_per_line
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
    # (3, "1 + 1 = 5 + 7", 18),
]

if __name__ == "__main__":
    helpers.run_solution(globals())
