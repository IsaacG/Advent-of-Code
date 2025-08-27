"""Everyone Codes Day N."""

import collections
import itertools


def solve(part: int, data: str) -> int:
    """Solve the fluffbolt game."""
    balloons = list(data)

    # Count how many bolts it takes to shoot through a line of balloons.
    if part == 1:
        balloons.reverse()
        for count, bolt in enumerate(itertools.cycle("RGB"), 1):
            while balloons and balloons.pop() == bolt:
                pass
            if not balloons:
                return count

    # Count how many bolts it takes to burst a circle of balloons.
    # We care about two points on the circle, on opposite ends.
    # We can represent that as two lists (or deques) where the important balloons are at the start of of either list.
    # We just need to make sure we shift balloons from the second half to the first half to keep things balanced.
    # If we pop two balloons from the first half, that makes the halves unbalanced and we need to shift one balloon.
    # We need to track even/odd to know if the bolt can hit a second balloon or not.
    count = 100 if part == 2 else 100000
    h1 = collections.deque(balloons * (count // 2))
    h2 = collections.deque(balloons * (count // 2))
    even = True
    for count, bolt in enumerate(itertools.cycle("RGB"), 1):
        # Colors match, even count: pop a second balloon.
        if bolt == h1.popleft() and even:
            h2.popleft()
        else:
            # Pop only one balloon? Toggle even and possibly rebalance.
            if even:
                h1.append(h2.popleft())
            even = not even
        if not h1:
            return count + len(h2)
    raise RuntimeError("Not solved")


TESTS = [
    (1, "GRBGGGBBBRRRRRRRR", 7),
    (2, "BBRGGRRGBBRGGBRGBBRRBRRRBGGRRRBGBGG", 2955),
]
