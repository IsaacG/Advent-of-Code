"""Chisel Foundation

You are a stonemason preparing a foundation for a building.
Each stone block has a measured height given in the array blocks (all positive integers).
You can reduce any block's height by chiseling; reducing a block by one unit costs one unit of work.
Your team has a total work budget of budget units.
You must choose a target maximum height H and chisel down every block taller than H until no block is taller than H.
Blocks shorter than H are left alone.
Find the smallest possible maximum height H you can achieve without exceeding your work budget.
If you have enough budget to reduce all blocks down to height 0, the answer is 0.
"""

import collections

def chiselFoundation(blocks, budget):
    """Return the smallest possible max height after applying budget."""
    heights = sorted(collections.Counter(blocks).items())
    while True:
        highest, count = heights.pop()
        if budget < count or highest == 0:
            return highest
        next_highest, next_count = heights.pop() if heights else (0, 0)
        reduction = min((highest - next_highest) * count, budget) // count
        new_height = highest - reduction
        if new_height > next_highest:
            return new_height
        heights.append((next_highest, count + next_count))
        budget -= reduction * count

assert chiselFoundation([5, 3, 7], 4) == 4
assert chiselFoundation([10], 0) == 10
assert chiselFoundation([2, 2, 2], 1) == 2
assert chiselFoundation([1, 100], 50) == 50
