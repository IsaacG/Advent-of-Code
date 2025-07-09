"""Codyssi Day N."""

import logging
import math

log = logging.info

class Die:
    """Model a die with support for rotations.

    Die layout:
       6
      423
       1
       5
    """

    NEIGHBORS = {
        1: (2, 3, 5, 4),
        2: (6, 3, 1, 4),
        6: (5, 3, 2, 4),
        5: (1, 3, 6, 4),
        3: (6, 5, 1, 2),
        4: (6, 2, 1, 5),
    }
    FACES = list(NEIGHBORS)

    def __init__(self, cur=None, up=None):
        # Start with the current face as 1 with the "up" as 2.
        self.cur = cur or 1
        self.up  = up  or 2

    def shifted(self, other=None):
        """Return how rotated the side is from the "default" orientation."""
        return self.NEIGHBORS[self.cur].index(other or self.up)

    def rotate(self, direction):
        """Rotate the die in a direction."""
        offset = "URDL0".index(direction)
        old = self.cur
        # Which face do we want as the new current.
        new_up_offset = self.shifted() + offset
        new_cur = self.NEIGHBORS[self.cur][new_up_offset % 4]
        self.cur = new_cur
        # On rotate down, the new up is the old cur.
        # Rotating left/right does not change the up.
        if offset == 0:    # up
            new_up_offset = self.shifted(old) + 2
            self.up = self.NEIGHBORS[self.cur][new_up_offset % 4]
        elif offset == 2:  # down
            self.up = old


def part_one(changes_blk: str, twists: str, size: int) -> int:
    """Solve part one."""
    die = Die()
    absorption = {face: 0 for face in die.FACES}
    for instruction, twist in zip(changes_blk.splitlines(), twists + "0"):
        affect, val = instruction.split(" - VALUE ")
        cell_count = size * (size if affect == "FACE" else 1)
        absorption[die.cur] += cell_count * int(val)

        die.rotate(twist)

    return math.prod(sorted(absorption.values())[-2:])


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    changes_blk, twists = data.split("\n\n")
    size = 3 if twists == "LURD" else 80
    if part == 1:
        return part_one(changes_blk, twists, size)

    die = Die()
    cell_values = {
        face: {(x, y): 0 for x in range(size) for y in range(size)}
        for face in die.FACES
    }

    def update_values(affect, val):
        if affect == "FACE":
            effects = [(x, y) for x in range(size) for y in range(size)]
        else:
            row_or_col, row_col_num_s = affect.split()
            row = row_or_col == "ROW"
            row_col_num = int(row_col_num_s) - 1
            shifted = die.shifted()
            # When rotates an odd number of times, a row is a column in the upright orientation and vice versa.
            if shifted % 2 == 1:
                row = not row
            # Depending on the orientation, row/col 1 may be row/col `size - 1`.
            if (row and shifted in (2, 3)) or (not row and shifted in (1, 2)):
                row_col_num = size - 1 - row_col_num
            if row:
                effects = [(x, row_col_num) for x in range(size)]
            else:
                effects = [(row_col_num, y) for y in range(size)]
        # Actually update the cell values.
        for xy in effects:
            cell_values[die.cur][xy] = (cell_values[die.cur][xy] + val) % 100

    for instruction, twist in zip(changes_blk.splitlines(), twists + "0"):
        affect, val_s = instruction.split(" - VALUE ")
        val = int(val_s)
        if part == 2 or affect == "FACE":
            update_values(affect, val)
        else:
            rot = "R" if affect.split()[0] == "ROW" else "U"
            for _ in range(4):
                update_values(affect, val)
                die.rotate(rot)

        die.rotate(twist)

    return math.prod(
        max(
            # Find the biggest row and biggest column for each side.
            max(sum(side[x, y] for x in range(size)) for y in range(size)),
            max(sum(side[x, y] for y in range(size)) for x in range(size)),
        ) + size
        for side in cell_values.values()
    )


TEST_DATA = [
    """\
FACE - VALUE 38
ROW 2 - VALUE 71
ROW 1 - VALUE 57
ROW 3 - VALUE 68
COL 1 - VALUE 52

LURD""",
    """\
FACE - VALUE 38
COL 32 - VALUE 39
COL 72 - VALUE 12
COL 59 - VALUE 56
COL 77 - VALUE 31
FACE - VALUE 43
COL 56 - VALUE 47
ROW 73 - VALUE 83
COL 15 - VALUE 87
COL 76 - VALUE 57

ULDLRLLRU"""
]
TESTS = [
    (1, TEST_DATA[0], 201474),
    (1, TEST_DATA[1], 6902016000),
    (2, TEST_DATA[0], 118727856),
    (2, TEST_DATA[1], 369594451623936000000),
    (3, TEST_DATA[0], 59477096746944),
    (3, TEST_DATA[1], 118479211258970523303936),
]
