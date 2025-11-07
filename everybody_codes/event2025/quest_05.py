"""Everyone Codes Day N."""

import logging
from lib import parsers

log = logging.info

def fishbone(numbers):
    segments = []
    for number in numbers:
        for segment in segments:
            if number < segment[1] and segment[0] is None:
                segment[0] = number
            elif number > segment[1] and segment[2] is None:
                segment[2] = number
            else:
                continue
            break
        else:
            segments.append([None, number, None])

    return segments

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    if part == 1:
        numbers = data[0][1:]
        return "".join(str(s[1]) for s in fishbone(numbers))
    if part == 2:
        vals = [
            int("".join(str(s[1]) for s in fishbone(numbers[1:])))
            for numbers in data
        ]
        return max(vals) - min(vals)

    swords = []
    for numbers in data:
        swords.append((fishbone(numbers[1:]), numbers[0]))

    def s(p):
        segments, idx = p
        return (-int("".join(str(s[1]) for s in segments)), [-int("".join(str(i) for i in segment if i is not None)) for segment in segments], -idx)

    swords.sort(key=s)
    return sum(
        idx * pos for idx, (segments, pos) in enumerate(swords, start=1)
    )
            
    pass


PARSER = parsers.parse_ints
TEST_DATA = [
    """\
1:2,4,1,1,8,2,7,9,8,6
2:7,9,9,3,8,3,8,8,6,8
3:4,7,6,9,1,8,3,7,2,2
4:6,4,2,1,7,4,5,5,5,8
5:2,9,3,8,3,9,5,2,1,4
6:2,4,9,6,7,4,1,7,6,8
7:2,3,7,6,2,2,4,1,4,2
8:5,1,5,6,8,3,1,8,3,9
9:5,7,7,3,7,2,3,8,6,7
10:4,1,9,3,8,5,4,3,5,5""",
    """\
1:7,1,9,1,6,9,8,3,7,2
2:6,1,9,2,9,8,8,4,3,1
3:7,1,9,1,6,9,8,3,8,3
4:6,1,9,2,8,8,8,4,3,1
5:7,1,9,1,6,9,8,3,7,3
6:6,1,9,2,8,8,8,4,3,5
7:3,7,2,2,7,4,4,6,3,1
8:3,7,2,2,7,4,4,6,3,7
9:3,7,2,2,7,4,1,6,3,7""",
    """\
1:7,1,9,1,6,9,8,3,7,2
2:7,1,9,1,6,9,8,3,7,2""",
]
TESTS = [
    (1, "58:5,3,7,8,9,10,4,5,7,8,8", "581078"),
    (2, TEST_DATA[0], 77053),
    (3, TEST_DATA[1], 260),
    (3, TEST_DATA[2], 4),
]

if __name__ == "__main__":
    for _part, _data, expected in TESTS:
        assert solve(_part, PARSER.parse(_data)) == expected
    print("Tests pass.")
    day = __file__.split("_", maxsplit=-1)[-1].split(".")[0]
    for _part in range(1, 4):
        with open(f"inputs/{day}.{_part}.txt", encoding="utf-8") as f:
            print(_part, solve(_part, PARSER.parse(f.read())))
