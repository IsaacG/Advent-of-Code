"""Everyone Codes Event 2026 Day 16."""

import io
from lib import helpers


def show_pointers(sequence: str, start: int, end: int, msg: str | None = None) -> None:
    print(sequence)
    out = " " * start + "^" + " " * (end - start - 1) + "^"
    if msg:
        out += " " * (len(sequence) - end + 1) + msg
    print(out, "\n")


def part2_visual():
    import collections
    import itertools
    tabs = list(tablets)
    count = 0
    while (c := collections.Counter(i for i, j in itertools.groupby(tabs))).most_common(1)[0][1] != 1:
        pos = 0
        for i, j in itertools.groupby(tabs):
            j = list(j)
            pos += len(j)
            if c[i] == 1:
                continue
            end = next(k for k in range(len(tabs) - 1, -1, -1) if tabs[k] == i) + 1
            if part == 1:
                count += 1
            else:
                count += end - pos
                swap = end - pos
                show_pointers("".join(tabs), pos, end - 1, f"{swap} swaps")
            tabs = tabs[:pos] + list(reversed(tabs[pos:end])) + tabs[end:]
            break

    return count


def solve(part: int, data: str) -> int:
    """Solve the parts.

    We select the left most tablet.
    Walk inwards from the two ends, finding a section bracketed by those colors.
    Flip the number of tablets based on the pointer distance.
    As we walk past tablets of other colors, collect those (interleaving tablets from the left and right).
    When we get to the center, start over with the remaining (reversed) remaining tablets.
    """
    tablets = data * [1, 10, 100][part - 1]

    count = 0
    while tablets:
        color = tablets[0]
        remaining = io.StringIO()
        front = True
        a, b = 0, len(tablets) - 1

        while a < b and tablets[b] != color:
            remaining.write(tablets[b])
            b -= 1

        while a < b:
            if front:
                while a < b and tablets[a] == color:
                    a += 1
            else:
                while a < b and tablets[b] == color:
                    b -= 1
            if a >= b:
                break

            if part == 1:
                count += 1
            else:
                count += b - a + 1

            if front:
                while a < b and tablets[a] != color:
                    remaining.write(tablets[a])
                    a += 1
            else:
                while a < b and tablets[b] != color:
                    remaining.write(tablets[b])
                    b -= 1
            front = not front

        tablets = remaining.getvalue()[::-1]
    return count


if __name__ == "__main__":
    helpers.run_solution(globals())
