"""Boat Parade Spots

The town's annual boat parade has multiple time slots when boats can pass the viewing stand.
Each slot is a half-open interval [start, end) (boats occupy the spot from start up to but not including end).
The parade marshal wants to maximize the number of boats that can be scheduled without any two overlapping (i.e., their intervals must be disjoint).
Given an array intervals where each interval is a pair [start, end), return the maximum number of boats that can be scheduled.
"""

import collections
import itertools

def canDo(intervals):
    starts = collections.deque(sorted(s for s, e in intervals))
    ends = collections.deque(sorted(e for s, e in intervals))
    most = 0
    cur = 0
    while starts:
        t = starts[0]
        while ends and ends[0] <= t:
            cur -= 1
            ends.popleft()
        while starts and starts[0] == t:
            cur += 1
            if cur > 1:
                return False
            starts.popleft()
    return True


def maxBoats(intervals):
    """Return the maximum number of non-overlapping intervals."""
    for i in range(len(intervals), -1, -1):
        if any(canDo(subset) for subset in itertools.combinations(intervals, r=i)):
            return i
    return 0


assert maxBoats([[1,3],[3,5]]) == 2
assert maxBoats([[1,3],[2,4]]) == 1
assert maxBoats([]) == 0
