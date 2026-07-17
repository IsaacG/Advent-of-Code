"""FlipFlop Codes: N."""

import more_itertools
import itertools
from lib import helpers, parsers

NUMS = [str(i) for i in range(5)]
RNUMS = NUMS[::-1]


def build_pattern(direction):
    if not direction:
        return [[""] * 5]
    d, *rest = direction
    patterns = build_pattern(rest)
    if d == 1:
        return [[a + b for a, b in zip(NUMS, p)] for p in patterns]
    if d == -1:
        return [[a + b for a, b in zip(RNUMS, p)] for p in patterns]
    if d == 0:
        return [[a + b for b in p] for p in patterns for a in NUMS]


def compute_patterns(n: int) -> list[set[int]]:
    patterns = []
    for direction in itertools.product([0, 1, -1], repeat=n):
        if 1 not in direction:
            continue
        if next(d for d in direction if d != 0) == -1:
            continue
        patterns.extend(build_pattern(direction))

    return [{int(a, 5) for a in p} for p in patterns]


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    ball_lines, card_lines = data
    balls = itertools.chain(*ball_lines)
    dimensions = part + 1

    cards = list(more_itertools.chunked(itertools.chain(*card_lines), 5**dimensions))
    patterns = compute_patterns(dimensions)
    print(f"{dimensions=}")

    got = [set() for card in cards]
    i = 0
    for ball in balls:
        i += 1
        bingos = 0

        for hit, card in zip(got, cards):
            if ball in card:
                hit.add(card.index(ball))
            bingos += sum(pattern.issubset(hit) for pattern in patterns)
                
        if bingos >= 5:
            return ball


WANT = [49, 63]
TEST_DATA = """\
62 121 64 51 86 85 36 31 8 113 71 72 75 101 115 44 52 78 26 80 116 98 79 17 77
110 91 10 9 55 74 107 67 93 54 81 25 58 82 56 5 89 32 14 119 48 35 109 47 21
6 69 40 92 68 18 105 66 41 90 22 30 63 57 15 28 125 76 49 65 123 20 16 99 24
108 96 53 87 60 38 73 59 94 83 100 33 111 46 4 106 124 27 104 84 88 42 1 118 12
70 37 39 112 19 7 97 11 114 95 3 120 50 2 61 117 122 102 13 45 103 29 34 23 43

82 39 88 103 71 76 108 109 104 34 49 58 85 107 121 105 67 18 77 118 30 117 26 29 55
6 43 23 96 100 2 47 11 37 24 4 73 120 81 60 112 106 12 92 57 1 54 16 40 31
13 17 3 111 78 56 115 102 124 33 8 122 75 61 25 89 64 20 119 46 113 87 116 44 53
66 38 94 91 36 93 5 45 32 62 42 69 63 28 14 72 86 74 79 9 50 84 80 35 41
10 97 21 83 70 48 90 7 125 15 52 22 51 101 99 19 68 110 114 123 27 65 95 98 59
"""
TESTS = [(i, TEST_DATA, want) for i, want in enumerate(WANT, start=1)]


if __name__ == "__main__":
    helpers.run_solution(globals())
