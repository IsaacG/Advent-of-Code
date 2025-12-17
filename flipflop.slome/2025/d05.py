"""FlipFlop Codes: Puzzle 5: Strange tunnels."""
from lib import parsers


def solve(part: int, data: str) -> int | str:
    """Solve the parts."""
    pairs = {}
    first = {}
    for idx, char in enumerate(data):
        if char not in first:
            first[char] = idx
        else:
            pairs[idx] = first[char]
            pairs[first[char]] = idx
    pos = 0
    steps = 0
    end = len(data)
    visited = set()
    while pos != end:
        visited.add(data[pos])
        goto = pairs[pos]
        distance = abs(pos - goto)
        if part == 3 and data[pos].isupper():
            distance *= -1
        steps += distance
        pos = goto + 1
    if part != 2:
        return steps

    out = []
    for tunnel in data:
        if tunnel not in visited and tunnel not in out:
            out.append(tunnel)
    return "".join(out)


PARSER = parsers.parse_one_str
TESTS = [
    (1, "ABccksiPiBAksP", 38),
    (2, "ABccksiPiBAksP", "Bc"),
    (3, "ABccksiPiBAksP", -6),
]
