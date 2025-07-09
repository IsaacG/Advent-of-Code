"""Codyssi Day N."""

import logging
import math

log = logging.info

class Die:
    """Model a die.

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
        return self.NEIGHBORS[self.cur].index(other or self.up)

    def _rotate(self, offset):
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

    def rotate_up(self):
        self._rotate(0)

    def rotate_right(self):
        self._rotate(1)

    def rotate_down(self):
        self._rotate(2)

    def rotate_left(self):
        self._rotate(3)


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    size = 80
    changes_blk, twists = data.split("\n\n")
    # size = 3
    # changes_blk = "ROW 1 - VALUE 5"
    # twists = ""
    if twists == "LURD":
        size = 3
    # die = Die(1, 4)
    die = Die(6, 5)
    absorption = {i: 0 for i in die.FACES}
    cells = {
        i: {(x, y): 0 for x in range(size) for y in range(size)}
        for i in die.FACES
    }

    def update_values(affect, val):
        if affect == "FACE":
            affects = [(x, y) for x in range(size) for y in range(size)]
        else:
            t, s = affect.split()
            row = t == "ROW"
            n = int(s) - 1
            shifted = die.shifted()
            if shifted % 2 == 1:
                row = not row
            if (row and shifted in (2, 3)) or (not row and shifted in (1, 2)):
                n = size - 1 - n
            if row:
                affects = [(x, n) for x in range(size)]
            else:
                affects = [(n, y) for y in range(size)]
        for xy in affects:
            cells[die.cur][xy] = (cells[die.cur][xy] + val) % 100

    for instruction, twist in zip(changes_blk.splitlines(), twists + "0"):
        old = die.cur
        affect, val_s = instruction.split(" - VALUE ")
        val = int(val_s)
        cell_count = size
        if part == 1:
            if affect == "FACE":
                cell_count *= size
            absorption[die.cur] += cell_count * val
        else:
            if part == 2 or affect == "FACE":
                update_values(affect, val)
            else:
                rot = die.rotate_right if affect.split()[0] == "ROW" else die.rotate_up
                for _ in range(4):
                    update_values(affect, val)
                    rot()
                    
            if part == 3 and size == 3 and False:
                for faces in "060\n423\n010\n050".splitlines():
                    for y in range(size):
                        print(" ".join(str(cells.get(int(face), {}).get((x, y), " ")).ljust(2) for face in faces for x in range(size)))
                print()


        # rotate
        {"L": die.rotate_left, "R": die.rotate_right, "U": die.rotate_up, "D": die.rotate_down, "0": lambda: None}[twist]()
        # print(f"{old} * {twist} = {die.cur}")

    if part == 1:
        out = math.prod(sorted(absorption.values())[-2:])
        assert out != 164746320665600
        return out
    if part in (2, 3):
        if size == 3 and False:
            for i, side in cells.items():
                print(f"== {i} ==")
                for y in range(size):
                    print(" ".join(str(side[x, y] + 1) for x in range(size)))
                print()

        return math.prod(
            max(
                max(sum(side[x, y] for x in range(size)) for y in range(size)),
                max(sum(side[x, y] for y in range(size)) for x in range(size)),
            ) + size
            for side in cells.values()
        )
    if part == 3:
        return


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
