"""Raid Teams

A guild has n members numbered 0 to n-1.
Some members have personal disputes and refuse to raid together.
You're given a list disputes where each element is a pair [a, b] representing a dispute between members a and b.
The guild must be split into exactly two raid teams.
Determine if it's possible to assign members to teams such that no team contains a disputing pair.
Return true if possible, false otherwise.
"""

import collections

def canSplit(n, disputes):
    """Return True if possible, else False"""
    d = collections.defaultdict(set)
    for a, b in disputes:
        d[a].add(b)
        d[b].add(a)
    unassigned = set(range(n))
    teams = [set(), set()]
    while unassigned:
        a = unassigned.pop()
        todo = {a}
        cur = 0
        while todo:
            disputes = {disputed for person in todo for disputed in d[person]}
            if teams[cur] & disputes or todo & disputes:
                return False
            teams[cur] |= todo
            unassigned -= todo
            cur = 1 - cur
            todo = disputes & unassigned

    return True


assert canSplit(4, [[0, 1], [1, 2], [2, 3], [3, 0]]) == True
assert canSplit(3, [[0, 1], [1, 2], [2, 0]]) == False
assert canSplit(1, []) == True
