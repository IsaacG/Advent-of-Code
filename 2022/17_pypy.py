import functools
import collections
import itertools
import re
import time

def parse():
    with open("data/17.txt") as f:
        return next(f).strip()

def solve(parsed_input, n) -> int:
        # n=2022
        direction = {"<": -1, ">": +1}
        rocks = [
            {0, 1, 2, 3},
            {complex(1, 0), complex(0, 1),complex(1, 1),  complex(2, 1), complex(1, 2)},
            {complex(0, 0), complex(1, 0), complex(2,0), complex(2,1), complex(2,2)},
            {complex(0,0), complex(0,1), complex(0,2), complex(0,3)},
            {complex(0,0), complex(0,1), complex(1,0), complex(1,1)},
        ]
        heights = [0, 2, 2, 3, 1]
        stream_size = len(parsed_input)
        stream = itertools.cycle(parsed_input)
        fall = complex(0, -1)

        landed = set()
        height = 0
        flats_at = {}

        # SHOW = 20
        i = cycle_offset = 0
        cycle_detection = None
        for j in range(n):
            i = j + cycle_offset
            rock = rocks[i % 5]
            offset = complex(2, height + 4)
            # print(f"{i+1} starts at {offset}")
            falling = True
            while falling:
                wind = -1 if next(stream) == "<" else +1
                o2 = wind + offset
                r2 = {r + o2 for r in rock}
                # if i == SHOW and offset == (4+4j):
                    # print(f"{offset=} {o2=} {landed=}")
                if all(0 <= r.real < 7 for r in r2) and landed.isdisjoint(r2):
                    offset = o2
                # if i == SHOW:
                    # print(f"Rock {i+1}: wind => {offset}")

                o2 = fall + offset
                r2 = {r + o2 for r in rock}
                if all(0 < r.imag for r in r2) and landed.isdisjoint(r2):
                    offset = o2
                    # if i == SHOW:
                        # print(f"Rock {i+1}: gravity => {offset}")
                else:
                    break
                    # if i == SHOW:
                        # print(f"Rock {i+1}: rest => {offset}")
            landed.update({offset + r for r in rock})
            # if i == SHOW: print(f"{i+2} landed. New landed: {landed}")
            height = max(height, int(offset.imag) + heights[i%5])
            # print(f"{i+1} lands at {offset}; {height=}")


            if not cycle_offset and all(complex(x, height) in landed for x in range(7)):
                t = (i % 5, i % stream_size)
                if t not in flats_at:
                    flats_at[t] = (i, height)
                else:
                    prior_i, prior_height = flats_at[t]

                    assert prior_i == 1610
                    assert prior_height == 2524

                    cycle_size = i - prior_i
                    height_diff = height - prior_height

                    cycle_count = (n - i) // cycle_size
                    cycle_offset = cycle_count * cycle_size
                    height += cycle_count * height_diff
                    landed.update(complex(x, height) for x in range(7))

                    assert n - cycle_size < i + cycle_offset < n

            if True:
                cut = 0
                if i % 100000 == 0:
                    for h in range(height, height - 1000, -1):
                        if all(complex(x, h) in landed for x in range(7)):
                            landed = {i for i in landed if i.imag >= h}
                            # print(f"{i=} {h=} {len(landed)=}")
                            break
            if i + 1 == n:
                break

        assert i == n - 1, f"{i=} {cycle_offset=} {n=}"
        if n == 1000000000000:
            assert height  > 1569051119345, height
            assert height != 1569051119351, height
            assert height  < 1569057275920, height
        if n == 2022:
            assert height == 3135, height
        return int(height)

if __name__ == "__main__":
    print(solve(parse(), 2022))
    print(solve(parse(), 1000000000000))

