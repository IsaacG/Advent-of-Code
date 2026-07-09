"""FlipFlop Codes, Puzzle 4: Magic Flowerstalk."""

from lib import helpers, parsers


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    size = len(data) - 1
    if part == 1:
        cut = 8 if size == 19 else 400
        keep = data[3: -cut - 1]
        return sum("o" in line for line in keep)
    if part == 2:
        side = None
        swaps = 0
        for line in data[3:-1]:
            if "o" not in line:
                continue
            for i in ["-o", "o-"]:
                if i in line and side is not None and side != i:
                    swaps += 1
                if i in line:
                    side = i
        return swaps
    if part == 3:
        count = 0
        while count == 0 or side is not None:
            side = None
            for idx, line in enumerate(list(data[3:-1]), start=3):
                if "o" not in line:
                    continue
                for i in ["-o", "o-"]:
                    if i not in line:
                        continue
                    if side is None:
                        data[idx] = ""
                        side = i
                    elif side == i:
                        pass
                    else:
                        side = i
                        data[idx] = ""
            if side:
                count += 1

        return count


    


PARSER = parsers.parse_one_str_per_line
TEST_DATA = """\
 \|/
 -@-
 /|\\
  |-o
o-|
o-|
  |-o
  |
o-|
  |-o
  |-o
o-|
o-|
  |
o-|
o-|
  |
o-|
  |-o
#####"""
TESTS = [
    (1, TEST_DATA, 7),
    (2, TEST_DATA, 6),
    (3, TEST_DATA, 5),
]

if __name__ == "__main__":
    helpers.run_solution(globals())
