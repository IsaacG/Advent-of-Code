import collections
import functools


def solve(part: int, data: str) -> str:
    parents = {}
    fruits = set()
    # Parse and construct tree.
    for line in data.splitlines():
        src, dsts = line.split(":")
        for dst in dsts.split(","):
            if dst == "@":
                fruits.add(src)
            else:
                parents[dst] = src
    if part == 3:
        fruits.discard("ANT")

    @functools.cache
    def get_depth(node):
        if node == "RR":
            return 0
        return 1 + get_depth(parents[node])

    # Group by depth.
    fruit_depth = collections.defaultdict(set)
    for fruit in fruits:
        fruit_depth[get_depth(fruit)].add(fruit)
    # Find the fruit with a unique depth.
    want = next(f.copy().pop() for d, f in fruit_depth.items() if len(f) == 1)
    # Construct the path to the fruit.
    path = ["@", want]
    while want != "RR":
        want = parents[want]
        path.append(want)
    if part != 1:
        path = [p[0] for p in path]
    return "".join(reversed(path))


TEST_DATA = """\
RR:A,B,C
A:D,E
B:F,@
C:G,H
D:@
E:@
F:@
G:@
H:@"""
TESTS = [
    (1, TEST_DATA, "RRB@"),
]
