"""Codyssi Day N."""

import dataclasses
import functools


@dataclasses.dataclass(slots=True, order=True)
class Recipe:
    """Dataclass to hold recipe info."""
    quality: int
    cost: int
    materials: int


def solve(part: int, data: str, testing: bool) -> int:
    """Solve the parts."""
    # Parse the recipes. Store them in a list. We can reference them by index.
    lines = data.splitlines()
    recipes = []
    for line in lines:
        for p in ["| Quality :", ", Cost :", ", Unique Materials :"]:
            line = line.replace(p, "")
        _, _, quality, cost, materials = line.split()
        recipes.append(Recipe(int(quality), int(cost), int(materials)))

    # Sort, highest quality first.
    recipes.sort(reverse=True)

    @functools.cache
    def optimal_production(items: tuple[int, ...], budget: int) -> tuple[int, int]:
        """Return the optimal production for a given set of items and a given budget.

        Items are simply refered to by their recipe index.
        """
        # Base case. No items in the budget. Nothing to produce.
        if not items:
            return 0, 0
        # Select the first (highest quality) item. Compare the optimal production we can achieve assuming
        # (1) we do produce this item vs (2) we do not. In either case, we explore the optimal production
        # of the remaining items, removing this item from the list.
        one = recipes[items[0]]
        # Case with this one item being produced. Update budget and remaining options.
        budget_with = budget - one.cost
        rest_with = tuple(i for i in items[1:] if recipes[i].cost <= budget_with)
        q_with, m_with = optimal_production(rest_with, budget_with)
        # Add the quality and materials of this one item.
        q_with += one.quality
        m_with += one.materials
        # Case without this one item. Budget, quality, materials do not change.
        # Remaining options only remove one item.
        q_wout, m_wout = optimal_production(items[1:], budget)
        # Pick the higher quality result.
        if q_wout > q_with:
            return q_wout, m_wout
        if q_with > q_wout:
            return q_with, m_with
        # On a tie, take the lower materials.
        return q_with, min(m_with, m_wout)

    if part == 1:
        return sum(i.materials for i in recipes[:5])
    if part == 2:
        budget = 30
    elif testing:
        budget = 150
    else:
        budget = 300
    q, m = optimal_production(tuple(range(len(recipes))), budget)
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
