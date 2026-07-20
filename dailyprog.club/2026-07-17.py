def fairSplitPirates(coins):
    return canSplit(sorted(coins, reverse=True), 0)

def canSplit(coins, balance):
    if sum(coins) == balance:
        return True
    biggest, *rest = coins
    if len(rest) == 0:
        return biggest == balance
    if biggest > sum(rest) + balance:
        return False
    return canSplit(rest, abs(biggest + balance)) or canSplit(rest, abs(biggest - balance))

assert fairSplitPirates([1, 5, 11, 5]) == True
assert fairSplitPirates([1, 2, 3, 5]) == False
assert fairSplitPirates([2, 2]) == True
assert fairSplitPirates([1]) == False

