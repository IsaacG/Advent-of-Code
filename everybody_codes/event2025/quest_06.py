"""Everyone Codes Day N."""

import collections
import math
import time


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    if part in [1, 2]:
        total = 0
        counts: dict[str, int] = collections.defaultdict(int)
        for i in data:
            if i.isupper():
                counts[i.lower()] += 1
            else:
                if i == "a" or part == 2:
                    total += counts[i]
        return total

    # Part three.
    # Number of repeated needed to get to 1000 characters.
    once = math.ceil(1000 / len(data))
    twice = once * 2
    repeats = 1000 - twice

    total = 0
    # Repeat the data enough to have a look behind and look ahead of 1000.
    # Compute the middle portion for one repetition then multiple it.
    d = data * (twice + 1)
    shift = len(data) * once
    for idx, m in enumerate(data):
        if m.islower():
            total += d[shift + idx - 1000:shift + idx + 1001].count(m.upper())
    total *= repeats

    # Handle the edges where there is not a full 1000 ahead or behind.
    d = data * twice
    for idx, m in enumerate(j for i in range(twice) for j in data):
        if m.islower():
            total += d[max(idx - 1000, 0):idx + 1001].count(m.upper())

    return total


TESTS = [
    (1, "ABabACacBCbca", 5),
    (2, "ABabACacBCbca", 11),
    (3, "AABCBABCABCabcabcABCCBAACBCa", 3442321),
]

if __name__ == "__main__":
    for _part, _data, expected in TESTS:
        assert solve(_part, (_data)) == expected
    print("Tests pass.")
    day = __file__.split("_", maxsplit=-1)[-1].split(".")[0]
    for _part in range(1, 4):
        with open(f"inputs/{day}.{_part}.txt", encoding="utf-8") as f:
            start = time.perf_counter_ns()
            got = solve(_part, (f.read()))
            end = time.perf_counter_ns()
            print(_part, got, (end - start) / 1_000_000_000)
