"""Everyone Codes Day N."""

import collections
from typing import cast
from lib import helpers
from lib import parsers

Fishbone = collections.namedtuple("Fishbone", ["index", "segments"])


def parse(numbers: list[int]) -> Fishbone:
    """Parse a Fishbone from a line of input."""
    segments: list[list[int | None]] = []
    index, *values = numbers
    for number in values:
        for segment in segments:
            if number < cast(int, segment[1]) and segment[0] is None:
                segment[0] = number
                break
            if number > cast(int, segment[1]) and segment[2] is None:
                segment[2] = number
                break
        else:
            segments.append([None, number, None])

    return Fishbone(index, segments)


def spine(fishbone: Fishbone) -> int:
    """Extract the spine of a fishbone."""
    return int("".join(str(s[1]) for s in fishbone.segments))


def sword_sort(sword: Fishbone) -> tuple[int, list[int], int]:
    """Return sort value for a fishbone."""
    return (
        spine(sword),
        [int("".join(str(i) for i in segment if i is not None)) for segment in sword.segments],
        sword.index,
    )


def solve(part: int, data: list[list[int]]) -> int:
    """Solve the parts."""
    swords = [parse(numbers) for numbers in data]
    swords.sort(key=sword_sort, reverse=True)
    spines = [spine(i) for i in swords]
    return [
        spines[0],
        max(spines) - min(spines),
        sum(idx * pos for idx, (pos, segments) in enumerate(swords, start=1)),
    ][part - 1]


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
    (1, "58:5,3,7,8,9,10,4,5,7,8,8", 581078),
    (2, TEST_DATA[0], 77053),
    (3, TEST_DATA[1], 260),
    (3, TEST_DATA[2], 4),
]

if __name__ == "__main__":
    helpers.run_solution(globals())
