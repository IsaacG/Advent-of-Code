"""Everyone Codes Event 2026 Day N."""

from lib import helpers


def solve(part: int, data: str) -> int:
    """Solve the parts."""
    data.sort()
    if part > 1:
        new_data = []
        for x, y, width in data:
            new_data.append((x, y))
            if width > 1:
                new_data.append((x + width - 1, y))
        data = new_data

    total = 0
    a, b = 0, len(data) - 1
    prior_height = 0
    while a <= b:
        new_height = max(prior_height, min(data[a][1], data[b][1]))
        height_delta, prior_height = max(0, new_height - prior_height), new_height
        width = data[b][0] - data[a][0] + 1
        if data[a][1] < data[b][1]:
            a += 1
        else:
            b -= 1
        total += height_delta * width

    return total


if __name__ == "__main__":
    helpers.run_solution(globals())
