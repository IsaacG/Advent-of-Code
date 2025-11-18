"""Everyone Codes Day N."""

import logging
import time
from lib import helpers
from lib import parsers

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    if part != 3:
        initial = [complex()]
        if part == 2:
            initial.append(complex(data.max_x, data.max_y))
        boom = set(initial)
        todo = set(initial)
        while todo:
            cur = todo.pop()
            for n in data.neighbors(cur):
                if n not in boom and int(data.chars[n]) <= int(data.chars[cur]):
                    boom.add(n)
                    todo.add(n)
        return len(boom)

    available = data.all_coords.copy()

    def explode(pos):
        boom = set(pos)
        todo = set(pos)
        while todo:
            cur = todo.pop()
            for n in data.neighbors(cur):
                if n in available and n not in boom and data.chars[n] <= data.chars[cur]:
                    boom.add(n)
                    todo.add(n)
        return boom

    picked = []
    log("Start")
    for i in range(3):
        p, c = complex(), 0
        for i in available:
            if i == 0 and data.chars[i] != 9: continue
            if i == 1 and data.chars[i] < 7: continue
            damage = explode([i])
            if len(damage) > c:
                c = len(damage)
                p = i
        picked.append(p)
        log(f"Picked {p} for {c} damage")
        available -= explode([p])

    available = data.all_coords.copy()
    assert len(picked) == 3
    return len(explode(picked))





PARSER = parsers.CoordinatesParser()
TEST_DATA = [
    """\
989611
857782
746543
766789""",
    """\
9589233445
9679121695
8469121876
8352919876
7342914327
7234193437
6789193538
6781219648
5691219769
5443329859""",
    """\
5411
3362
5235
3112""",
    """\
41951111131882511179
32112222211508122215
31223333322105122219
31234444432147511128
91223333322176021892
60112222211166431583
04661111166111111746
01111119042122222177
41222108881233333219
71222127839122222196
56111026279711111507""",
]
TESTS = [
    (1, TEST_DATA[0], 16),
    (2, TEST_DATA[1], 58),
    (3, TEST_DATA[2], 14),
    (3, TEST_DATA[3], 133),
]

if __name__ == "__main__":
    for _part, _data, expected in TESTS:
        assert solve(_part, PARSER.parse(_data)) == expected
    print("Tests pass.")
    day = int(__file__.split("_", maxsplit=-1)[-1].split(".")[0])
    for _part in range(1, 4):
        with open(f"inputs/{day:02}.{_part}.txt", encoding="utf-8") as f:
            _input = PARSER.parse(f.read())  # type: list[list[int]]
            start = time.perf_counter_ns()
            got = solve(_part, _input)
            end = time.perf_counter_ns()
            print(f"{day:02}.{_part} {got:15} {helpers.format_ns(end - start):8}")
