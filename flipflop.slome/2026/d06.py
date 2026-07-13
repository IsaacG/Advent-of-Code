"""FlipFlop Codes, Puzzle 6: Gears And Lights."""

import string
from lib import helpers, parsers


def solve(part: int, data: parsers.CoordinatesParser) -> int:
    """Solve the parts."""
    # Parse the input, setting up the data we will use.
    start = data.coords["S"].copy().pop()
    gears = data.coords["#"]
    if part > 1:
        # Parts two, three: "3" is also a gear.
        gears |= data.coords["3"]
    # Bluetooth inputs are lowercase letters.
    bt_inputs = {pos for pos, char in data.chars.items() if char in string.ascii_lowercase}

    def is_non_prime_group(pos: tuple[int, int]) -> bool:
        """Return if a group of gears contains a non-prime number of gears."""
        todo = [pos]
        seen = {pos}
        while todo:
            pos = todo.pop()
            for neighbor in helpers.neighbors_t(*pos):
                if neighbor not in seen and neighbor in gears:
                    seen.add(neighbor)
                    todo.append(neighbor)
        size = len(seen)
        return any(size % neighbor == 0 for neighbor in range(2, int(size**0.5) + 1))  # or size == 1

    # Use Dijksta's to compute all gear rotations.
    rotations = {start: False}  # False = CCW = Left = low
    todo = list(rotations.items())
    seen = {start}

    while todo:
        pos, rotation = todo.pop()
        rotation = not rotation  # Alternate rotation
        for neighbor in helpers.neighbors_t(*pos):
            if neighbor in seen:
                continue
            if neighbor in gears:
                seen.add(neighbor)
                rotations[neighbor] = rotation
                todo.append((neighbor, rotation))
            elif part > 1 and neighbor in bt_inputs:
                seen.add(neighbor)
                # Map the BT input to a BT output and check BT output neighbors.
                output = data.coords[data.chars[neighbor].upper()].copy().pop()
                for neighbor in helpers.neighbors_t(*output):
                    if neighbor in seen or neighbor not in gears:
                        continue
                    if part == 2 or is_non_prime_group(neighbor):
                        todo.append((neighbor, rotation))

    # Determine which lights are high, low or off.
    bits = []
    for light in sorted(data.coords["*"], key=lambda x: (x[1], x[0])):
        adjacent = next((neighbor for neighbor in helpers.neighbors_t(*light) if neighbor in rotations), None)
        if not adjacent:
            continue
        bits.append("1" if rotations[adjacent] else "0")
    return int("".join(bits), 2)


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
WANT = [4, 1195, 148]
TESTS = [(i, TEST_DATA, want) for i, want in enumerate(WANT, start=1)]

if __name__ == "__main__":
    helpers.run_solution(globals())
