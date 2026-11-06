"""Everyone Codes Event 2026 Day 9."""

import collections
from lib import helpers


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    result = 0
    for _, growth, limit in data:
        branches = {1: 1}  # size, number of occurances
        seconds = 1
        forks = 0

        if part == 1:
            tree_size = lambda: forks + sum(size * num for size, num in branches.items())
        else:
            tree_size = lambda: forks + 1

        while tree_size() < limit:
            # For large growths, skip to the next fork.
            steps = 1 if part == 1 else growth - max(branches) 
            seconds += steps

            next_branches = collections.defaultdict(int)
            for size, occurances in branches.items():
                size += steps
                if size < growth:
                    next_branches[size] += occurances
                else:
                    next_branches[1] += occurances
                    next_branches[size // 2] += 2 * occurances
                    forks += occurances

            branches = next_branches

        result += seconds

    return result


if __name__ == "__main__":
    helpers.run_solution(globals())
