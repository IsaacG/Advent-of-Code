"""Codyssi Day N."""

import collections
import functools
import itertools
import logging
import queue
import re

log = logging.info

def solve(part: int, data: str, test_number: int | None) -> int:
    """Solve the parts."""
    # Set up the parameters.
    if test_number == 2 or test_number == 4:
        short = True
        size = (3, 3, 5, 3)
    else:
        short = False
        size = (10, 15, 60, 3)
    size_x, size_y, size_z, size_a = size
    end = (size[0] - 1, size[1] - 1, size[2] - 1, 0)
    end_x, end_y, end_z, end_a = end
    space = (range(size[0]), range(size[1]), range(size[2]), range(-1, 2))

    # Parse the input.
    rules = []
    for line in data.splitlines():
        m = re.fullmatch(
            r"RULE (\d+): (-?\d+)x([+-]\d+)y([+-]\d+)z([+-]\d+)a DIVIDE (\d+) HAS REMAINDER (\d+) \| "
            + r"DEBRIS VELOCITY \((-?\d+), (-?\d+), (-?\d+), (-?\d+)\)",
            line,
        )
        assert m is not None
        rules.append([int(i) for i in m.groups()])

    # For each rule, for each position, check for debris.
    debris = []
    for _, mult_x, mult_y, mult_z, mult_a, mod, rem, vx, vy, vz, va in rules:
        for pos_x, pos_y, pos_z, pos_a in itertools.product(*space):
            res = mult_x * pos_x + mult_y * pos_y + mult_z * pos_z + mult_a * pos_a
            if res % mod == rem:
                debris.append((pos_x, pos_y, pos_z, pos_a + 1, vx, vy, vz, va))

    if part == 1:
        return len(debris)

    @functools.cache
    def debris_field(t):
        """Return the location of all pieces of debris at any given time."""
        return {
            ((ix + vx * t) % size_x, (iy + vy * t) % size_y, (iz + vz * t) % size_z)
            for ix, iy, iz, ia, vx, vy, vz, va in debris
            if (ia + va * t) % 3 == 1
        }

    @functools.cache
    def debris_field_count(t):
        """Return the location of all pieces of debris at any given time."""
        counter = collections.defaultdict(int)
        for ix, iy, iz, ia, vx, vy, vz, va in debris:
            if (ia + va * t) % 3 == 1:
                counter[((ix + vx * t) % size_x, (iy + vy * t) % size_y, (iz + vz * t) % size_z)] += 1
        counter[(0, 0, 0)] = 0
        return counter


    max_hits = 0 if part == 2 else 3
    seen = set()

    # All possible moves.
    moves = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (1, 0, 0), (0, 0, -1), (0, -1, 0), (-1, 0, 0)]
    q = queue.PriorityQueue()
    start = (0, 0, 0)
    q.put((0, *start, 0, 0))
    steps = 0
    # A-star with Manhatten distance.
    while not q.empty():
        _, x, y, z, t, hits = q.get()
        if x == end_x and y == end_y and z == end_z:
            return t

        steps += 1
        if steps and steps % 100000 == 0:
            log(f"Size: {q.qsize()}, {t=}, {hits=}")

        t += 1
        for dx, dy, dz in moves:
            # Skip moves that would move us out of feasible space.
            if not  0 <= (nx := x + dx) < size_x: continue
            if not  0 <= (ny := y + dy) < size_y: continue
            if not  0 <= (nz := z + dz) < size_z: continue
            # Do not re-check positions we've tried before.
            if (nx, ny, nz, t, hits) not in seen:
                seen.add((nx, ny, nz, t, hits))
                nhits = hits + debris_field_count(t)[nx, ny, nz]
                if nhits <= max_hits:
                    # distance = abs(nx - end_x) + abs(ny - end_y) + abs(nz - end_z)
                    q.put((t, nx, ny, nz, t, nhits))


TEST_DATA = [
    """\
RULE 1: 8x+2y+3z+5a DIVIDE 9 HAS REMAINDER 4 | DEBRIS VELOCITY (0, -1, 0, 1)
RULE 2: 4x+7y+10z+9a DIVIDE 5 HAS REMAINDER 4 | DEBRIS VELOCITY (0, 1, 0, 1)
RULE 3: 6x+3y+7z+3a DIVIDE 4 HAS REMAINDER 1 | DEBRIS VELOCITY (-1, 0, 1, -1)
RULE 4: 3x+11y+11z+3a DIVIDE 2 HAS REMAINDER 1 | DEBRIS VELOCITY (-1, 1, 0, -1)""",
    """\
RULE 1: 8x+10y+3z+5a DIVIDE 9 HAS REMAINDER 4 | DEBRIS VELOCITY (0, -1, 0, 1)
RULE 2: 3x+7y+10z+9a DIVIDE 9 HAS REMAINDER 4 | DEBRIS VELOCITY (0, 1, 0, 1)
RULE 3: 10x+3y+7z+3a DIVIDE 11 HAS REMAINDER 9 | DEBRIS VELOCITY (-1, 0, 1, -1)
RULE 4: 5x+4y+9z+3a DIVIDE 7 HAS REMAINDER 2 | DEBRIS VELOCITY (0, -1, -1, -1)
RULE 5: 3x+11y+11z+3a DIVIDE 3 HAS REMAINDER 1 | DEBRIS VELOCITY (-1, 1, 0, -1)
RULE 6: 4x+6y+7z+3a DIVIDE 8 HAS REMAINDER 6 | DEBRIS VELOCITY (0, -1, 0, -1)
RULE 7: 7x+4y+3z+7a DIVIDE 11 HAS REMAINDER 5 | DEBRIS VELOCITY (0, 1, 0, -1)
RULE 8: 3x+6y+9z+9a DIVIDE 5 HAS REMAINDER 3 | DEBRIS VELOCITY (1, 1, -1, -1)
"""]
TESTS = [
    (1, TEST_DATA[1], 32545),
    (2, TEST_DATA[0], 23),
    (2, TEST_DATA[1], 217),
    (3, TEST_DATA[0], 8),
    (3, TEST_DATA[1], 166),
]
