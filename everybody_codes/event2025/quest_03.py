"""Everyone Codes Day N."""

import logging

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    boxes = [int(i) for i in data.split(",")]
    if part == 1:
        return sum(set(boxes))
    if part == 2:
        return sum(sorted(set(boxes))[:20])

    sets = 0
    while boxes:
        for i in set(boxes):
            boxes.remove(i)
        sets +=1
    return sets




    pass


TEST_DATA = [
]
TESTS = [
    (1, "10,5,1,10,3,8,5,2,2", 29),
    (2, "4,51,13,64,57,51,82,57,16,88,89,48,32,49,49,2,84,65,49,43,9,13,2,3,75,72,63,48,61,14,40,77", 781),
    (3, "4,51,13,64,57,51,82,57,16,88,89,48,32,49,49,2,84,65,49,43,9,13,2,3,75,72,63,48,61,14,40,77", 3),
]

if __name__ == "__main__":
    for _part, _data, expected in TESTS:
        assert solve(_part, PARSER.parse(_data)) == expected
    print("Tests pass.")
    day = __file__.split("_", maxsplit=1)[-1].split(".")[0]
    for _part in range(1, 4):
        with open(f"inputs/{day}.{_part}.txt", encoding="utf-8") as f:
            etprint(_part, solve(_part, PARSER.parse(f.read())))
