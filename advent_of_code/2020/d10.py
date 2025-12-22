#!/usr/bin/env python
"Day 10. Power adapters."""

import collections
import functools


def solve(data: list[int], part: int) -> int:
    """Count paths."""
    return (part1 if part == 1 else part2)(data)


def part1(data: list[int]) -> int:
    """Count the 1-steps and 3-steps."""
    # Sort the plugs.
    nums = sorted(data)
    # Add the source and dest, 0 and max+3.
    nums.insert(0, 0)
    nums.append(max(nums) + 3)
    # Compute the size of each step.
    diffs = [nums[i + 1] - nums[i] for i in range(len(nums) - 1)]
    # Count and multiply.
    counts = collections.Counter(diffs)
    return counts[1] * counts[3]


def part2(data: list[int]) -> int:
    """Count all possible paths from 0 to dest."""
    nums = [0] + sorted(data) + [max(data) + 3]

    @functools.cache
    def possible_paths_from(i):
        """Compute all possible paths from node i to the end.

        Paths from N-1 to N = 1.
        Paths from M to N = sum(
            all paths from v to N
            for all valid next-nodes v
        ).
        Valid next-nodes are any nodes within 3 of M.

        Dynamic programming ahead. Cache result.
        """
        if i == len(nums) - 1:
            return 1
        valid = [
            j for j in range(i + 1, min(i + 4, len(nums)))
            if nums[j] - nums[i] <= 3
        ]
        return sum(possible_paths_from(i) for i in valid)

    return possible_paths_from(0)


SAMPLE = [
    "16\n10\n15\n5\n1\n11\n7\n19\n6\n12\n4",
    "28\n33\n18\n42\n31\n14\n46\n20\n48\n47\n24\n23\n49\n45\n19\n"
    + "38\n39\n11\n1\n32\n25\n35\n8\n17\n7\n9\n4\n2\n34\n10\n3"
]
TESTS = [(1, SAMPLE[0], 35), (1, SAMPLE[1], 220), (2, SAMPLE[1], 19208)]
