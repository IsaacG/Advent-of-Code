"""Everyone Codes Day N."""
# pylint: disable=C3001


def solve(part: int, data: str, testing: bool) -> int:
    """Solve the parts."""
    given_input = int(data)
    col_count = -1
    used = 0
    thickness = 1
    added_per_column: list[int] = []

    def next_used_3() -> int:
        cum_thick = [sum(added_per_column[i:]) for i in range(len(added_per_column))]
        remaining = [ct - ((priests * col_count * ct) % acolytes) for ct in cum_thick[:-1]] + cum_thick[-1:]
        return 2 * sum(remaining[1:]) + remaining[0]

    if part == 1:
        provided = given_input
        next_used = lambda: used + col_count
        next_thickness = lambda: 1
    elif part == 2:
        acolytes = 5 if testing else 1111
        provided = 50 if testing else 20240000
        next_used = lambda: used + thickness * col_count
        next_thickness = lambda: (thickness * given_input) % acolytes
    else:
        priests = given_input
        acolytes = 5 if testing else 10
        provided = 160 if testing else 202400000
        next_used = next_used_3
        next_thickness = lambda: ((thickness * priests) % acolytes) + acolytes

    while used <= provided:
        col_count += 2
        added_per_column.append(thickness)
        used = next_used()
        thickness = next_thickness()

    return (used - provided) * (1 if part == 3 else col_count)


TESTS = [
    (1, "13", 21),
    (2, "3", 27),
    (3, "2", 2),
]
