"""Festival Staging

A festival organizer has a list of performer schedules: each performer needs a stage from their start time starts[i] to end time ends[i] (end time is non-inclusive).
A stage can be used by only one performer at a time.
Determine the minimum number of stages required to accommodate all performances without any overlap.
"""

def minStages(starts, ends):
    # return the minimum number of stages needed
    starts.sort(reverse=True)
    ends.sort(reverse=True)

    active = 0
    most = 0
    time = 0
    while starts:
        cur = starts[-1]
        while ends and ends[-1] <= cur:
            active -= 1
            ends.pop()
        while starts and starts[-1] <= cur:
            active += 1
            starts.pop()
        most = max(most, active)
    return most

assert minStages([0, 0], [1, 1]) == 2
assert minStages([0], [1]) == 1
assert minStages([0, 1], [1, 2]) == 1
assert minStages([0, 1], [5, 2]) == 2
assert minStages([], []) == 0

