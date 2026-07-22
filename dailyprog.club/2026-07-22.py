"""Photon Path

## The Grid
You are calibrating a photon beam in an n by n grid of mirrors.
Each cell is either empty or contains a mirror.
There are two kinds of mirrors: '/' (slash) and '\\' (backslash).
The grid is given as a flat array of integers, row-major: 0 means empty, 1 means a / mirror, 2 means a \ mirror.

## Starting State
The beam starts at cell (startRow, startCol) facing in direction startDir, which is one of "up", "down", "left", or "right".
The cell it starts on may contain a mirror, but the mirror does not affect the beam's initial direction; mirrors only affect the beam when it enters a cell that contains one.

## Movement
At each step, the beam attempts to move one cell in its current direction.
If the next cell would be outside the grid, the beam stops.
If the next cell is inside, it moves there. Then:

If the cell contains a / mirror: the beam's direction changes as if reflecting off a line with slope 1: "up" becomes "right", "right" becomes "up", "down" becomes "left", "left" becomes "down".
If the cell contains a \ mirror: the beam's direction changes as if reflecting off a line with slope -1: "up" becomes "left", "left" becomes "up", "down" becomes "right", "right" becomes "down".

## Trajectory
You must record the beam's position and direction at the beginning of each step (before moving).
That means:

The first entry is the starting cell and starting direction.
After moving into a new cell (and possibly reflecting), the beam's position and new direction are recorded for the next step.
The recording stops after the step that leaves the grid or when a loop is detected.

## Loop Detection
It is possible for the beam to get trapped in a cycle.
If the beam ever revisits the same cell with the same direction it had on a previous visit, it is caught in a loop and will never leave.
The simulation must stop at that point; the repeated state is included as the final entry of the trajectory.

## Output
Return an object with three arrays: rows, cols, and dirs.
The arrays have the same length; element i gives the beam's position and direction at step i.
"""

DIRS = {"right": (1, 0), "up": (0, -1), "left": (-1, 0), "down": (0, 1)}
VECTORS = list(DIRS.values()) * 2
SRID = {v: k for k, v in DIRS.items()}
ROT = {
    "L": dict(zip(VECTORS, VECTORS[1:])),
    "R": dict(zip(VECTORS[1:], VECTORS)),
}


def photonPath(n, x, y, d, grid):
    "Return a dict with keys 'rows', 'cols', 'dirs'."
    o_rows = []
    o_cols = []
    o_dirs = []

    board = {
        (bx, by): v
        for by, row in enumerate(grid[i:i+n] for i in range(0, n*n, n))
        for bx, v in enumerate(row)
    }
    dx, dy = DIRS[d]
    seen = set()

    while True:
        o_rows.append(y)
        o_cols.append(x)
        o_dirs.append(SRID[dx, dy])
        x += dx
        y += dy
        if (x, y) not in board:
            break
        if (x, y, dx, dy) in seen:
            break
        seen.add((x, y, dx, dy))
        v = board[x, y]
        if v == 0:
            continue
        if (v == 1 and dy == 0) or (v == 2 and dy != 0):
            dx, dy = ROT["L"][dx, dy]
        else:
            dx, dy = ROT["R"][dx, dy]

    return {"rows": o_rows, "cols": o_cols, "dirs": o_dirs}

assert photonPath(4, 0, 0, "right", [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == {"rows": [0, 0, 0, 0], "cols": [0, 1, 2, 3], "dirs": ["right", "right", "right", "right"]}
assert photonPath(4, 1, 1, "right", [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == {"rows": [1, 1, 0], "cols": [1, 2, 2], "dirs": ["right", "up", "up"]}
assert photonPath(4, 0, 0, "right", [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]) == {"rows": [0, 0, 0, 1, 2, 2, 2], "cols": [0, 1, 2, 2, 2, 1, 0], "dirs": ["right", "right", "down", "down", "left", "left", "left"]}
assert photonPath(
        2, 0, 0, "right", [1, 2, 2, 1]
        ) == {
        "rows": [0, 0, 1, 1, 0], "cols": [0, 1, 1, 0, 0],
        "dirs": ["right", "down", "left", "up", "right"]}
assert photonPath(
        3, 0, 0, "right", [1, 2, 0, 2, 0, 2, 0, 2, 1]
        ) == {
        "rows": [0, 0, 1, 2, 2, 1, 1, 1, 0],
        "cols": [0, 1, 1, 1, 2, 2, 1, 0, 0],
        "dirs": ["right", "down", "down", "right", "up",
                 "left", "left", "up", "right"]}

