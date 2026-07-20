import collections

def cycles(start, links):
    seen = set()
    todo = [start]
    while todo:
        a = todo.pop()
        if a not in links:
            continue
        for b in links[a]:
            if b == start:
                return True
            if b in seen:
                continue
            seen.add(b)
            todo.append(b)

    return False
    

def firstWarpCycle(gates):
    # Return the 0-based index of the first gate that creates a cycle, or -1
    links = collections.defaultdict(list)
    for i, (a, b) in enumerate(gates):
        links[a].append(b)
        if any(cycles(start, links) for start in links):
            return i
    return -1


assert 2 == firstWarpCycle([[0, 1], [1, 2], [2, 0], [3, 4]])
assert -1 == firstWarpCycle([[0, 1], [2, 3], [4, 5]])
assert -1 == firstWarpCycle([[0, 1]])

