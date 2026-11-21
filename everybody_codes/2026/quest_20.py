"""Everyone Codes Event 2026 Day 20."""

import collections
import itertools
import re
from lib import helpers
from lib import parsers

# Used to split a line into components.
RE = re.compile("([0-9A]+)([+-])([0-9A]+)(=)([0-9A]+)([+-])([0-9A]+)")

# Number of segments per character.
SEGMENTS = {
        "0": 6, "1": 2, "2": 5, "3": 5,
        "4": 4, "5": 5, "6": 6, "7": 3,
        "8": 7, "9": 6, "+": 2, "-": 1,
        "=": 2, "A": 6,
}

# Transformations within one char with a segment swap
SWAPS = {
    "2": "3",
    "5": "3",
    "3": "25",
    "0": "69A",
    "6": "9A0",
    "9": "A06",
    "A": "069",
}
# Transformations of a char by dropping one segment. Inverted to build ADD.
DROP = {
    "+": "-",
    "8": "0A69",
    "7": "1",
    "9": "35",
    "6": "5",
}

ADD = collections.defaultdict(str)
for a, bs in DROP.items():
    for b in bs:
        ADD[b] += a
ADD = dict(ADD)


def base11(num: int) -> str:
    """Convert to base11, inverse of `int(number, 11)`."""
    if num == 0:
        return "0"

    chars = "0123456789A"
    result = ""

    while num:
        num, mod = divmod(num, 11)
        result = chars[mod] + result

    return result


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    data = [list(line) for line in data]
    
    def segments(line: list[str]) -> int:
        """Return the number of segments in an equation if it is valid, else 0."""
        # Tidy up the input. Strip spaces, list to str.
        line = "".join(line).replace(" ", "")
        # Convert to parts.
        parts = RE.match(line).groups()
        # Convert base 11 to base 10.
        if part > 1:
            parts = [
                i if i in "+=-" else str(int(i, 11))
                for i in parts
            ]
        # Evaluate and sum up segments.
        if eval("".join(str(i) for i in parts).replace("=", "==")):
            return sum(SEGMENTS[str(i)] for i in line)
        return 0

    def one_char_change(line: list[str]) -> int:
        """Return segment count if the equation can be made true by changing one character."""
        for idx, char in enumerate(line):
            for alt in SWAPS.get(char, ""):
                line[idx] = alt
                if (s := segments(line)):
                    return s
            line[idx] = char
        return 0

    def multi_char_change(line: list[str]) -> int:
        """Return segment count if the equation can be made true by changing two characters."""
        for a, b in itertools.permutations(range(len(line)), r=2):
            char_a, char_b = line[a], line[b]
            if not (char_a in ADD and char_b in DROP):
                continue
            for alt_a in ADD[char_a]:
                line[a] = alt_a
                for alt_b in DROP[char_b]:
                    line[b] = alt_b
                    if (s := segments(line)):
                        return s
                line[b] = char_b
            line[a] = char_a
        return 0

    if part < 3:
        total = sum(segments(line) for line in data)
    else:
        total = sum(
            segments(line) or one_char_change(line) or multi_char_change(line)
            for line in data
        )

    if part > 1:
        total = base11(total)
    return total


PARSER = parsers.parse_one_str_per_line


if __name__ == "__main__":
    helpers.run_solution(globals())
