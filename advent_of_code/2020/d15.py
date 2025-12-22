#!/usr/bin/env python
"""Day 15. Van Eck sequence. https://www.youtube.com/watch?v=etMJxB-igrc - Numberphile."""


def solve(data: list[int], part: int) -> int:
    """Solve Van Eck's n'th digit.

    1st pass: store the last two timestamps. 30s.
    2nd pass: store the last timestamp in a map. 15s.
    3rd pass: store the last timestamp in a list. 8.5s.
    """
    end = 2020 if part == 1 else 30000000
    time_said = [0] * end
    for i, j in enumerate(data[:-1]):
        time_said[j] = i + 1
    last_spoken = data[-1]

    for counter in range(len(data), end):
        if not time_said[last_spoken]:
            say = 0
        else:
            say = counter - time_said[last_spoken]
        time_said[last_spoken] = counter
        last_spoken = say
    return last_spoken


PARSER = lambda s: [int(i) for i in s.split(',')]
TESTS = [
    (1, '0,3,6', 436),
    (1, '1,3,2', 1),
    (1, '2,1,3', 10),
]
