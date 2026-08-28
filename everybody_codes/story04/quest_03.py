"""Everyone Codes Day N."""

import logging
from lib import helpers
from lib import parsers

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    parsed = {}
    for line in data:
        k, v = line.split("=")
        parsed[k] = v
    height, width = int(parsed["height"]), int(parsed["width"])
    lhoff = len(parsed["horizontal-offsets"])
    lvoff = len(parsed["vertical-offsets"])
    size = lhoff * lvoff * 2
    hrep, hrem = divmod(width, size)
    vrep, vrem = divmod(height, size)
    # logging.debug(f"{height=}, {width=}, {lhoff=}, {lvoff=}, {vrep, vrem=}, {hrep, hrem=}, {size=}")

    last_row_start = True
    count = {True: 0, False: 0}
    perc = max(1, size // 100)
    for y in range(size):
        if y % perc == 0:
            log("%d%%", y // perc)
        if y == vrem:
            ycopy = count.copy()
        x = 0
        t = x % 2 == int(parsed["horizontal-offsets"][y % len(parsed["horizontal-offsets"])]) or y == 0
        cur = last_row_start if not t else not last_row_start
        last_row_start = cur
        xcount = {True: 0, False: 0}
        for x in range(size):
            if x == hrem:
                count[True] += xcount[True]
                count[False] += xcount[False]
            l = y % 2 == int(parsed["vertical-offsets"][x % len(parsed["vertical-offsets"])])
            r = y % 2 == int(parsed["vertical-offsets"][(x + 1) % len(parsed["vertical-offsets"])])
            t = x % 2 == int(parsed["horizontal-offsets"][y % len(parsed["horizontal-offsets"])])
            b = x % 2 == int(parsed["horizontal-offsets"][(y + 1) % len(parsed["horizontal-offsets"])])
            if l and r and t and b:
                xcount[cur] += 1
            if r:
                cur = not cur
        count[True] += hrep * xcount[True]
        count[False] += hrep * xcount[False]
    ycopy[True] += vrep * count[True]
    ycopy[False] += vrep * count[False]
    if part == 1:
        return sum(ycopy.values())
    return max(ycopy.values())

    isolated = set()
    for x in range(width):
        for y in range(height):
            l = y % 2 == int(parsed["vertical-offsets"][x % len(parsed["vertical-offsets"])])
            r = y % 2 == int(parsed["vertical-offsets"][(x + 1) % len(parsed["vertical-offsets"])])
            t = x % 2 == int(parsed["horizontal-offsets"][y % len(parsed["horizontal-offsets"])])
            b = x % 2 == int(parsed["horizontal-offsets"][(y + 1) % len(parsed["horizontal-offsets"])])
            if l and r and t and b:
                isolated.add((x, y))
    if part == 1:
        return len(isolated)

    color = {(0, 0): True}
    for x in range(width - 1):
        for y in range(height - 1):
            r = y % 2 == int(parsed["vertical-offsets"][(x + 1) % len(parsed["vertical-offsets"])])
            b = x % 2 == int(parsed["horizontal-offsets"][(y + 1) % len(parsed["horizontal-offsets"])])
            cur = color[x, y]
            color[x + 1, y] = cur if not r else not cur
            color[x, y + 1] = cur if not b else not cur

    x, y = width - 2, height - 1
    r = y % 2 == int(parsed["vertical-offsets"][(x + 1) % len(parsed["vertical-offsets"])])
    cur = color[x, y]
    color[x + 1, y] = cur if not r else not cur

    count = {True: 0, False: 0}
    for i in isolated:
        count[color[i]] += 1
    return max(count.values())


# PARSER = parsers.parse_one_str
TEST_DATA = [
    """\
width=30
height=10
horizontal-offsets=10011
vertical-offsets=11011""",
    """\
width=40
height=12
horizontal-offsets=11100
vertical-offsets=001101""",
    """\
width=100
height=70
horizontal-offsets=111101111101101111000100100110
vertical-offsets=110100001110111011101000001111""",
    """\
""",
    """\
""",
]
TESTS = [
    (1, TEST_DATA[0], 27),
    (2, TEST_DATA[0], 15),
    (2, TEST_DATA[1], 7),
    (2, TEST_DATA[2], 269),
    # (2, TEST_DATA[1], None),
    # (3, TEST_DATA[2], None),
]

if __name__ == "__main__":
    helpers.run_solution(globals())
