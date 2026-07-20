"""Find the missing number

You are handed an array of n distinct integers taken from the range 0 through n, so exactly one number from the full set is missing.
Return that missing number.
"""

def findMissingNumber(nums):
    for i, n in enumerate(sorted(nums)):
        if i != n:
            return i
    return len(nums)

assert findMissingNumber([3, 0, 1]) == 2
assert findMissingNumber([0, 1]) == 2
assert findMissingNumber([9, 6, 4, 2, 3, 5, 7, 0, 1]) == 8
