"""Everyone Codes Day N."""

from lib import helpers
from lib import parsers


def solve(part: int, data: list[list[int]]) -> int:
    """Solve the parts."""
    total_nums = 1 + sum((pair[-1] - pair[0] + 1) for pair in data)
    offset = int("2025" * part) % total_nums

    ranges = (
        [range(1, 2)]
        + [range(pair[0], pair[-1] + 1, +1) for pair in data[0::2][::+1]]
        + [range(pair[-1], pair[0] - 1, -1) for pair in data[1::2][::-1]]
    )
    for r in ranges:
        size = len(r)
        if offset < size:
            return r[offset]
        offset -= size
    raise RuntimeError("Not solved.")


PARSER = parsers.BaseParseReFindall(r'\d+', lambda x: [int(i) for i in x], one_line=False)
TESTS = [
    (1, "72\n58\n47\n61\n67", 67),
    (2, "10-15\n12-13\n20-21\n19-23\n30-37", 30),
]

if __name__ == "__main__":
    helpers.run_solution(globals())
