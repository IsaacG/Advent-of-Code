"""Everyone Codes Day N."""

import logging
from lib import helpers
from lib import parsers

log = logging.info
DIAGS = [1+1j, 1-1j,-1+1j,-1-1j]

def p3(data):
    all_coords = [complex(x, y) for x in range(34) for y in range(34)]
    active = set()

    def neighbors(i):
        for d in DIAGS:
            if i + d in all_coords:
                yield i + d

    def print_active():
        for y in range(34):
            print("".join(
                "#" if complex(x,y) in active else "."
                for x in range(34)
            ))

    want_steps = 1000000000
    assert data.max_x == data.max_y == 7
    want_active = {i + 13 + 13j for i in data.all_coords if i in data.coords["#"]}
    want_off = {i + 13 + 13j for i in data.all_coords if i not in data.coords["#"]}
    # print(f"{len(want_active)=}")
    # print(f"{len(want_off)=}")

    if False:
        for y in range(13, 13+9):
            print("".join(
                "#" if complex(x,y) in want_active else "."
                for x in range(13, 13+9)
            ))
        print()

        for y in range(13, 13+9):
            print("".join(
                "#" if complex(x,y) in want_off else "."
                for x in range(13, 13+9)
            ))
        print()

    total = 0
    seen_at = {}
    seen = {}

    for step in range(5000):
        active = frozenset({
            c for c in all_coords
            if (
                (c in active and sum(n in active for n in neighbors(c)) % 2 == 1)
                or (c not in active and sum(n in active for n in neighbors(c)) % 2 == 0)
            )
        })
        if want_active.issubset(active) and want_off.isdisjoint(active):
            print(step)
            seen_at[step] = len(active)
            if active in seen:
                cycle_start = seen[active]
                cycle = step - cycle_start
                print(f"{seen_at=}")
                print(f"{cycle_start=}")
                print(f"{cycle=}")
                spots = set()
                for prior in seen_at:
                    if prior >= cycle_start:
                        spots.update(range(cycle_start+(prior-cycle_start), want_steps, cycle))
                total = 0
                for spot in spots:
                    total += seen_at[((spot - cycle_start) % cycle) + cycle_start]
                return total

            seen[active] = step
    raise RuntimeError("Nope")

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    if part == 3:
        return p3(data)
    active = data.coords["#"]
    total = 0

    def neighbors(i):
        for d in DIAGS:
            if i + d in data.all_coords:
                yield i + d

    def print_active():
        for y in range(data.max_y+1):
            print("".join(
                "#" if complex(x,y) in active else "."
                for x in range(data.max_x+1)
            ))

    for _ in range(10 if part == 1 else 2025):
        #print_active()
        #print()
        active = {
            c for c in data.all_coords
            if (
                (c in active and sum(n in active for n in neighbors(c)) % 2 == 1)
                or (c not in active and sum(n in active for n in neighbors(c)) % 2 == 0)
            )
        }
        # print( len(active))
        total += len(active)
    return total


PARSER = parsers.CoordinatesParser()
TEST_DATA = [
    """\
.#.##.
##..#.
..##.#
.#.##.
.###..
###.##""",
    """\
#......#
..#..#..
.##..##.
...##...
...##...
.##..##.
..#..#..
#......#""",
]
TESTS = [
    (1, TEST_DATA[0], 200),
    (3, TEST_DATA[1], 278388552),
]

if __name__ == "__main__":
    helpers.run_solution(globals())
