"""Everyone Codes Day N."""

import logging
import itertools
from lib import helpers
from lib import parsers

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    pos = data.coords["@"].copy().pop()
    count = 0
    dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    movements = dirs
    if part == 3:
        movements = [(0, -1)] * 3 + [(1, 0)] * 3 + [(0, 1)] * 3 + [(-1, 0)] * 3

    moves = itertools.cycle(enumerate(movements))
    seen = {pos,}
    if part == 1:
        end = data.coords["#"].pop()
        while pos != end:
            _, d = next(moves)
            np = pos[0] + d[0], pos[1] + d[1]
            if np in seen:
                continue
            seen.add(np)
            pos = np
            count += 1
        return count

    if part == 2:
        history = []
        seen.update(data.coords["#"])
        want = {(end[0] + d[0], end[1] + d[1]) for d in movements for end in data.coords["#"]} - data.coords["#"]
        while not seen >= want:
            if all((pos[0] + d[0], pos[1] + d[1]) in seen for d in dirs):
                while all((pos[0] + d[0], pos[1] + d[1]) in seen for d in dirs):
                    pos, i = history.pop()
                    count -= 1
                    while i != next(moves)[0]:
                        True
                    for _ in range(len(movements) - 1):
                        next(moves)
            i, d = next(moves)
            np = pos[0] + d[0], pos[1] + d[1]
            if np in seen:
                continue
            seen.add(np)
            history.append((pos, i))
            pos = np
            count += 1
        return count

    if part == 3:
        max_x = max(i[0] for i in data.coords["#"] | data.coords["@"])
        min_x = min(i[0] for i in data.coords["#"] | data.coords["@"])
        max_y = max(i[1] for i in data.coords["#"] | data.coords["@"])
        min_y = min(i[1] for i in data.coords["#"] | data.coords["@"])

        bones = data.coords["#"]
        seen.update(data.coords["#"])
        want = {(end[0] + d[0], end[1] + d[1]) for d in dirs for end in data.coords["#"]} - data.coords["#"]
        print((35,7) in want)
        print(data.chars[(35, 7)])
        print(data.chars[(34, 7)])
        print(data.chars[(36, 7)])
        print(data.chars[(35, 6)])
        print(data.chars[(35, 8)])

        def floodfill(pos):
            s = pos
            todo = [pos]
            area = set()
            done = {pos}
            while todo:
                p = todo.pop()
                if not (min_x <= p[0] <= max_x and min_y <= p[1] <= max_y):
                    return []
                if p in seen or p in area:
                    continue
                area.add(p)
                cands = {(p[0] + d[0], p[1] + d[1]) for d in dirs}
                assert len(cands) == 4
                for np in cands:
                    if np in done or np in seen:
                        continue
                    done.add(np)
                    todo.append(np)
            return area

        filled = set()
        for w in want:
            filled.update(floodfill(w))
        print((35,7) in want)
        print((35,7) in filled)
        print((35,7) in seen)
        print(floodfill((35,7)))
        seen |= filled

        def display():
            x0 = min(p[0] for p in seen)
            x1 = max(p[0] for p in seen)
            y0 = min(p[1] for p in seen)
            y1 = max(p[1] for p in seen)
            print(f"Step: {count}")
            for y in range(y0, y1+1):
                print("".join(" " if (x,y) == pos else "#" if (x,y) in bones else " " if (x,y) in seen else " " for x in range(x0, x1+1)))
            print()

        while not seen >= want:
            if count > 1200:
                display()
            assert not all((pos[0] + d[0], pos[1] + d[1]) in seen for d in dirs), count
            _, d = next(moves)
            np = pos[0] + d[0], pos[1] + d[1]
            if np in seen:
                continue
            pos = np
            seen.add(pos)
            max_x = max(max_x, pos[0])
            min_x = min(min_x, pos[0])
            max_y = max(max_y, pos[1])
            min_y = min(min_y, pos[1])
            count += 1

            for d in dirs:
                flood = set()
                np = pos[0] + d[0], pos[1] + d[1]
                if np not in seen:
                    flood.update(floodfill(np))
                if flood:
                    # print(f"{count=} FF {len(flood)}: {flood}")
                    seen.update(flood)

        return count


PARSER = parsers.CoordinatesParser()
TEST_DATA = [
    """\
.......
.......
.......
.#.@...
.......
.......
.......""",
    """\
#..#.......#...
...#...........
...#...........
#######........
...#....#######
...#...@...#...
...#.......#...
...........#...
...........#...
#..........#...
##......#######""",
    """\
................................................................
.........................###.........###........................
....................##...###########.#####......#.......###.....
.........##.............############....####.............##.....
.......######..............#############.###....................
.........##................#############.###.......##...........
...............##...........########....####....................
...............................####.#######...........##........
........................##################...........####.......
....#.........#########################.....##......######......
..............#.##......##....##..##.##...............##........
..............................##....##..........##..............
........####....#################..######...................##..
........###.....###...####..###..##...##.########...............
.................####....###..##.##.##..###....##.....##........
....##...........#######.....##..##..##......#####..........#...
...........##......#########......#....##.######..........#####.
...........##........###########################....#.......#...
.........######............##################.......#...........
...........##.............#########.............................
............#.........#############....................#........
.....#...........##..####......###......##........#.............
.............##................###..........#.....#.............
..................##...........##...................##..........
..........................###.####.####.........................
................#.###########..###.############.#...............
.....#####....###...............................###.............
.....#####...#############......@......#############............
.....#########.###################################.#............
...###########..##.....###################.....##..##...........
...######...#######.##...###.........##...##...###.##...........
.....##.########........#####..###..####.......#.########.......
............#########################################...........
..............#####################################.............
...............................###..............................
................................................................""",
]
TESTS = [
    (1, TEST_DATA[0], 12),
    (2, TEST_DATA[0], 47),
    # (3, TEST_DATA[0], 87),
    # (3, TEST_DATA[1], 239),
    (3, TEST_DATA[2], 1539),
]

if __name__ == "__main__":
    helpers.run_solution(globals())
