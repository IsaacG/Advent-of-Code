"""Everyone Codes Event 2026 Day 6."""

from lib import helpers
import collections


def solve(part: int, data: list[str]) -> int:
    """Solve the parts."""
    components = {}
    used_by = collections.defaultdict(set)
    for line in data:
        a, b = line.split(":")
        components[a] = b.split(",")
        for i in components[a]:
            used_by[i].add(a)

    if part == 1:
        todo = {"NULL"}
        used = set()
        seen = set()
        while todo:
            for component in components.get(todo.pop(), []):
                if component not in seen:
                    seen.add(component)
                    todo.add(component)
        return len(seen - {"NULL"})

    contains = {}
    for ingredient in {"NULL", "NULLv1", "NULLv2", "NULLv3"}:
        todo = {ingredient}
        seen = set()
        while todo:
            for component in used_by.get(todo.pop(), []):
                if component not in seen:
                    seen.add(component)
                    todo.add(component)
        contains[ingredient] = seen

    if part == 2:
        return len(contains["NULL"] - {"NULL"})

    return sum(
        v > 1 for v in collections.Counter(i for j in {"NULLv1", "NULLv2", "NULLv3"} for i in contains[j]).values()
    )


if __name__ == "__main__":
    helpers.run_solution(globals())
