"""Hidden Stash

A pirate has logged his daily steps (positive forward, negative backward).
He believes he revisited a spot along the trail, meaning some contiguous set of days had a total displacement of exactly zero.
Given an array steps of integers, return true if there exists a non-empty contiguous subarray whose sum is zero, otherwise false.
"""

def hiddenStash(steps):
    return any(
        sum(steps[i:j]) == 0
        for i in range(len(steps))
        for j in range(i + 1, len(steps) + 1)
    )

assert hiddenStash([3, -2, -1, 5]) == True
assert hiddenStash([1, 2, 3]) == False
assert hiddenStash([0]) == True
