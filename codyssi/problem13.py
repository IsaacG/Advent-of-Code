"""Codyssi Day N."""

import collections
import re


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    lines = data.splitlines()
    balances = {}
    txns = []
    debts = collections.defaultdict(list)
    for line in lines:
        if m := re.fullmatch(r"(.+) HAS (\d+)", line):
            balances[m.group(1)] = int(m.group(2))
        elif m := re.fullmatch(r"FROM (.+) TO (.+) AMT (\d+)", line):
            txns.append([m.group(1), m.group(2), int(m.group(3))])

    def transfer(frm, to, amount):
        balances[frm] -= amount
        balances[to] += amount
        if part == 3 and to in debts:
            frm = to
            for debt in debts[frm]:
                to, amount = debt
                pay = min(balances[frm], amount)
                if pay:
                    debt[1] -= pay
                    transfer(frm, to, pay)

    for frm, to, amount in txns:
        o_amt = amount
        if part > 1 and amount > balances[frm]:
            debts[frm].append([to, amount - balances[frm]])
            amount = balances[frm]
        transfer(frm, to, amount)
    return sum(sorted(balances.values(), reverse=True)[:3])


TEST_DATA = """\
Alpha HAS 131
Bravo HAS 804
Charlie HAS 348
Delta HAS 187
Echo HAS 649
Foxtrot HAS 739

FROM Echo TO Foxtrot AMT 328
FROM Charlie TO Bravo AMT 150
FROM Charlie TO Delta AMT 255
FROM Alpha TO Delta AMT 431
FROM Foxtrot TO Alpha AMT 230
FROM Echo TO Foxtrot AMT 359
FROM Echo TO Alpha AMT 269
FROM Delta TO Foxtrot AMT 430
FROM Bravo TO Echo AMT 455
FROM Charlie TO Delta AMT 302
"""
TESTS = [
    (1, TEST_DATA, 2870),
    (2, TEST_DATA, 2542),
    (3, TEST_DATA, 2511),
]
