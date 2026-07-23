"""Clean Sweep

A robot vacuum has to reach its charging station before it runs out of power.
The room is a rectangular grid of tiles, where '#' are walls, '.
' are cleanable open tiles, 'S' marks the vacuum's start position, and 'E' marks the charging station.
The vacuum can move to an adjacent tile (up, down, left, right) as long as it is not a wall.
Return the minimum number of steps to reach the charging station, or -1 if it cannot be reached.
"""

import collections

def cleanSweep(grid):
    """Return the minimum steps to reach E, or -1."""
    spaces = set()
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == "S":
                todo = collections.deque([(0, x, y)])
            if char == "E":
                end = (x, y)
            if char in "E.":
                spaces.add((x, y))

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    seen = set()
    while todo:
        steps, x, y = todo.popleft()
        if (x, y) == end:
            return steps
        steps += 1
        for dx, dy in directions:
            neighbor = (x + dx, y + dy)
            if neighbor in spaces and neighbor not in seen:
                seen.add(neighbor)
                todo.append((steps, *neighbor))
    return -1


assert cleanSweep(["S.", ".E"]) == 2
assert cleanSweep(["S#E"]) == -1
assert cleanSweep(["S..", "...", "..E"]) == 4

