"""The Bounty Hunter's Schedule

You are a bounty hunter.
You have a list of targets, each with a deadline deadlines[i] (the number of days from now the target must be caught by, starting from day 1) and a reward rewards[i].
You can catch at most one target per day, and catching a target takes exactly one day.
Your goal is to maximize the total reward you can earn.
Return the maximum possible total reward.

## Constraints:

1 ≤ n ≤ 500
deadlines[i] ≥ 1
rewards[i] ≥ 1
"""

import heapq

def maxBounty(deadlines, rewards):
    selected = []
    for deadline, reward in sorted(zip(deadlines, rewards)):
        heapq.heappush(selected, reward)
        if len(selected) > deadline:
            heapq.heappop(selected)
    return sum(selected)


assert maxBounty([2, 1, 2, 1], [10, 5, 20, 15]) == 35
assert maxBounty([1, 1, 1], [100, 200, 300]) == 300
assert maxBounty([3, 2, 1, 1], [10, 20, 30, 40]) == 70

assert maxBounty([], []) == 0
assert maxBounty([2, 2, 2], [100, 200, 300]) == 500
assert maxBounty([3, 3, 3], [100, 200, 300]) == 600
assert maxBounty([4, 4, 4], [100, 200, 300]) == 600

