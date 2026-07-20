"""Triple Bet

A gambler picks three stocks from a portfolio whose recent returns are given as an array returns.
The gambler's total return is the product of the returns of the three chosen stocks.
The returns can be positive or negative integers.
Find the maximum possible product your client can achieve by picking exactly three distinct stocks.
The order of picks doesn't matter.

Solved in 3/5
"""

import itertools
import math

def maxTripleProduct(returns):
    # TODO: return maximum product of any three distinct elements
    returns.sort()
    return max(math.prod(returns[-3:]), math.prod(returns[:2]) * returns[-1])

    # Too slow, take 1
    return max(math.prod(i) for i in itertools.combinations(set(returns), r=3))

    # Too slow, take 2
    candidates = set(returns[:2] + returns[-3:])
    return max(math.prod(i) for i in itertools.combinations(candidates, r=3))



assert maxTripleProduct([1, 2, 3, 4]) == 24
assert maxTripleProduct([-1, 2, 3, 4]) == 24
assert maxTripleProduct([-5, -4, -3]) == -60
