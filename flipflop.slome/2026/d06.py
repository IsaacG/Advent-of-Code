"""FlipFlop Codes, Puzzle 6: Gears And Lights."""

import logging
import string
from lib import helpers, parsers

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    if part == 1:
        start = data.coords["S"].copy().pop()
        gears = data.coords["#"]
        rotations = {start: False}
        todo = [(start, False)]  # False = CCW = Left = low
        seen = {start}
        log("Start loop")
        while todo:
            pos, rot = todo.pop()
            for i in helpers.neighbors_t(*pos):
                if i in seen or i not in gears:
                    continue
                seen.add(i)
                rotations[i] = not rot
                todo.append((i, not rot))
        log("End loop")

        bits = []
        for light in sorted(data.coords["*"], key=lambda x: (x[1], x[0])):
            adjacent = next((i for i in helpers.neighbors_t(*light) if i in rotations), None)
            if not adjacent:
                continue
            bits.append("1" if rotations[adjacent] else "0")
        return int("".join(bits), 2)

    if part == 2:
        start = data.coords["S"].copy().pop()
        gears = data.coords["#"] | data.coords["3"]
        receivers = {pos for pos, char in data.chars.items() if char in string.ascii_lowercase}
        rotations = {start: False}
        todo = [(start, False)]  # False = CCW = Left = low
        seen = {start}
        log("Start loop")
        while todo:
            pos, rot = todo.pop()
            for i in helpers.neighbors_t(*pos):
                if i in seen:
                    continue
                if i in gears:
                    seen.add(i)
                    rotations[i] = not rot
                    todo.append((i, not rot))
                if i in receivers:
                    seen.add(i)
                    output = data.coords[data.chars[i].upper()].copy().pop()
                    todo.append((output, rot))
        log("End loop")

        bits = []
        for light in sorted(data.coords["*"], key=lambda x: (x[1], x[0])):
            adjacent = next((i for i in helpers.neighbors_t(*light) if i in rotations), None)
            if not adjacent:
                continue
            bits.append("1" if rotations[adjacent] else "0")
        return int("".join(bits), 2)

    def non_prime_group(pos):
        todo = [pos]
        seen = {pos}
        while todo:
            pos = todo.pop()
            for i in helpers.neighbors_t(*pos):
                if i in seen or i not in gears:
                    continue
                seen.add(i)
                todo.append(i)
        n = len(seen)
        return not (n > 1 and all(n % i != 0 for i in range(2, int(n**0.5) + 1)))

    if part == 3:
        start = data.coords["S"].copy().pop()
        gears = data.coords["#"] | data.coords["3"]
        receivers = {pos for pos, char in data.chars.items() if char in string.ascii_lowercase}
        rotations = {start: False}
        todo = [(start, False)]  # False = CCW = Left = low
        seen = {start}
        log("Start loop")
        while todo:
            pos, rot = todo.pop()
            for i in helpers.neighbors_t(*pos):
                if i in seen:
                    continue
                if i in gears:
                    seen.add(i)
                    rotations[i] = not rot
                    todo.append((i, not rot))
                if i in receivers:
                    seen.add(i)
                    output = data.coords[data.chars[i].upper()].copy().pop()
                    for i in helpers.neighbors_t(*output):
                        if i in seen or i not in gears:
                            continue
                        if non_prime_group(i):
                            todo.append((i, not rot))
        log("End loop")

        bits = []
        for light in sorted(data.coords["*"], key=lambda x: (x[1], x[0])):
            adjacent = next((i for i in helpers.neighbors_t(*light) if i in rotations), None)
            if not adjacent:
                continue
            bits.append("1" if rotations[adjacent] else "0")
        return int("".join(bits), 2)


# PARSER = parsers.parse_one_str
TEST_DATA = """\
;&%,&/<.%~&|-!-;-+`.
=#######:@#=*3333,%!
@*+;|.|####.!3,33A&^
-<a|*!~#`!#~`3*-3|/;
S##########*@/!`-|`-
,,|@:#./,@#,,@B=@!%@
<3C!*#`~=*#;./333*.@
%3@&/#*:`~#^|/+3<!&=
|33*><:b###<<c333*~|
<&&@/:!|``:/:&:&&`,&"""

TESTS = [
    (1, TEST_DATA, 4),
    (2, TEST_DATA, 1195),
    (3, TEST_DATA, 148),
]

if __name__ == "__main__":
    helpers.run_solution(globals())
