"""The Overbooked Chef

Chef Marco has a list of cooking tasks, each with a start time and an end time (in minutes past midnight).
He wants to schedule as many non-overlapping tasks as possible to maximize his output.
Two tasks overlap if their time intervals intersect: that is, if one starts before or exactly when the other ends (inclusive).
He will consider tasks in order by their start time (ascending), breaking ties by end time (ascending).
For each task in that order, if it starts after the last scheduled task ends (strictly later, i.e., start > lastEnd), he schedules it (status 'keep').
Otherwise, he drops it (status 'drop').
No merging occurs in this algorithm.

Your task: Given two arrays starts and ends of equal length (1–8 intervals), simulate Chef Marco's greedy algorithm step by step.
Return an object with three fields:

* answer: the number of tasks scheduled (kept).
* order: an array of the original indices of tasks in the order they are considered.
* status: an array of the same length, each element being either "keep" or "drop", indicating the decision for the corresponding task in the order array.
"""

def chefSchedule(starts, ends):
    """Return {"answer": ..., "order": [...], "status": [...]}."""
    intervals = sorted((b, c, a) for a, (b, c) in enumerate(zip(starts, ends)))
    last_end = -1
    order, status = [], []
    kept = 0
    for start, end, idx in intervals:
        if start > last_end:
            last_end = end
            status.append("keep")
            kept += 1
        else:
            status.append("drop")
        order.append(idx)
    return {"answer": kept, "order": order, "status": status}

assert chefSchedule([1, 2, 3], [3, 4, 5]) == {"answer": 1, "order": [0, 1, 2], "status": ["keep", "drop", "drop"]}
assert chefSchedule([1, 3, 5], [2, 4, 6]) == {"answer": 3, "order": [0, 1, 2], "status": ["keep", "keep", "keep"]}
assert chefSchedule([1, 2, 4, 6, 7], [3, 5, 5, 8, 9]) == {"answer": 3, "order": [0, 1, 2, 3, 4], "status": ["keep", "drop", "keep", "keep", "drop"]}
