"""Max window sum

You're analyzing a stream of sensor readings.
Given an array of integers readings and a window size k, return the maximum sum of any k consecutive readings.
If k is larger than the number of readings, return null, since there's no valid window.
"""

def maxWindowSum(readings, k):
    if k > len(readings):
        return None

    winSum = sum(readings[:k])
    best = winSum
    for i in range(len(readings) - k):
        winSum -= readings[i]
        winSum += readings[i + k]
        best = max(best, winSum)
    return best

assert maxWindowSum([1, 2, 3, 4, 5], 2) == 9
assert maxWindowSum([-1, -2, -3, -4], 2) == -3
assert maxWindowSum([5, 1, 9, 3], 1) == 9

