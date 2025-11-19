"""Everyone Codes Day N."""

import math
import time
from lib import helpers
from lib import parsers


def experiment2(ducks):
    """Sort ducks right-to-left and count moves.

    Look for peaks that can flow into basins.

    *
    *
    **  *
    **  *
    *****
    12345 COL
    00000 MOVES

    In this example, two ducks from col 1 can flow into the basin on cols 3-4.

    1. Find a peak: any column taller than the next column.
    2. Find the basin: the first column shorter than the next one. Flow into here. Extend this basin if there are repeated low columns.
    3. Determine how high the basin can be filled.
    3a. If the peak is adjacent to the basin: `(source - dest) / (width + 1) * width` (rounded up/down/maybe).
    3b. If the peak is not adjacent to the basin: `min( [source - source_neighbor], [basin_right - basin], [basin_left, basin] )`.
    4. Flood fill the basin, tracking movements. Source through basin edge have movement of flow amount. Basin tiles get moves equal to `sum(fill for that column and all basin columns to its right)`.
    5. Basin fill is a tad messy unless `flow_amount % basin_width == 0`. I used `basin_fills, extra = divmod(flow_amount, basin_width)` where the right `extra` spots of the basin get `basin_fills + 1` and the left part of the basin gets `basin_fills`.
    """
    big = sum(ducks)
    num = len(ducks) - 1
    moves = [0] * len(ducks)

    steps = 0
    while any(a > b for a, b in zip(ducks, ducks[1:])):
        print("COLS", " ".join(str(i).rjust(3) for i in ducks), "=", sum(ducks))
        print("MOVE", " ".join(str(i).rjust(3) for i in moves))
        print()
        peak_idx, peak_height, peak_adjacent = next(
            (idx, a, b)
            for idx, (a, b) in enumerate(zip(ducks, ducks[1:]))
            if a > b
        )
        basin_end_idx, basin_height, right_edge_height = next(
            (
                (idx, a, b)
                for idx, (a, b) in enumerate(zip(ducks, ducks[1:]))
                if a < b and idx > peak_idx
            ),
            # If the basin hits the right end, end the basin in the right most column.
            (num, ducks[num], big)
        )
        basin_start_idx, left_edge_height = next(
            (idx + 1, a)
            for idx, (a, b) in enumerate(zip(ducks, ducks[1:]))
            if peak_idx <= idx < basin_end_idx and b == basin_height
        )
        basin_width = basin_end_idx - basin_start_idx + 1

        # Maximum number of ducks that can move:
        # Don't overflow the basin and don't make the peak lower than its neighbor.
        fill_amount = min(peak_height - peak_adjacent, min(right_edge_height - basin_height, left_edge_height - basin_height) * basin_width)

        # If the peak is also the basin edge, don't make the peak lower than the basin height.
        if peak_idx + 1 == basin_start_idx:
            fill_amount = min(fill_amount, int(math.ceil((peak_height - peak_adjacent) * basin_width / (basin_width + 1))))

        # t = int(math.ceil(fill_amount / basin_width))
        # while high - fill_amount + 1 < low + t:
        #     fill_amount -= 1
        #     t = int(math.ceil(fill_amount / basin_width))
        # print(f"{basin_width=}, {high - low=}, {fill_amount=}")
        print(f"Move {fill_amount} from {peak_idx} to basin {basin_start_idx}..{basin_end_idx}.")

        all_fill, extra = divmod(fill_amount, basin_width)
        # print(f"Fill from {src} to {start}..{edge} with {fill_amount=} -- {all_fill=}, {extra=}")
        ducks[peak_idx] -= fill_amount
        # All ducks flow from the peak into the basin.
        for i in range(peak_idx, basin_start_idx):
            moves[i] += fill_amount
        # Fill the basin from the far side, which gets the extra ducks.
        moved = 0
        for i in range(basin_end_idx, basin_end_idx - extra, -1):
            ducks[i] += all_fill + 1
            moved += all_fill + 1
            moves[i] += moved
        for i in range(basin_end_idx - extra, basin_start_idx - 1, -1):
            ducks[i] += all_fill
            moved += all_fill
            moves[i] += moved

    print("COLS", " ".join(str(i).rjust(3) for i in ducks), "=", sum(ducks))
    print("MOVE", " ".join(str(i).rjust(3) for i in moves))
    print("EXPR", ducks, sum(ducks))
    return max(moves), ducks

def solve(part: int, data: list[int]) -> int:
    """Solve the parts."""
    # data = [9, 1, 1, 3, 1, 9]
    ducks = data.copy()
    num = len(ducks) - 1

    if True:
        start = time.perf_counter_ns()
        steps = 0
        while any(a > b for a, b in zip(ducks, ducks[1:])):
            steps += 1
            for i in range(num):
                if ducks[i] > ducks[i + 1]:
                    ducks[i] -= 1
                    ducks[i + 1] += 1
        end = time.perf_counter_ns()
        brute = end - start
        print("WANT", ducks, sum(ducks))
        start = time.perf_counter_ns()
        got_steps, got_ducks = experiment2(data)
        end = time.perf_counter_ns()
        flow = end - start
        print(f"{steps=} <> {got_steps=} :: {brute/1000} vs {flow/1000}")
        if steps != got_steps:
            print(f"{steps=} != {got_steps=}")
    else:
        steps, ducks = experiment2(data)

    if part > 1:
        assert ducks == sorted(ducks)
        average = sum(ducks) // len(ducks)
        return steps + sum(abs(i - average) for i in ducks) // 2

    for _ in range(steps, 10):
        for i in range(num):
            if ducks[i] < ducks[i + 1]:
                ducks[i] += 1
                ducks[i + 1] -= 1
    return sum(idx * count for idx, count in enumerate(ducks, start=1))


PARSER = parsers.parse_one_int_per_line
TEST_DATA = [
    """\
9
1
1
4
9
6""",
    """\
9
1
1
4
9
6""",
    """\
805
706
179
48
158
150
232
885
598
524
423""",
]
TESTS = [
    (1, TEST_DATA[0], 109),
    (2, TEST_DATA[1], 11),
    (2, TEST_DATA[2], 1579),
]

if __name__ == "__main__":
    helpers.run_solution(globals())
