"""Boat Parade Spots

The town's annual boat parade has multiple time slots when boats can pass the viewing stand.
Each slot is a half-open interval [start, end) (boats occupy the spot from start up to but not including end).
The parade marshal wants to maximize the number of boats that can be scheduled without any two overlapping (i.e., their intervals must be disjoint).
Given an array intervals where each interval is a pair [start, end), return the maximum number of boats that can be scheduled.
"""

def maxBoats(intervals):
    """Return the maximum number of non-overlapping intervals."""
    if not intervals:
        return 0
    (s, e), *rest = intervals
    filtered = [[a, b] for a, b in rest if b <= s or a >= e]
    withBoat = 1 + maxBoats(filtered)
    if len(filtered) == len(rest):
        return withBoat
    return max(withBoat, maxBoats(rest))

"""
// Javascript

function maxBoats(intervals) {
  if (intervals.length === 0) {
    return 0
  }
  const [first, ...rest] = intervals
  const [start, end] = first
  const filtered = rest.filter(other => other[0] >= end || other[1] <= start)
  const withFirst = 1 + maxBoats(filtered)
  if (filtered.length === rest.length) {
    return withFirst
  }
  const withoutFirst = maxBoats(rest)
  return Math.max(withFirst, withoutFirst)
}
"""


assert maxBoats([[1,3],[3,5]]) == 2
assert maxBoats([[1,3],[2,4]]) == 1
assert maxBoats([]) == 0
