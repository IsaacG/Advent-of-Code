"""Aquaq Day N."""

class Die:
    """Model a die with support for rotations. Borrows from Codyssi problem 20."""

    FACES = list(range(1, 7))

    def __init__(self, cur, left, up):
        # Up, right, down, left
        self.NEIGHBORS = {}
        self.cur = cur
        self.up = up
        self.set(cur, left=left, up=up)
        self.set(left, right=cur, up=up)
        self.set(up, up=cur, right=left)
        print(self.NEIGHBORS)

    def set(self, face, up=None, right=None, down=None, left=None):
        up = up or 7 - down
        right = right or 7 - left
        down = down or 7 - up
        left = left or 7 - right
        assert all([up, right, down, left])
        self.NEIGHBORS[face] = (up, right, down, left)
        self.NEIGHBORS[7 - face] = (up, left, down, right)

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


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    dice = [Die(1, 2, 3), Die(1, 3, 2)]
    total = 0
    for idx, direction in enumerate(data):
        for die in dice:
            die.rotate(direction)
            if dice[0].cur == dice[1].cur:
                total += idx
    assert total != 16477
    return total


TESTS = [
    (1, "LRDLU", 5),
]
