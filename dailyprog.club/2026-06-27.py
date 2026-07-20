"""Garden Plots

A gardener has a row of plots.
Each plot can be planted with a vegetable that yields a profit given as profits[i].
However, if two adjacent plots are both planted, the soil will be depleted and neither yields anything.
The gardener can choose to leave any plot empty.
Determine the maximum total profit the gardener can achieve.
"""

import functools

def gardenPlots(profits):
    # return the maximum profit without planting two adjacent plots
    return maxProfit(tuple(profits))

@functools.cache
def maxProfit(profits):
    if not profits:
        return 0
    p, *ps = profits
    return max(
        p + maxProfit(tuple(ps[1:])),
        maxProfit(tuple(ps[0:])),
    )

assert gardenPlots([1, 2, 3]) == 4
assert gardenPlots([10, 1, 1, 10]) == 20
assert gardenPlots([5]) == 5
