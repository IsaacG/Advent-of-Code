"""Everyone Codes Day N."""

from lib import parsers


def engrave(x: int, y: int) -> bool:
    """Return if a location shove be engraved."""
    nx, ny = 0, 0
    for _ in range(100):
        # [X1,Y1] * [X2,Y2] = [X1 * X2 - Y1 * Y2, X1 * Y2 + Y1 * X2]
        nx, ny = nx * nx - ny * ny, nx * ny * 2
        nx, ny = int(nx / 100000), int(ny / 100000)
        nx, ny = nx + x, ny + y
        if not (-1000000 <= nx <= 1000000 and -1000000 <= ny <= 1000000):
            return False
    return True


def solve(part: int, data: list[list[int]]) -> int | str:
    """Solve the parts."""
    num_a = complex(*data[0])
    num = complex()
    if part == 1:
        for _ in range(3):
            num *= num
            num = complex(int(num.real) // 10, int(num.imag) // 10) + num_a
        return f"[{int(num.real)},{int(num.imag)}]"

    step = 1 if part == 3 else 10
    return sum(
        engrave(x, y)
        for y in range(data[0][1], data[0][1] + 1001, step)
        for x in range(data[0][0], data[0][0] + 1001, step)
    )


PARSER = parsers.parse_ints
TESTS = [
    (1, "A=[25,9]", "[357,862]"),
    (2, "A=[35300,-64910]", 4076),
    (3, "A=[35300,-64910]", 406954),
]


if __name__ == "__main__":
    for _part, _data, expected in TESTS:
        assert solve(_part, PARSER.parse(_data)) == expected
    print("Tests pass.")
    day = __file__.split("_", maxsplit=1)[-1].split(".")[0]
    for _part in range(1, 4):
        with open(f"inputs/{day}.{_part}.txt", encoding="utf-8") as f:
            print(_part, solve(_part, PARSER.parse(f.read())))
