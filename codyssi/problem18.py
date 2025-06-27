"""Codyssi Day N."""

import functools
import logging

log = logging.info

def solve(part: int, data: str, testing: bool) -> int:
    """Solve the parts."""
    lines = data.splitlines()
    items = []
    byname = {}
    for line in lines:
        for p in ["| Quality :", ", Cost :", ", Unique Materials :"]:
            line = line.replace(p, "")
        num, name, quality, cost, materials = line.split()
        items.append((int(quality), int(cost), name, int(materials)))
        byname[name] = (int(cost), int(quality), int(materials))

    items.sort(reverse=True)

    @functools.cache
    def optimal_production(items, budget):
        available = sorted((i for i in items if byname[i][0] <= budget), key=lambda i: byname[i][0])
        if not available:
            return 0, 0
        one, *rest = available
        f_rest = frozenset(rest)
        q_with, m_with = optimal_production(f_rest, budget - byname[one][0])
        q_with += byname[one][1]
        m_with += byname[one][2]
        q_wout, m_wout = optimal_production(f_rest, budget)
        if q_wout > q_with:
            return q_wout, m_wout
        if q_with > q_wout:
            return q_with, m_with
        return q_with, min(m_with, m_wout)

    if part == 1:
        return sum(i[-1] for i in items[:5])
    if part == 2:
        budget = 30
    elif testing:
        budget = 150
    else:
        budget = 300
    q, m = optimal_production(frozenset(byname), budget)
    return q * m


TEST_DATA = """\
1 ETdhCGi | Quality : 36, Cost : 25, Unique Materials : 7
2 GWgcpkv | Quality : 38, Cost : 17, Unique Materials : 25
3 ODVdJYM | Quality : 1, Cost : 1, Unique Materials : 26
4 wTdbhEr | Quality : 23, Cost : 10, Unique Materials : 18
5 hoOYtHQ | Quality : 25, Cost : 15, Unique Materials : 27
6 jxRouXI | Quality : 31, Cost : 17, Unique Materials : 7
7 dOXpCyA | Quality : 23, Cost : 2, Unique Materials : 28
8 LtCtwHO | Quality : 37, Cost : 26, Unique Materials : 29
9 DLxTAif | Quality : 32, Cost : 24, Unique Materials : 1
10 XCUJAZF | Quality : 22, Cost : 25, Unique Materials : 29
11 cwoqgJA | Quality : 38, Cost : 28, Unique Materials : 7
12 ROPdFSh | Quality : 41, Cost : 29, Unique Materials : 15
13 iYypXES | Quality : 37, Cost : 12, Unique Materials : 15
14 srwmKYA | Quality : 48, Cost : 25, Unique Materials : 14
15 xRbzjOM | Quality : 36, Cost : 20, Unique Materials : 21"""
TESTS = [
    (1, TEST_DATA, 90),
    (2, TEST_DATA, 8256),
    (3, TEST_DATA, 59388),
]
