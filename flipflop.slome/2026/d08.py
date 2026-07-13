"""FlipFlop Codes, Puzzle 8: The Amazing Digital Stoats."""

import functools
import collections
import logging
from lib import helpers, parsers

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""

    if part == 1:
        stoats = {"A": 1, "B": 1}
        rules = collections.defaultdict(list)
        for start, *end in data:
            rules[start].append(dict(collections.Counter(end)))
        # print(rules)
        for i in range(7):
            next_gen = collections.defaultdict(int)
            for group, count in stoats.items():
                for next_group, next_count in rules[group][0].items():
                    next_gen[next_group] += next_count * count
            stoats = next_gen
            # print(i, stoats, sum(stoats.values()))
        return sum(stoats.values())

    rules = collections.defaultdict(list)
    for a, b, *out in data:
        pair = tuple(sorted([a, b]))
        assert pair not in rules
        rules[pair] = out
    # print(rules)

    @functools.cache
    def offspring(a: str, b: str, generations: int) -> int:
        if generations == 0:
            return 0
        pair = tuple(sorted([a, b]))
        result = [a] + rules[pair] + [b]
        generations -= 1
        return len(rules[pair]) + sum(offspring(i, j, generations) for i, j in zip(result[:-1], result[1:]))

    return 2 + offspring("A", "B", 7 if part == 2 else 21)

        


# PARSER = parsers.parse_one_str
TEST_DATA = """\
A A C
A B C
A C B
B B A B A
B C B A
C C B B"""
TESTS = [
    (1, TEST_DATA, 4102),
    (2, TEST_DATA, 433),
    (3, TEST_DATA, 117302657),
]

if __name__ == "__main__":
    helpers.run_solution(globals())
