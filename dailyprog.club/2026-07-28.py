"""The Queen's Garden

The royal gardener must place n rose bushes in an n × n grid.
No two bushes may share the same row, column, or diagonal (including both main diagonals).
Count the number of distinct ways to arrange all n bushes.
"""
import functools

@functools.cache
def ways(n, available):
    if n > len(available):
        return 0
    if n == 1:
        return len(available)
    explore, *rest = sorted(available)
    filtered = [
        i for i in rest
        if (
            explore[0] != i[0]     # same column
            and explore[1] != i[1] # same row
            and abs(explore[0] - i[0]) != abs(explore[1] - i[1]) # same diagonal
        )
    ]
    return ways(n, frozenset(rest)) + ways(n - 1, frozenset(filtered))

def bushArrangementsA(n):
    """Return number of valid placements."""
    return ways(n, frozenset((x, y) for x in range(n) for y in range(n)))

def bushArrangements(n):
    """Return number of valid placements."""
    placed = set()
    cols = set()

    def solve(row):
        if row == n:
            return 1
        options = 0
        for col in range(n):
            if col in cols:
                continue  # this columns already has a piece
            if any(abs(i[0] - col) == abs(i[1] - row) for i in placed):
                continue  # this diagonal already has a piece
            placed.add((col, row))
            cols.add(col)
            options += solve(row + 1)
            placed.remove((col, row))
            cols.remove(col)
        return options

    return solve(0)







assert bushArrangements(1) == 1
assert bushArrangements(2) == 0
assert bushArrangements(4) == 2

