"""FlipFlop Codes: N."""

import more_itertools
import itertools
import logging
from lib import helpers, parsers

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    if part == 1:
        return solvep1(data)
    if part == 2:
        return solvep2(data)
    if part == 3:
        return solvep3(data)

def solvep1(data: str) -> int:
    patterns = [set(range(i, i + 5)) for i in [0, 5, 10, 15, 20]]
    patterns += [set(range(i, i + 25, 5)) for i in range(5)]
    patterns += [set(range(0, 26, 6)), set(range(4, 24, 4))]
    calls, cards = data
    got = [set() for card in cards]
    i = 0
    for group in calls:
        for call in group:
            bingos = 0
            i += 1
            for hit, card in zip(got, cards):
                if call in card:
                    hit.add(card.index(call))
                for pattern in patterns:
                    if pattern.issubset(hit):
                        bingos += 1
                    
            if bingos >= 5:
                print(i, call)
                return call

def solvep2(data: str) -> int:
    pattern_x = [set(range(i, i + 5, 1)) for i in range(0, 25*5, 5)]     # x
    pattern_y = [set(range(i, i + 25, 5)) for c in range(5) for i in range(c*25, c*25+5)]   # y
    pattern_z = [set(range(i, i + 125, 25)) for i in range(25)]   # z
    patterns = pattern_x + pattern_y + pattern_z
    assert len(pattern_x) == len(pattern_y) == len(pattern_z) == 25
    assert len(patterns) == 3 * 5 ** 2

    diag = []
    for c in range(5):
        tl = c * 25
        patterns.append(set(range(tl, tl + 26, 6)))
        patterns.append(set(range(tl + 4, tl + 24, 4)))
    for x in range(5):
        patterns.append(set(range(x, 125, 30)))
        patterns.append(set(range(20+x, 120, 20)))
    for y in range(5):
        patterns.append(set(range(5*y, 125, 26)))
        patterns.append(set(range(5*y+4, 121, 24)))
    assert len(patterns) == 3 * 5**2 + 3 * 2 * 5

    patterns.append(set(range(0, 125, 31)))
    patterns.append(set(range(4, 125, 25+5-1)))
    patterns.append(set(range(20, 125, 25-5+1)))
    patterns.append(set(range(24, 110, 25-5-1)))
    assert len(patterns) == 3 * 25 + 3 * 2 * 5 + 2 * 2
    print(len(patterns))

    # print(max(len(p) for p in patterns))
    # print(min(len(p) for p in patterns))
    assert all(len(p) == 5 for p in patterns)

    calls, cards = data
    got = set()
    i = 0

    all_cards = []
    for c in cards:
        all_cards.extend(c)
    cards = list(more_itertools.chunked(all_cards, 125))
    assert all(len(c) == 125 for c in cards)
    # assert len(all_cards) == 5

    print(f"{len(cards)=}")

    got = [set() for card in cards]
    i = 0
    for group in calls:
        for call in group:
            bingos = 0
            i += 1
            for hit, card in zip(got, cards):
                if call in card:
                    hit.add(card.index(call))
                for pattern in patterns:
                    if pattern.issubset(hit):
                        bingos += 1
                    
            if bingos >= 5:
                return call

def solvep3(data: str) -> int:
    pattern_x = [set(range(s + i, s + i + 5, 1)) for i in range(0, 25*5, 5) for s in range(0, 625, 125)]     # x
    pattern_y = [set(range(s + i, s + i + 25, 5)) for c in range(5) for i in range(c*25, c*25+5) for s in range(0, 625, 125)]   # y
    pattern_z = [set(range(s + i, s + i + 125, 25)) for i in range(25) for s in range(0, 625, 125)]   # z
    pattern_w = [set(range(i, i + 625, 125)) for i in range(125)]   # w
    assert len(pattern_x) == len(pattern_y) == len(pattern_z) == len(pattern_w) == 125
    patterns = pattern_x + pattern_y + pattern_z + pattern_w
    assert len(patterns) == 4 * 5 ** 3

    diag = []
    for s in range(0, 625, 125):
        for c in range(5):
            patterns.append(set(range(s + c * 25, s + c * 25 + 26, 6)))
            patterns.append(set(range(s + c * 25 + 4, s + c * 25 + 24, 4)))
        for c in range(5):
            patterns.append(set(range(s + c, s + 125, 30)))
            patterns.append(set(range(s + 20+c, s + 120, 20)))
        for c in range(5):
            patterns.append(set(range(s + 5*c, s + 125, 26)))
            patterns.append(set(range(s + 5*c+4, s + 121, 24)))
        patterns.append(set(range(s + 0, s + 125, 31)))
        patterns.append(set(range(s + 4, s + 125, 25+5-1)))
        patterns.append(set(range(s + 20, s + 125, 25-5+1)))
        patterns.append(set(range(s + 24, s + 110, 25-5-1)))
    assert len(patterns) == 4 * 5**3 + 4 * 3 * 5, f"{len(patterns)} != {4 * 5**3 + 4 * 3 * 2* 5}"
    # 8 diags
    patterns.append(set(range(  0, 625, 125+25+5+1)))
    patterns.append(set(range(  4, 625, 125+25+5-1)))
    patterns.append(set(range( 20, 625, 125+25-5+1)))
    patterns.append(set(range( 24, 610, 125+25-5-1)))
    patterns.append(set(range(100, 625, 125-25+5+1)))
    patterns.append(set(range(104, 620, 125-25+5-1)))
    patterns.append(set(range(120, 600, 125-25-5+1)))
    patterns.append(set(range(124, 589, 125-25-5-1)))
    assert len(patterns) == 888, len(patterns)

    print(max(len(p) for p in patterns))
    print(min(len(p) for p in patterns))
    assert all(len(p) == 5 for p in patterns)

    calls, cards = data
    got = set()
    i = 0

    all_cards = []
    for c in cards:
        all_cards.extend(c)
    cards = list(more_itertools.chunked(all_cards, 625))
    assert all(len(c) == 625 for c in cards)
    # assert len(all_cards) == 5

    print(f"{len(cards)=}")

    got = [set() for card in cards]
    i = 0
    for group in calls:
        for call in group:
            bingos = 0
            i += 1
            for hit, card in zip(got, cards):
                if call in card:
                    hit.add(card.index(call))
                for pattern in patterns:
                    if pattern.issubset(hit):
                        bingos += 1
                    
            if bingos >= 5:
                return call



WANT = [49, 63]
# PARSER = parsers.parse_one_str
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
# TESTS = [
#     (1, TEST_DATA[0], None),
#     (2, TEST_DATA[1], None),
#     (3, TEST_DATA[2], None),
# ]

if __name__ == "__main__":
    helpers.run_solution(globals())
