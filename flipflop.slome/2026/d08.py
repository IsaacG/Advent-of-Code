"""FlipFlop Codes, Puzzle 8: The Amazing Digital Stoats."""

import functools
import collections
from lib import helpers, parsers


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    if part == 1:
        stoats = {"A": 1, "B": 1}
        # Rules: each stoat is replaced by some other set.
        rules = collections.defaultdict(list)
        for start, *end in data:
            rules[start].append(dict(collections.Counter(end)))
        for i in range(7):
            next_gen = collections.defaultdict(int)
            for group, count in stoats.items():
                for next_group, next_count in rules[group][0].items():
                    next_gen[next_group] += next_count * count
            stoats = next_gen
        return sum(stoats.values())

    # Rules: a pair of stoat create additional stoat(s)
    rules = collections.defaultdict(list)
    for a, b, *out in data:
        pair = tuple(sorted([a, b]))
        assert pair not in rules
        rules[pair] = out

    @functools.cache
    def offspring(a: str, b: str, generations: int) -> int:
        """Compute the number of resulting offspring from a pair over n generations."""
        if generations == 0:
            return 0
        pair = tuple(sorted([a, b]))
        result = [a] + rules[pair] + [b]
        generations -= 1
        # Return the number of offspring: immediate + future generations.
        return len(rules[pair]) + sum(offspring(i, j, generations) for i, j in zip(result[:-1], result[1:]))

    return 2 + offspring("A", "B", 7 if part == 2 else 21)

        
WANT = [4102, 433, 117302657]
TEST_DATA = """\
A A C
A B C
A C B
B B A B A
B C B A
C C B B"""
TESTS = [(i, TEST_DATA, want) for i, want in enumerate(WANT, start=1)]

if __name__ == "__main__":
    helpers.run_solution(globals())
