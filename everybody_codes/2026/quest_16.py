"""Everyone Codes Event 2026 Day 16."""

import io
from lib import helpers


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
