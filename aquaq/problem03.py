"""Aquaq Day N."""

MAP = """\
  ##
 ####
######
######
 ####
  ##
"""

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    tiles = {
        complex(x, y)
        for y, row in enumerate(MAP.splitlines())
        for x, char in enumerate(row)
        if char == "#"
    }
    pos = complex(2, 0)
    total = 0
    for i in data:
        direction = {"U": complex(0, -1), "D": complex(0, 1), "R": complex(1, 0), "L": complex(-1, 0)}[i]
        if pos + direction in tiles:
            pos += direction
        total += pos.real + pos.imag
    return total


TESTS = [(1, "UDRR", 14)]
