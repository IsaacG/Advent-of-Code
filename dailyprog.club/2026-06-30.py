"""Wine Tasting

You have a collection of wine bottles on a shelf.
Each bottle has a 'richness' value (a positive integer).
You want to select a consecutive sequence of bottles to serve at a tasting, but the total richness (the product of all values in the sequence) must be strictly less than a given limit.
What is the length of the longest possible sequence you can choose? Return the maximum length, or 0 if no sequence qualifies.
"""

import math

def longestSequence(nums, limit):
    # return the longest length of a contiguous subarray with product < limit
    best = 0
    for i in range(len(nums)):
        run = nums[i]
        size = 1
        for m in nums[i + 1:]:
            if run * m >= limit:
                break
            run *= m
            size += 1
        if best < size and run <= limit:
            best = size
    return best

assert longestSequence([1, 2, 3], 6) == 2
assert longestSequence([], 10) == 0
assert longestSequence([5], 10) == 1
assert longestSequence([10, 20], 200) == 1
