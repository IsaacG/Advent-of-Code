"""Perfect Pairing

In a cooking contest, each contestant must create a dish with a total flavor score exactly matching the judge's magic number.
Contestants work in pairs, combining their flavor scores.
Given an array of flavor scores scores (each an integer) and the magic number target, write a function to count how many distinct pairs of scores can be combined to match the magic number.
A 'distinct pair' means a pair of indices (i, j) with i < j and scores[i] + scores[j] == target.
Return the count.
"""

def countPairs(scores, target):
    # return the number of distinct pairs i<j with scores[i]+scores[j]==target
    return sum(
        scores[i] + scores[j] == target
        for i in range(len(scores) - 1)
        for j in range(i + 1, len(scores))
    )

assert countPairs([1, 2, 3, 4, 5], 5) == 2
assert countPairs([1, 2, 3], 10) == 0
assert countPairs([3, 3, 3], 6) == 3

