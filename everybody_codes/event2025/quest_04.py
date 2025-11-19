"""Everyone Codes Day N."""
import math
from lib import helpers
from lib import parsers


def solve(part: int, data: list[list[int]]) -> int:
    """Solve the parts."""
    ratio = math.prod(a[-1] / b[0] for a, b in zip(data, data[1:]))
    return [int(ratio * 2025), math.ceil(10000000000000 / ratio), int(ratio * 100)][part - 1]


PARSER = parsers.parse_ints
TESTS = [
    (1, "128\n64\n32\n16\n8", 32400),
    (1, """102\n75\n50\n35\n13""", 15888),
    (2, "128\n64\n32\n16\n8", 625000000000),
    (2, """102\n75\n50\n35\n13""", 1274509803922),
    (3, "5\n5|10\n10|20\n5", 400),
    (3, "5\n7|21\n18|36\n27|27\n10|50\n10|50\n11", 6818),
]

if __name__ == "__main__":
    helpers.run_solution(globals())
