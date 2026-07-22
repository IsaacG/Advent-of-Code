"""Envious Neighbors

On a street lined with houses, each house has an integer height.
Homeowners feel envious of the first house to their right that is strictly taller.
For each house, compute how many houses lie between them and their object of envy (so zero if the immediate neighbor is taller).
If there is no taller house to the right, output 0.
Given the array heights, return an array of the same length where each entry is the envy distance for that house.
"""

def enviousNeighbors(heights):
    # return a list of envy distances
    return [
        next(
            (
                j - i - 1
                for j in range(i + 1, len(heights))
                if heights[j] > heights[i]
            ), 0
        ) for i in range(len(heights))
    ]

assert enviousNeighbors([4, 3, 2, 5, 1]) == [2, 1, 0, 0, 0]
assert enviousNeighbors([1, 2, 3]) == [0, 0, 0]
assert enviousNeighbors([3, 2, 1]) == [0, 0, 0]
assert enviousNeighbors([1]) == [0]
