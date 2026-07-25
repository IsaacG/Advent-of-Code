"""VIP Seats

You're organizing a charity concert.
There are K VIP seats, and you need to fill them with donors whose total donation equals exactly T.
Each donor i is willing to donate donations[i] dollars (a positive integer), but you can only invite a donor to a VIP seat once.
Return true if there exists a selection of exactly K donors whose total donation is exactly T, otherwise false.
"""

import collections

def vipSeats(donations, K, T):
    """Return True if exactly K donors sum to T, else False."""
    if T == 0 or K == 0:
        return T == K
    todo = collections.deque([(0, K, T)])
    l = len(donations)
    seen = {(0, K, T)}
    while todo:
        start_idx, k, t = todo.popleft()
        if k == 1:
            if t in donations[start_idx:]:
                return True
            continue
        k -= 1
        for i in range(start_idx, l - k):
            d = donations[i]
            if d > t or (i, k, t - d) in seen:
                continue
            seen.add((i + 1, k, t - d))
            todo.append((i + 1, k, t - d))
    return False

    # return any(sum(i) == T for i in itertools.combinations(donations, r=K))


# assert vipSeats([1, 2, 3, 4, 5, 6], 2, 5) == True
assert vipSeats([1, 2, 3, 4, 5, 6], 3, 10) == True
assert vipSeats([1, 2, 3], 2, 6) == False
assert vipSeats([5], 1, 5) == True
assert vipSeats([1, 2], 0, 0) == True
assert vipSeats([10, 20], 3, 30) == False
