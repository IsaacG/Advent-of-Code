"""Turtle Walk

A turtle starts at the top-left corner (row 0, col 0) of an n × n grid, facing right.
It receives a list of commands: - "forward" moves one cell in the direction it's facing - "left" and "right" turn 90° without moving The turtle never leaves the grid (you can assume valid commands).
Return the turtle's trajectory as three equal-length arrays, one entry per step.
Index 0 is the initial state, before any command, and each command adds one more entry: - rows: the turtle's row at each step - cols: the turtle's column at each step - dirs: the direction it faces at each step, one of "up", "down", "left", or "right" The visualizer replays this trajectory to draw the grid and the turtle's path, so you only return where it went, not the grid itself.
"""

def turtleWalk(n, commands):
    # Return {"rows": [...], "cols": [...], "dirs": [...]}: the turtle's
    # row, column, and facing at each step (index 0 is the start).
    deltas = {
        "right": (1, 0),
        "up": (0, -1),
        "left": (-1, 0),
        "down": (0, 1),
    }
    directions = list(deltas) * 2
    rotate = {
        "right": dict(zip(directions[1:], directions)),
        "left": dict(zip(directions, directions[1:])),
    }

    x, y = 0, 0
    direction = "right"
    result = {"rows": [y], "cols": [x], "dirs": [direction]}

    for command in commands:
        if command == "forward":
            dx, dy = deltas[direction]
            x += dx
            y += dy
        else:
            direction = rotate[command][direction]
        result["rows"].append(y)
        result["cols"].append(x)
        result["dirs"].append(direction)
    return result

assert turtleWalk(3, ["forward"]) == {"rows": [0, 0], "cols": [0, 1], "dirs": ["right", "right"]}
assert turtleWalk(3, ["right", "forward"]) == {"rows": [0, 0, 1], "cols": [0, 0, 0], "dirs": ["right", "down", "down"]}
assert turtleWalk(4, ["forward", "right", "forward", "right", "forward", "right", "forward"]) == {"rows": [0, 0, 0, 1, 1, 1, 1, 0], "cols": [0, 1, 1, 1, 1, 0, 0, 0], "dirs": ["right", "right", "down", "down", "left", "left", "up", "up"]}
assert turtleWalk(2, ["forward", "left", "left", "forward"]) == {"rows": [0, 0, 0, 0, 0], "cols": [0, 1, 1, 1, 0], "dirs": ["right", "right", "up", "left", "left"]}

