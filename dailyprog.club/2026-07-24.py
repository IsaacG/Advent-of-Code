"""Divisible Bounty

A merchant hides pouches of coins along a trade route.
Each pouch contains coins (could be a debt, represented by negative coins).
You want to find the longest contiguous stretch of the route where the total number of coins is exactly divisible by the number of guards (a fixed positive integer k).
Return the length of that longest stretch.
If there is no such stretch, return 0.
"""

def divisibleBounty(pouches, k):
    """Return the length of the longest stretch where the total is divisible by k."""
    return max(
        m - n
        for n in range(len(pouches))
        for m in range(n + 1, len(pouches) + 1)
        if sum(pouches[n:m]) % k == 0
    ) 

def optimized(pouches, k):
	"""Return the length of the longest stretch where the total is divisible by k."""
	num_pouches = len(pouches)
	for n in range(num_pouches, -1, -1):
		if any(
			sum(pouches[a:b + 1]) % k == 0
			for a in range(num_pouches - n + 1)
			for b in range(a, num_pouches)
		):
			return n
	return 0


assert divisibleBounty([2, 3, 5, 1, 4], 5) == 5
assert divisibleBounty([1, 2], 3) == 2
assert divisibleBounty([5], 5) == 1
