import functools
import collections
import itertools
import re
import time

def parse():
    with open("data/17.txt") as f:
        return next(f).strip()

def shiftadd(vals):
    out = 0
    for v in vals:
        out <<= 3
        out |= v
    return out

def solve(parsed_input, n) -> int:
        rocks = [
            {complex(0, 0), complex(1, 0), complex(2, 0), complex(3, 0)},
            {complex(1, 0), complex(0, 1), complex(1, 1), complex(2, 1), complex(1, 2)},
            {complex(0, 0), complex(1, 0), complex(2, 0), complex(2, 1), complex(2,2)},
            {complex(0, 0), complex(0, 1), complex(0, 2), complex(0, 3)},
            {complex(0, 0), complex(0, 1), complex(1, 0), complex(1, 1)},
        ]
        heights = [int(max(i.imag for i in r)) for r in rocks]
        stream_size = len(parsed_input)
        stream = parsed_input
        gravity = complex(0, -1)

        landed = set()
        height = 0
        seen = {}

        # SHOW = 20
        cycle_detection = None
        height_deltas = collections.deque([0] * 40)

        wind_idx = -1
        rock_cnt = -1

        while rock_cnt + 1 < n:
            rock_cnt += 1
            if rock_cnt and rock_cnt % 1000000 == 0:
                print(f"Step {rock_cnt}")
            rock_shape = rocks[rock_cnt % 5]
            bottom_left_corner = complex(2, height + 4)

            while True:
                wind_idx = (wind_idx + 1) % stream_size
                wind = -1 if stream[wind_idx] == "<" else +1
                o2 = wind + bottom_left_corner
                r2 = {r + o2 for r in rock_shape}
                if all(0 <= r.real < 7 for r in r2) and landed.isdisjoint(r2):
                    bottom_left_corner = o2

                o2 = gravity + bottom_left_corner
                r2 = {r + o2 for r in rock_shape}
                if all(0 < r.imag for r in r2) and landed.isdisjoint(r2):
                    bottom_left_corner = o2
                else:
                    break

            landed.update({bottom_left_corner + r for r in rock_shape})
            new_height = max(height, int(bottom_left_corner.imag) + heights[rock_cnt%5])
            height_deltas.append(new_height - height)
            height_deltas.popleft()
            height = new_height

            if rock_cnt < 10000000 and all(complex(x, height) in landed for x in range(7)):
                t = ((((wind_idx) << 4) | (rock_cnt % 5)), shiftadd(height_deltas))
                if t not in seen:
                    seen[t] = (rock_cnt, height)
                else:
                    prior_rock_cnt, prior_height = seen[t]
                    print(f"Cycle found {prior_rock_cnt, prior_height} -> {rock_cnt, height}.")
                    print(height_deltas, shiftadd(height_deltas))

                    # assert prior_rock_cnt == 1610, prior_rock_cnt
                    # assert prior_height == 2524

                    if True:
                        cycle_size = rock_cnt - prior_rock_cnt
                        height_diff = height - prior_height

                        cycle_count = (n - rock_cnt) // cycle_size
                        rock_cnt += cycle_count * cycle_size
                        height += cycle_count * height_diff
                        landed.update(complex(x, height) for x in range(7))

                        assert n - cycle_count < rock_cnt < n

            if True:
                cut = 0
                if rock_cnt % 100000 == 0:
                    for h in range(height, height - 1000, -1):
                        if all(complex(x, h) in landed for x in range(7)):
                            landed = {i for i in landed if i.imag >= h}
                            # print(f"{i=} {h=} {len(landed)=}")
                            break

        return height

if __name__ == "__main__":
    height = solve('>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>', 1000000000000)
    print(height)
    assert height == 1514285714288

