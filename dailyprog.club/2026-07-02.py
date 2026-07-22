"""Ancient Fresco

A conservator is restoring an ancient fresco painted on a grid of square tiles.
Some tiles still show pigment (represented as 1) while others are bare (0).
Pigment spreads orthogonally: if two pigmented tiles are directly above/below or left/right of each other, they are part of the same continuous painted area.
Write a function that, given a 2D array fresco, returns the total number of separate painted areas.
"""

def countFrescoPatches(fresco):
    # return the number of separate painted areas
    ungrouped = {
        (x, y)
        for y, row in enumerate(fresco)
        for x, i in enumerate(row)
        if i
    }
    groups = 0
    while ungrouped:
        seed = ungrouped.pop()
        seen = {seed}
        todo = [seed]
        while todo:
            x, y = todo.pop()
            for dx, dy in {(0, 1), (0, -1), (1, 0), (-1, 0)}:
                n = x + dx, y + dy
                if n not in ungrouped or n in seen:
                    continue
                seen.add(n)
                todo.append(n)
        groups += 1
        ungrouped -= seen
    return groups

assert countFrescoPatches([[1]]) == 1
assert countFrescoPatches([[0, 0], [0, 0]]) == 0
assert countFrescoPatches([[1, 0, 1]]) == 2
assert countFrescoPatches([[1, 1], [1, 1]]) == 1
