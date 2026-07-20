"""
In a sealed-bid auction the prize goes to whoever placed the second-highest distinct bid.
Given the list of bids, return that amount, or null if there aren't two different bid values.
"""

def secondHighestBid(bids):
    s = sorted(set(bids))
    if len(s) < 2:
        return None
    return s[-2]

assert secondHighestBid([2, 1, 3, 2]) == 2
assert secondHighestBid([5, 5, 5]) == None
assert secondHighestBid([10, 7]) == 7

