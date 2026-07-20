"""Best single trade

You may buy one share on a single day and sell it on a later day.
Given the daily prices, return the maximum profit you can make, or 0 if no trade is worth making.
"""

def maxProfit(prices):
    max_profit = 0
    highest_sale = 0
    for price in reversed(prices):
        max_profit = max(max_profit, highest_sale - price)
        highest_sale = max(highest_sale, price)
    return max_profit

assert maxProfit([7, 1, 5, 3, 6, 4]) == 5
assert maxProfit([7, 6, 4, 3, 1]) == 0
assert maxProfit([1, 5]) == 4
