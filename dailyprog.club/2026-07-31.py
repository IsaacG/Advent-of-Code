"""Concert Setlist

You are organizing a concert and have a playlist of songs, each with a unique duration in minutes.
The playlist is sorted in ascending order by duration.
You need to select exactly two songs whose combined duration equals the target slot length.
Your job is to simulate a two-pointer search over the sorted durations.

Starting with a pointer at the beginning (left) and one at the end (right), repeat the following until the pointers meet:

* If the sum of the durations at left and right equals the target, you've found a pair!
  Record the pointer positions and stop (the answer is the left index).
* If the sum is less than the target, move the left pointer one step to the right.
* If the sum is greater than the target, move the right pointer one step to the left.

Return an object with three fields:

* "answer": the index of the left pointer when a valid pair is found, or -1 if no pair exists.
* "lo": an array of the left pointer values at each step (including the starting position).
* "hi": an array of the right pointer values at each step (parallel to lo).
"""

def concertSearch(durations, target):
    """Return {"answer": ..., "lo": [...], "hi": [...]}."""
    lo, hi = 0, len(durations) - 1
    los, his = [], []
    while lo < hi:
        los.append(lo)
        his.append(hi)
        got = durations[lo] + durations[hi]
        if got < target:
            lo += 1
        elif got > target:
            hi -= 1
        else:
            break
    return {"answer": lo if lo < hi else -1, "lo": los, "hi": his}

assert concertSearch([3, 5, 7, 9], 12) == {"answer": 0, "lo": [0], "hi": [3]}
assert concertSearch([1, 2, 3, 4, 5, 6], 10) == {"answer": 3, "lo": [0, 1, 2, 3], "hi": [5, 5, 5, 5]}
assert concertSearch([1, 2, 3], 6) == {"answer": -1, "lo": [0, 1], "hi": [2, 2]}
