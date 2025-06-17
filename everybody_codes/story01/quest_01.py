"""Everyone Codes Day N."""

import re


def eni(n: int, exp: int, mod: int, part: int) -> int:
    """Return an ENI result."""
    if part != 3:
        remainders = []
        if part == 1:
            # Part 1: brute force each remainder.
            score = 1
            steps = exp
        else:
            # Part 2: higher values; skip to the end using pow() and compute 5 remainders.
            score = pow(n, exp - 5, mod)
            steps = 5

        for step in range(steps):
            score = score * n % mod
            remainders.append(score)
        return int("".join(str(i) for i in reversed(remainders)))

    # Part 3: solve for each remainder with cycle finding.
    seen = set()
    scores = []
    score = 1
    for step in range(exp):
        score = score * n % mod

        # Stop on cycle detection.
        if score in seen:
            break

        scores.append(score)
        seen.add(score)

    # Find how many steps since the score was last seen, ie cycle length.
    prior_step = scores.index(score)
    stride = step - prior_step
    # How many times does the cycle repeat and how many steps after the last cycle?
    div, rmod = divmod(exp - step, stride)
    modsum = lambda x: sum(i % mod for i in x)
    # Score: (steps prior to cycling) + (cycle scores repeated div times) + (steps after the last cycle).
    return modsum(scores) + div * modsum(scores[prior_step:]) + modsum(scores[prior_step:prior_step + rmod])


def verify_eni(a: int, b: int, c: int, x: int, y: int, z: int, m: int, part: int) -> int:
    """Return the sum of three ENIs."""
    return eni(a, x, m, part) + eni(b, y, m, part) + eni(c, z, m, part) 


def solve(part: int, data: str) -> int:
    """Solve the line which yields the highest ENI sum."""
    return max(
        verify_eni(*[int(i) for i in re.findall(r"[0-9]+", line)], part=part)
        for line in data.splitlines()
    )


TEST_DATA = [
    """\
A=4 B=4 C=6 X=3 Y=4 Z=5 M=11
A=8 B=4 C=7 X=8 Y=4 Z=6 M=12
A=2 B=8 C=6 X=2 Y=4 Z=5 M=13
A=5 B=9 C=6 X=8 Y=6 Z=8 M=14
A=5 B=9 C=7 X=6 Y=6 Z=8 M=15
A=8 B=8 C=8 X=6 Y=9 Z=6 M=16""",
    """\
A=4 B=4 C=6 X=3 Y=14 Z=15 M=11
A=8 B=4 C=7 X=8 Y=14 Z=16 M=12
A=2 B=8 C=6 X=2 Y=14 Z=15 M=13
A=5 B=9 C=6 X=8 Y=16 Z=18 M=14
A=5 B=9 C=7 X=6 Y=16 Z=18 M=15
A=8 B=8 C=8 X=6 Y=19 Z=16 M=16""",
    """\
A=3657 B=3583 C=9716 X=903056852 Y=9283895500 Z=85920867478 M=188
A=6061 B=4425 C=5082 X=731145782 Y=1550090416 Z=87586428967 M=107
A=7818 B=5395 C=9975 X=122388873 Y=4093041057 Z=58606045432 M=102
A=7681 B=9603 C=5681 X=716116871 Y=6421884967 Z=66298999264 M=196
A=7334 B=9016 C=8524 X=297284338 Y=1565962337 Z=86750102612 M=145""",
    """\
A=4 B=4 C=6 X=3000 Y=14000 Z=15000 M=110
A=8 B=4 C=7 X=8000 Y=14000 Z=16000 M=120
A=2 B=8 C=6 X=2000 Y=14000 Z=15000 M=130
A=5 B=9 C=6 X=8000 Y=16000 Z=18000 M=140
A=5 B=9 C=7 X=6000 Y=16000 Z=18000 M=150
A=8 B=8 C=8 X=6000 Y=19000 Z=16000 M=160""",
    """\
A=3657 B=3583 C=9716 X=903056852 Y=9283895500 Z=85920867478 M=188
A=6061 B=4425 C=5082 X=731145782 Y=1550090416 Z=87586428967 M=107
A=7818 B=5395 C=9975 X=122388873 Y=4093041057 Z=58606045432 M=102
A=7681 B=9603 C=5681 X=716116871 Y=6421884967 Z=66298999264 M=196
A=7334 B=9016 C=8524 X=297284338 Y=1565962337 Z=86750102612 M=145""",
]
TESTS = [
    (1, TEST_DATA[0], 11611972920),
    (2, TEST_DATA[1], 11051340),
    (2, TEST_DATA[2], 1507702060886),
    (3, TEST_DATA[3], 3279640),
    (3, TEST_DATA[4], 7276515438396),
]
