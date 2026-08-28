"""Everyone Codes Day N."""

import logging
from lib import helpers


def solve(part: int, data: list[str]) -> int:
    """Solve the parts."""
    parsed = dict(line.split("=", 1) for line in data)
    height, width = int(parsed["height"]), int(parsed["width"])
    horiz_offsets = [int(i) for i in parsed["horizontal-offsets"]]
    vert_offsets = [int(i) for i in parsed["vertical-offsets"]]
    len_x_offsets = len(horiz_offsets)
    len_y_offsets = len(vert_offsets)

    # Patterns repeat after x_offsets * y_offsets
    # Only check up to x_offsets * y_offsets (or width/height) in each direction.
    # Except ... double that in case the pattern alternates.
    size_x = min(width, len_x_offsets * len_y_offsets * 2)
    repeated_x, remainder_x = divmod(width, size_x)

    size_y = min(height, len_x_offsets * len_y_offsets * 2)
    repeated_y, remainder_y = divmod(height, size_y)

    prior_row_color = True  # Arbitrary color for the first cell.
    ycount = {True: 0, False: 0}
    status_step = max(1, size_y // 100)  # for status output printing
    for y in range(size_y):
        if y % status_step == 0:
            logging.info("%d%%", y // status_step)
        # This section is repeated after the last full block.
        if y == remainder_y:
            count = ycount.copy()
        top = 0 == horiz_offsets[y % len_x_offsets]
        # The start color of each row can be determined by the start color of the prior row.
        # Flip colors if we cross a line.
        cur = prior_row_color = prior_row_color != top
        xcount = {True: 0, False: 0}
        for x in range(size_x):
            # This section is repeated after the last full block.
            if x == remainder_x:
                for color, num in xcount.items():
                    ycount[color] += num
            # Check for a border on all four sides.
            left = y % 2 == vert_offsets[x % len_y_offsets]
            right = y % 2 == vert_offsets[(x + 1) % len_y_offsets]
            top = x % 2 == horiz_offsets[y % len_x_offsets]
            bottom = x % 2 == horiz_offsets[(y + 1) % len_x_offsets]
            # If there is a border on all four sides, this cell is isolated.
            if left and right and top and bottom:
                xcount[cur] += 1
            cur = cur != right  # Change colors when crossing a line.
        # This section is repeated fully x times.
        for color, num in xcount.items():
            ycount[color] += repeated_x * num
    # This section is repeated fully y times.
    for color, num in ycount.items():
        count[color] += repeated_y * num

    return (sum if part == 1 else max)(count.values())


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
